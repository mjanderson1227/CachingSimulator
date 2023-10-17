#include "cache_row.hpp"
#include <algorithm>
#include <cstdlib>
#include <map>
#include <string>
#include <vector>

// Constructor
cache_row::cache_row(int associativity) : associativity(associativity), blocks(), recent_used_values()
{
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

void cache_row::replace(std::string tag, cache_block data)
{
    this->blocks.erase(this->recent_used_values.back());
    this->recent_used_values.pop_back();
    this->recent_used_values.push_front(tag);
    this->blocks.emplace(tag, data);
}

void cache_row::add_block(std::string tag, cache_block data)
{
    this->recent_used_values.push_front(tag);
    this->blocks.emplace(tag, data);
}
