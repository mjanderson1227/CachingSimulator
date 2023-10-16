#ifndef CACHE_H
#define CACHE_H
#include "address.hpp"
#include "cache_row.hpp"
#include <cstddef>
#include <string>
#include <vector>

class cache
{
  private:
    std::vector<cache_row> rows;
    int associativity;
    int block_size;

  public:
    cache(int associativity, int num_rows, int block_size);
    std::vector<std::byte> read_from(address address, int num_bytes) const;
    // TODO: Write to method.
};
#endif
