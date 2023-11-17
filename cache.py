from cache_builder import CacheBuilder
from dataclasses import dataclass
import random

# Address Object to encapsulate cache address.
@dataclass
class Address:
    full: int
    tag: int
    index: int
    offset: int
    # If the address does not have proper zero padding, then this will not work.
    def __init__(self, address: int, builder: CacheBuilder):
        while address >= builder.physical_size:
            address -= builder.physical_size
        self.full = address
        self.partition(builder)

    # Partition the address to conform the address and cache parameters.
    def partition(self, builder: CacheBuilder):
        # Discard "0b"
        binary_string = bin(self.full)[2:]

        # Pad the binary string with zeros so that it conforms to the physical address.
        if len(binary_string) < builder.address_bits:
            diff = builder.address_bits - len(binary_string)
            binary_string = ('0' * diff) + binary_string

        # Partition the string into the tag, index, and offset.
        self.tag = int(binary_string[0:builder.tag_bits], 2)
        off_begin = builder.index_bits + builder.tag_bits
        self.index = int(binary_string[builder.tag_bits:off_begin], 2)
        self.offset = int(binary_string[off_begin:], 2)

@dataclass
class CacheBlock:
    tag: int
    valid: bool
    data: bytearray
    def __init__(self, block_size: int):
        self.tag = 0
        self.valid = False
        self.data = bytearray(block_size)

@dataclass
class CacheRow:
    blocks: list[CacheBlock]
    blocks_filled: int

class Cache:
    rows: list[CacheRow]
    hits: int
    compulsory_misses: int
    conflict_misses: int
    builder: CacheBuilder

    def __init__(self, builder: CacheBuilder):
        self.rows = []
        self.hits = 0
        self.compulsory_misses = 0
        self.conflict_misses = 0
        self.builder = builder

        for _ in range(builder.number_rows):
            block_list = [CacheBlock(self.builder.block_size) for _ in range(self.builder.associativity)]
            row_object = CacheRow(block_list, 0)
            self.rows.append(row_object)

    # Formatting for output printing.
    def __repr__(self) -> str:
        to_return = []
        for row_index, row in enumerate(self.rows):
            row_str = [f'row {row_index}']
            for block_index, block in enumerate(row.blocks):
                row_str.append(f'\t{block_index}: {block.data}');
            to_return.append('\n'.join(row_str))
        to_return.append(str(self.hits))
        to_return.append(str(self.compulsory_misses))
        to_return.append(str(self.conflict_misses))
        return '\n'.join(to_return)

    def access(self, address_list: list[Address], length_list: list[int]):
        address = address_list[0]
        cur_row = self.rows[address.index]
        found_block = list(filter(lambda block: block.tag == address.tag, cur_row.blocks))
        if len(found_block) == 0:
            new_block = None
            if cur_row.blocks_filled == (associativity := self.builder.associativity) - 1:
                print("Conflict Miss.")
                self.conflict_misses += 1
                random_block = cur_row.blocks[random.randrange(associativity)]
                random_block.tag = address.tag
                new_block = random_block
            else:
                print("Compulsory Miss.")
                self.compulsory_misses += 1
                next_block = cur_row.blocks[cur_row.blocks_filled + 1]
                next_block.tag = address.tag
                next_block.valid = True
                cur_row.blocks_filled += 1
                new_block = next_block
            # Fill the cache.
            for address, length in zip(address_list, length_list):
                end_index = address.offset + length
                for index in range(address.offset, end_index):
                    new_block.data[index] = 0xFF
        else:
            # print(found_block)
            print("Hit!")
            self.hits += 1

    # Need to read the number of bytes from the file and then make the
    def read_cache(self, address: Address, length: int):
        for _ in range(length):
            addr_list = [address]
            length_list = [self.builder.block_size]
            if address.offset != 0:
                remaining_space = self.builder.block_size - address.offset
                addr_next_row = Address(address.full + remaining_space, self.builder)
                addr_list.append(addr_next_row)
                length_list[0] -= address.offset
                length_list.append(address.offset)
            # print(addr_list)
            # print(length_list)
            self.access(addr_list, length_list)
            address = Address(address.full + 1, self.builder)
