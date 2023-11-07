import math

# CacheBuilder will be passed into the constructor of the Cache class to get the desired values.
class CacheBuilder:
    def __init__(
            self, 
            trace_files: list[str],
            cache_size: int,
            block_size: int,
            associativity: int,
            replacement_policy: str,
            physical_size: int):

        # Constructed values.
        self.trace_files = trace_files
        self.cache_size = cache_size * 1024
        self.block_size = block_size
        self.associativity = associativity
        self.replacement_policy = replacement_policy
        self.physical_size = physical_size * 1024

        # Calculated values.
        self.number_blocks = int(self.cache_size / self.block_size)
        self.number_rows = int(self.number_blocks / self.associativity)
        self.address_bits = math.ceil(math.log2(self.physical_size))
        self.block_bits = math.ceil(math.log2(block_size))
        self.index_bits = math.ceil(math.log2(self.number_rows))
        self.tag_bits = self.address_bits - self.block_bits - self.index_bits

        # Calculate overhead.
        self.overhead = self.number_rows * (self.tag_bits + 1)
        self.total_size = self.overhead + self.cache_size

    # Print info about the cache that will be built using this class.
    def __repr__(self) -> str:
        str_list = []
        str_list.append(f'Trace File(s): {", ".join(self.trace_files)}\n')
        str_list.append('***** Cache Input Parameters *****')
        str_list.append(f'Cache Size: {int(self.cache_size / 1024):>26} KB')
        str_list.append(f'Block Size: {self.block_size:>25} Bytes')
        str_list.append(f'Associativity: {self.associativity:>21}')
        str_list.append(f'Replacement Policy: {self.replacement_policy:>17}\n')
        str_list.append('***** Cache Calculated Values *****\n')
        str_list.append(f'Total # Blocks: {self.number_blocks:>24}')
        str_list.append(f'Tag Size: {self.tag_bits:>27} bits')
        str_list.append(f'Index Size: {self.index_bits:>25} bits')
        str_list.append(f'Total # Rows: {self.number_rows:>25}')
        str_list.append(f'Overhead Size: {self.overhead:>25} bytes')
        str_list.append(f'Implementation Memory Size: {self.total_size / 1024:>13.2f} KB ({self.total_size} bytes)')
        str_list.append(f'Cost: {f"${round(self.total_size / 1024 * 0.09, 2):.2f} @ ($0.09 / KB)":>50}')
        return '\n'.join(str_list)
