#include "cache_row.hpp"
#include <algorithm>
#include <map>
#include <string>
cache_row::cache_row(int associativity) : associativity(associativity), blocks()
{
    this->index_to_remove = std::map<std::string, cache_block>::iterator(this->blocks.begin());
}

bool cache_row::is_valid(std::string tag)
{
    return this->blocks.count(tag);
}

bool cache_row::is_dirty(std::string tag)
{
    return this->blocks[tag].dirty;
}

bool cache_row::is_full()
{
    return this->blocks.size() == this->associativity;
}

cache_block& cache_row::get_block(std::string tag)
{
    return this->blocks[tag];
}

void cache_row::replace(std::string tag)
{
    this->blocks.erase(index_to_remove->first);
    this->index_to_remove = this->blocks.begin();
    this->blocks[tag];
}

void cache_row::add_block()
{
}
