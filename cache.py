from cache_builder import CacheBuilder
from address import Address
import random

class Cache:
    rows: list[set[int]]
    hits: int
    compulsory_misses: int
    conflict_misses: int
    builder: CacheBuilder
    cpi: float

    def __init__(self, builder: CacheBuilder):
        self.rows = []
        self.hits = 0
        self.compulsory_misses = 0
        self.conflict_misses = 0
        self.builder = builder
        self.cpi = 0.00

        for _ in range(builder.number_rows):
            tag_set = set()
            self.rows.append(tag_set)

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

    def access(self, address: Address, length: int):
        # Keep track of the offset and append each row address to the address queue.
        current_offset = address.offset

        # Determine the addresses that the cache will access.
        addr_queue = [address]
        while current_offset + length > self.builder.block_size:
            next_address = Address(address.full + length, self.builder)
            addr_queue.append(next_address)
            current_offset -= self.builder.block_size

        # Go through the address queue and access each address.
        for current_location in addr_queue:
            current_row = self.rows[current_location.index]
            if current_location.tag in current_row:
                self.hits += 1
                
            else:
                if len(current_row) >= self.builder.associativity:
                    self.conflict_misses += 1
                    random_tag = random.choice(list(current_row))
                    current_row.remove(random_tag)
                else:
                    self.compulsory_misses += 1
                    
                current_row.add(current_location.tag)
