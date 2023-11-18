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

# Command that the program will use to pass to handle a cache access.
@dataclass
class AccessCommand:
    current_row: Address
    current_length: int
    next_row: Address
    next_length: int
    requires_row_carry: bool

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

        total_accesses = sum([self.compulsory_misses, self.conflict_misses, self.hits])
        hit_rate = round((self.hits * 100) / total_accesses, 4)
        miss_rate = round(1 - hit_rate, 4)

        return '\n'.join([
            "***** CACHE SIMULATION RESULTS *****\n",
            format_string("Total Cache Accesses", f'{total_accesses}'),
            format_string("Cache Hits", f'{self.hits}'),
            format_string("Cache Misses", f'{self.conflict_misses + self.compulsory_misses}'),
            format_string("--- Compulsory Misses", f'{self.compulsory_misses}'),
            format_string("--- Conflict Misses", f'{self.conflict_misses}'),
            "\n***** *****  CACHE HIT & MISS RATE  ***** *****\n",
            format_string("Hit Rate", hit_rate),
            format_string("Miss Rate", miss_rate)
            ])

    def print_full(self) -> str:
        to_return = []
        for row_index, row in enumerate(self.rows):
            row_str = [f'row {row_index}']
            for tag, block in row.blocks.items():
                row_str.append(f'\t{tag}: {block.data}');
            to_return.append('\n'.join(row_str))
        return '\n'.join(to_return)


    def access(self, command: AccessCommand):
        row1 = self.rows[command.current_row.index]
        cur_tag = command.current_row.tag
        cur_offset = command.current_row.offset

        is_valid = command.current_row.tag in row1.blocks.keys()
        if is_valid:
            self.hits += 1
        else:
            block_to_add = CacheBlock(cur_tag, self.builder.block_size)
            for i in range(cur_offset, self.builder.block_size):
                block_to_add.data[i] = 0xFF
            if len(row1.blocks) >= self.builder.associativity:
                random_tag = random.choice(list(row1.blocks.keys()))
                del row1.blocks[random_tag]
                self.conflict_misses += 1
                row1.blocks[cur_tag] = block_to_add
            else:
                self.compulsory_misses += 1
                row1.blocks[cur_tag] = block_to_add

        row2 = self.rows[command.next_length]

        if command.requires_row_carry and not is_valid:
            block_to_add = CacheBlock(command.next_row.tag, self.builder.block_size)
            for i in range(0, command.next_length):
                block_to_add.data[i] = 0xFF
            if len(row2.blocks) >= self.builder.associativity:
                random_tag = random.choice(list(row2.blocks.keys()))
                del row2.blocks[random_tag]
                row2.blocks[command.next_row.tag] = block_to_add
            else:
                row2.blocks[command.next_row.tag] = block_to_add

    # Need to read the number of bytes from the file and then make the
    def read_cache(self, address: Address, length: int):
        for _ in range(length):
            new_offset = self.builder.block_size - address.offset
            next_row_address = Address(address.full + new_offset, self.builder)

            command = AccessCommand(address, new_offset, next_row_address, address.offset, address.offset != 0)
            self.access(command)

            # Increment the address.
            address = Address(address.full + 1, self.builder)
