#ifndef CACHE_ROW_H
#define CACHE_ROW_H
#include <cstddef>
#include <deque>
#include <map>
#include <string>
#include <vector>

// Represent each block as a struct.
struct cache_block
{
    // Vector that represents a stream of data.
    std::vector<std::byte> data;
    bool dirty;
};

/* Will represent a specific row in the overall cache.  Most importantly it contains a hash table that manages the
 respective blocks mapping them by tags.*/
class cache_row
{
  private:
    // The number of blocks in each cache row.
    int associativity;

    // Keep a deque for storing all the most recently used values.
    std::deque<std::string> recent_used_values;

    /* Hash Map that maps the tag to a vector of n bytes where n is the offset for each block.
     Since we are using a map a valid bit is not needed. */
    std::map<std::string, cache_block> blocks;

  public:
    // Constructor that uses associativity as the size of a new vector.
    cache_row(int associativity);

    // Check if the row has the given tag
    bool is_valid(std::string tag);

    // Check if the memory inside the block has been written to.
    bool is_dirty(std::string tag);

    // Check if the row is full.
    bool is_full();

    // Get a reference to the data at one of the blocks depending on the tag.
    cache_block& get_block(std::string tag);

    // Replace a block in the cache
    void replace(std::string tag, cache_block data);

    // Add a new block to the with the tag as the key.
    void add_block(std::string tag, cache_block data);
};
#endif
