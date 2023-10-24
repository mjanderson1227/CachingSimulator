#!/bin/python3

from argparse import ArgumentParser 
from cache_builder import CacheBuilder

# Create a new ArgumentParser to parse the command line arguments.
parse = ArgumentParser(
        prog='Sim.exe',
        description='A caching simulator with configurable cache parameters.')

# Add command line arguments for parsing.
parse.add_argument('-f', '--file', action='append')
parse.add_argument('-s', '--cache-size')
parse.add_argument('-b', '--block-size')
parse.add_argument('-a', '--associativity')
parse.add_argument('-r', '--replacement-algorithm')
parse.add_argument('-p', '--physical-memory')

# Parse command line arguments.
args = parse.parse_args()

# Create a cachebuilder to store and calculate the values needed for the cache.
cache_builder = CacheBuilder(
        args.file,
        int(args.cache_size),
        int(args.block_size),
        int(args.associativity),
        args.replacement_algorithm,
        int(args.physical_memory))

# Print the cache information.
cache_builder.print_info()
