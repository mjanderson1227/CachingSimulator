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
        # Use to format the string to be printed.
        FORMAT_OFFSET = 30
        format_string = lambda label, output: f'{label}: {"".join([" " for _ in range(FORMAT_OFFSET - len(label))])}{output}\n'

        return ''.join([
            'Cache Simulator - CS 3853 Fall 2023 - Group #06\n\n',
            f'Trace File(s): {", ".join(self.trace_files)}\n\n',
            '***** Cache Input Parameters *****\n\n',
            format_string('Cache Size', f'{int(self.cache_size / 1024)} KB'),
            format_string('Block Size', f'{self.block_size} Bytes'),
            format_string('Associativity', f'{self.associativity}'),
            format_string('Replacement Policy', f'{self.replacement_policy}'),
            '\n',
            '***** Cache Calculated Values *****\n\n',
            format_string('Total # Blocks', f'{self.number_blocks}'),
            format_string('Tag Size', f'{self.tag_bits} bits'),
            format_string('Index Size', f'{self.index_bits} bits'),
            format_string('Total # Rows', f'{self.number_rows}'),
            format_string('Overhead Size', f'{self.overhead} bytes'),
            format_string('Implementation Memory Size', f'{self.total_size / 1024:.2f} KB ({self.total_size} bytes)'),
            format_string('Cost', f'${round(self.total_size / 1024 * 0.09, 2):.2f} @ ($0.09 / KB)'),
        ])
