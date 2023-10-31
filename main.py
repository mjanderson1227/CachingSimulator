#!/bin/python3

from argparse import ArgumentParser 
from cache_builder import CacheBuilder

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
cache_builder.print_info()
