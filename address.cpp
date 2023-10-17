#include "address.hpp"
#include <string>

// Constructor
address::address(std::string full_address, int tag_size, int index_size, int offset_size)
    : tag(full_address.substr(0, tag_size)), index(stoi(full_address.substr(tag_size, tag_size + index_size))),
      offset(stoi(full_address.substr(tag_size + index_size, full_address.length())))
{
}

std::string address::get_tag()
{
    return this->tag;
}

int address::get_index()
{
    return this->index;
}

int address::get_offset()
{
    return this->offset;
}
