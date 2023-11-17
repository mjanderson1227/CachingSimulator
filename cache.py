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
            row_object = CacheRow(block_list, self.builder.associativity)
            self.rows.append(row_object)

    def __repr__(self) -> str:
        to_return = []
        for row in self.rows:
            for block in row.blocks:
                to_return.append(str(block.data));
        return '\n'.join(to_return)

    # Need to read the number of bytes from the file and then make the
    def read_cache(self, address: Address):

        # Split the address if a miss will cover 2 rows.
        logistics: list[tuple[Address, int]] = [(address, self.builder.block_size - address.offset)]
        if address.offset != 0:
            next_row = Address(address.full + self.builder.block_size, self.builder)
            logistics.append((next_row, address.offset))

        for row_info in logistics:
            cur_address = row_info[0]
            n_bytes = row_info[1]
            print(bin(cur_address.offset), n_bytes)

            current_row = self.rows[cur_address.index]
            is_full = current_row.blocks_filled >= self.builder.associativity

            # Find a block that has a matching tag.
            filtered_row = list(filter(lambda block: block.tag == address.tag, current_row.blocks))

            # Block was not found in the list.
            if len(filtered_row) == 0:
                block_data = None
                if is_full:
                    # Conflict Miss, swap a block.
                    self.conflict_misses += 1
                    random_index = random.randrange(self.builder.associativity)
                    random_block = current_row.blocks[random_index]
                    random_block.tag = cur_address.tag
                    random_block.valid = True
                    block_data = random_block

                else:
                    self.compulsory_misses += 1
                    next_block = current_row.blocks[current_row.blocks_filled]
                    next_block.valid = True
                    next_block.tag = cur_address.tag
                    current_row.blocks_filled += 1
                    block_data = next_block

                # move n_bytes of memory into the cache.
                tracked_offset = cur_address.offset
                for _ in range(n_bytes):
                    # print(tracked_offset)
                    block_data.data[tracked_offset] = 0xFF
                    tracked_offset += 1


            # Block with matching tag found in the list.
            else:
                self.hits += 1
