from cache_builder import CacheBuilder
from address import Address
from math import ceil
import random

class Cache:
    rows: list[set[int]]
    hits: int
    compulsory_misses: int
    conflict_misses: int
    builder: CacheBuilder
    clock_cycles: int
    total_instructions: int

    def __init__(self, builder: CacheBuilder):
        self.rows = []
        self.hits = 0
        self.compulsory_misses = 0
        self.conflict_misses = 0
        self.builder = builder
        self.clock_cycles = 0
        self.total_instructions = 0
        self.blocks_filled = 0

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
        unused_blocks = self.builder.number_blocks - self.blocks_filled
        overhead_per_block = self.builder.overhead / self.builder.number_blocks
        unused_kb = unused_blocks * (self.builder.block_size + overhead_per_block) / 1024
        use_percentage = round(unused_kb / self.builder.implementation_size * 100, 2)
        waste = round(unused_kb * 0.09, 2)

        return '\n'.join([
            "***** CACHE SIMULATION RESULTS *****\n",
            format_string("Total Cache Accesses", f'{total_accesses}'),
            format_string("Cache Hits", f'{self.hits}'),
            format_string("Cache Misses", f'{self.conflict_misses + self.compulsory_misses}'),
            format_string("--- Compulsory Misses", f'{self.compulsory_misses}'),
            format_string("--- Conflict Misses", f'{self.conflict_misses}'),
            "\n***** *****  CACHE HIT & MISS RATE  ***** *****\n",
            format_string("Hit Rate", f'{hit_rate}%'),
            format_string("Miss Rate", f'{miss_rate}%'),
            format_string("CPI", f'{self.clock_cycles / self.total_instructions:.2f} Cycles/Instruction'),
            format_string("Unused Cache Space", f'{unused_kb:.2f} KB / {self.builder.implementation_size} KB = {use_percentage:}% Waste: ${waste}'),
            format_string("Unused Cache blocks", f'{unused_blocks} / {self.builder.number_blocks}'),
            ])

    def access(self, address: Address, length: int, access_type: str):
        # Increment instruction count if it is an instruction.
        if access_type == "I":
            self.total_instructions += 1

        # Track the offset of each address that is accessed.
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
            status = None

            if current_location.tag in current_row:
                self.hits += 1
                status = "hit"
            elif len(current_row) >= self.builder.associativity:
                self.conflict_misses += 1
                random_tag = random.choice(list(current_row))
                current_row.remove(random_tag)
                status = "miss"
                self.blocks_filled += 1
            else:
                self.compulsory_misses += 1
                status = "miss"
                self.blocks_filled += 1

            n_read = ceil(self.builder.block_size / 4)
            if access_type == "I":
                self.clock_cycles += 1 if status == "hit" else 4 * n_read
                self.clock_cycles += 2
            else:
                self.clock_cycles += 1 if status == "hit" else 4 * n_read
                self.clock_cycles += 1

            current_row.add(current_location.tag)
