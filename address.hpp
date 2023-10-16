#ifndef ADDRESS_H
#define ADDRESS_H
#include <string>
class address
{
  private:
    std::string tag;
    int index;
    int offset;

  public:
    address(std::string full_address, int tag_size, int index_size, int offset_size);
    std::string get_tag();
    int get_index();
    int get_offset();
};
#endif // !DEBUG
