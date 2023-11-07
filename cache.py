from cache_builder import CacheBuilder
from dataclasses import dataclass

# Address Object to encapsulate cache address.
@dataclass
class Address:
    tag: int
    index: int
    offset: int
    def get_full(self) -> str:
        return ''.join([hex(x) for x in self.__dataclass_fields__.values()])

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

    def __init__(self, builder: CacheBuilder):
        for _ in range(builder.number_rows):
            create_block = lambda: bytearray([0 for _ in range(builder.block_size)])
            block_list = [CacheBlock(0, False, create_block()) for _ in range(builder.associativity)]
            row_object = CacheRow(block_list, builder.associativity)
            self.rows.append(row_object)
