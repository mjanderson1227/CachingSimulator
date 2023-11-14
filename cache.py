from cache_builder import CacheBuilder
from dataclasses import dataclass
import random

# Address Object to encapsulate cache address.
@dataclass
class Address:
    tag: int
    index: int
    offset: int
    def __init__(self, address: int, builder: CacheBuilder):
        binary_string = bin(address)
        try:
            self.tag = int(binary_string[0:builder.tag_bits], 2)
            print(self.tag)
            self.index = int(binary_string[builder.tag_bits:builder.index_bits], 2)
            self.offset = int(binary_string[builder.index_bits:builder.block_bits], 2)
        except ValueError:
            print(binary_string[builder.tag_bits:builder.index_bits])

@dataclass
class CacheBlock:
    tag: int
    valid: bool
    data: bytearray

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
            block_list = [CacheBlock(0, False, bytearray(builder.block_size)) for _ in range(builder.associativity)]
            row_object = CacheRow(block_list, builder.associativity)
            self.rows.append(row_object)

    def __repr__(self) -> str:
        to_return = []
        for row in self.rows:
            for block in row.blocks:
                to_return.append(str(block.data));
        return '\n'.join(to_return)

    def replace(self, row: CacheRow, to_add: CacheBlock): 
        random_num = random.randrange(len(row.blocks))
        row.blocks[random_num] = to_add

    # def write_cache(self, address: Address, data: list[str]):

    # Need to read the number of bytes from the file and then make the
    def read_cache(self, address: Address, bytes_read: list[str]):
        current_index = address.index
        current_offset = address.offset
        current_row = self.rows[address.index]

        # Access each position in the cache and update cache results.
        for byte in bytes_read:
            if current_offset >= (associativity := self.builder.associativity):
                current_offset -= associativity
                current_index += 1 if current_index + 1 < self.builder.number_rows else -self.builder.number_rows

            is_full = len(current_row.blocks) == self.builder.associativity

            # Will return either an empty array or a single item that has an equivalent tag.
            foundblock = list(filter(lambda item: item.tag == address.tag, current_row.blocks))
            itemlength = len(foundblock)

            # (TODO: CHECK THIS FIRST IF THERE IS AN ISSUE WITH THE NUMBERS.)
            if not itemlength and is_full:
                # Conflict Miss. 
                self.conflict_misses += 1

            elif (block := foundblock.pop()):
                # Hit.
                self.hits += 1
                block.valid = True
                
            else:
                # Compulsory Miss - The next cache block has yet to be filled.
                self.compulsory_misses += 1

            # Fill the cache.
            current_row.blocks[current_index].data[current_offset] = int(byte)
            current_row.blocks[current_index].valid = True
            current_offset += 1
