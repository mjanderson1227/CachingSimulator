from argparse import ArgumentParser
from cache_builder import CacheBuilder
from cache import Cache
from address import Address

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
def simulate_fetch(address: int, length: int): 
    addr = Address(address, cache_builder)
    cache.access(addr, length, "I")
    
# Assume all data accesses are 4 bytes. 
def simulate_data(dst: int, src: int):
    LENGTH = 4
    if src:
        addr_src = Address(src, cache_builder)
        cache.access(addr_src, LENGTH, "D")
    if dst:
        addr_dst = Address(dst, cache_builder)
        cache.access(addr_dst, LENGTH, "D")

# Parse the trace files.
for trace_file in cache_builder.trace_files:
    with open(trace_file, 'r') as input_file:
        for line in input_file:
            splitline = list(filter(lambda token: token != '', line.split(' ')))
            identifier = splitline[0][0:3]
            if identifier == 'EIP':
                length = int(splitline[1][1:3])
                address = int(splitline[2], 16)
                simulate_fetch(address, length)
            elif identifier == 'dst':
                dst = int(splitline[1], 16)
                src = int(splitline[4], 16)
                simulate_data(dst, src)

# Print the cache data.
print(cache)
