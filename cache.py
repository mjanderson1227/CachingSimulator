from cache_builder import CacheBuilder
from dataclasses import dataclass
from address import Address
import random

@dataclass
class CacheBlock:
    tag: int
    data: bytearray
    def __init__(self, tag: int, block_size: int):
        self.tag = tag
        self.data = bytearray(block_size)

@dataclass
class CacheRow:
    blocks: dict[int, set]

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

    def access(self, addr_list: list[Address]):
        for current_location in addr_list:
            current_row = self.rows[current_location.index]
            if current_location.tag in current_row.blocks.keys():
                self.hits += 1
            else:
                new_block = CacheBlock(current_location.tag, self.builder.block_size)
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
        addr_queue = [address]
        if address.offset + length > self.builder.block_size:
            second_address = Address(address.full + length, self.builder)
            addr_queue.append(second_address)
        self.access(addr_queue)
