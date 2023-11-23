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
    data: bytearray
    def __init__(self, tag: int, block_size: int):
        self.tag = tag
        self.data = bytearray(block_size)

@dataclass
class CacheRow:
    blocks: dict[int, CacheBlock]

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
            block_list = {}
            row_object = CacheRow(block_list)
            self.rows.append(row_object)


    # Formatting for output printing.
    def __repr__(self) -> str:
        FORMAT_OFFSET = 24
        format_string = lambda label, output: f'{label}: {"".join([" " for _ in range(FORMAT_OFFSET - len(label))])}{output}'

        total_accesses = self.compulsory_misses + self.hits + self.conflict_misses
        hit_rate = round((self.hits * 100) / total_accesses, 4)
        miss_rate = round(100 - hit_rate, 4)

        return '\n'.join([
            "***** CACHE SIMULATION RESULTS *****\n",
            format_string("Total Cache Accesses", f'{total_accesses}'),
            format_string("Cache Hits", f'{self.hits}'),
            format_string("Cache Misses", f'{self.conflict_misses + self.compulsory_misses}'),
            format_string("--- Compulsory Misses", f'{self.compulsory_misses}'),
            format_string("--- Conflict Misses", f'{self.conflict_misses}'),
            "\n***** *****  CACHE HIT & MISS RATE  ***** *****\n",
            format_string("Hit Rate", f'{hit_rate}%'),
            format_string("Miss Rate", f'{miss_rate}%')
            ])

    def print_full(self) -> str:
        to_return = []
        for row_index, row in enumerate(self.rows):
            row_str = [f'row {row_index}']
            for tag, block in row.blocks.items():
                row_str.append(f'\t{tag}: {block.data}');
            to_return.append('\n'.join(row_str))
        return '\n'.join(to_return)

    def access(self, addr_list: list[Address]):
        for current_location in addr_list:
            current_row = self.rows[current_location.index]
            if current_location.tag in current_row.blocks.keys():
                self.hits += 1
            else:
                new_block = CacheBlock(current_location.tag, self.builder.block_size)
                for i in range(0, self.builder.block_size):
                    new_block.data[i] = 0xFF
                if len(current_row.blocks) >= self.builder.associativity:
                    self.conflict_misses += 1
                    random_tag = random.choice(list(current_row.blocks.keys()))
                    current_row.blocks.pop(random_tag)
                    current_row.blocks[current_location.tag] = new_block
                else:
                    self.compulsory_misses += 1
                    current_row.blocks[current_location.tag] = new_block

    def read_cache(self, address: Address, length: int):
        # Determine the addresses that the cache will access.
        addr_list = [address]
        if address.offset + length >= self.builder.block_size:
            second_address = Address(address.full + length, self.builder)
            addr_list.append(second_address)
        self.access(addr_list)
