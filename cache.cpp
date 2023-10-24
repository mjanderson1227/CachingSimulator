#include "cache.hpp"
#include "address.hpp"
#include "cache_row.hpp"
#include <algorithm>
#include <string>
#include <vector>

// Constructor
cache::cache(int associativity, int num_rows, int block_size)
    : associativity(associativity), block_size(block_size), rows(num_rows)
{
    std::for_each(this->rows.begin(), this->rows.end(),
                  /* Lambda to call for each cache row. Captures the value of associativity as a variable to use in the
                  construction of the inner class.*/
                  [associativity](cache_row row) { row = cache_row(associativity); });
}

std::vector<std::byte> cache::read_from(address address, int num_bytes) const
{
    // Create a new vector to return with the bytes.
    std::vector<std::byte> data = std::vector<std::byte>();

    // Get the tag bit.
    std::string tag_bit = address.get_tag();
    int index = address.get_index();
    int offset = address.get_offset();

    // Get the desired row.
    cache_row desired_row = this->rows.at(offset);

    // Conflict Miss - The number of blocks currently filled is full, so a block must be replaced.
    if (!desired_row.is_valid(tag_bit) && desired_row.is_full())
    {
        // TODO: Remove an index in the cache and read main memory into the block.
    }
    // Compulsory Miss - The tag does not already exist in the cache.
    else if (desired_row.is_valid(tag_bit))
    {
        // TODO: read from main memory.  And fill the next empty space.
    }
    // Hit - Get the number of bytes needed from the cache.
    else
    {
        cache_block block = desired_row.get_block(tag_bit);
        std::vector<std::byte> block_data = block.data;
        // Copy n bytes of data from the block into the data vector.
        std::copy(block_data.begin(), block_data.begin() + num_bytes, data);
    }

    // Data will be a conceptual vector block of data for the program to use.
    return data;
}
