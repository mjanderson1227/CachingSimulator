from argparse import ArgumentParser
from dataclasses import dataclass 
from cache_builder import CacheBuilder
from cache import Address, Cache
from itertools import groupby

# Create a new ArgumentParser to parse the command line arguments.
parse = ArgumentParser(
        prog='Sim.exe',
        description='A caching simulator with configurable cache parameters.')

# Add command line arguments for parsing.
parse.add_argument('-f', '--file', action = 'append', required = True)
parse.add_argument('-s', '--cache-size', required = True, type = int)
parse.add_argument('-b', '--block-size', required = True, type = int)
parse.add_argument('-a', '--associativity', required = True, type = int)
parse.add_argument('-r', '--replacement-algorithm', required = True, type = str)
parse.add_argument('-p', '--physical-memory', required = True, type = int)

# Parse command line arguments.
args = parse.parse_args()

# Create a cachebuilder to store and calculate the values needed for the cache.
cache_builder = CacheBuilder(
        args.file,
        args.cache_size,
        args.block_size,
        args.associativity,
        args.replacement_algorithm,
        args.physical_memory)

# Print the cache information.
print(cache_builder)

# Create a new cache from the builder.
cache = Cache(cache_builder)

# Print the actual cache data.
# print(cache)

def simulate_fetch(address: int, length: int): 
    addr = Address(address, cache_builder)
    FILLED_VALUE = ["F"] * length
    cache.read_cache(addr, LIST_OF_ONES)
    
# TODO: Finish Defining this function
def simulate_data(dst: int, src: int):
    cache.read_cache(src, LIST_OF_ONES)
    FILLED_VALUE = ["F"] * length

@dataclass
class UnwrapResult:
    fetch: list[tuple]
    data: list[tuple]
def unwrap_group(grouped_values: groupby) -> UnwrapResult:
    filter_list = lambda li: list(filter(lambda x: x != '', li))
    fetch = []
    data = []
    for key, group in grouped_values:
        if key == '\n':
            continue

        for member in group:
            # Filter empty spaces from the list.
            split = filter_list(member.split(' '))
            if split[0] == 'EIP':
                length = int(split[1][1:3])
                address = int(split[2], 16)
                # print(f'({length}): {address}')
                fetch.append((address, length))
            elif split[0] == 'dstM':
                dst = int(split[1], 16)
                src = int(split[4], 16)
                # print(f'dst: {dst}  ::  src: {src}')
                data.append((dst, src))
    return UnwrapResult(fetch, data)

# Parse the trace files.
for trace_file in cache_builder.trace_files:
    with open(trace_file, 'r') as input_file:
        values = groupby(input_file, lambda x: x[0:4])
        result = unwrap_group(values)
        for item in result.fetch:
            simulate_fetch(*item)
        # for fetch, data in zip(result.fetch, result.data):
            # simulate_fetch()
