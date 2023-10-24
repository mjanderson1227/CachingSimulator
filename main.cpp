#include <cstdio>
#include <cstring>
#include <iostream>
#include <map>
#include <set>
#include <string>
#include <vector>

// Helper to tokenize a string into a vector.
/*std::vector<std::string> tokenize_commas(char* str)
{
    std::vector<std::string> split_strings;
    char* current_index = str;

    std::string* valid_characters = new std::string("");

    while (*current_index != '\0')
    {
        if (*current_index == ',')
        {
            split_strings.push_back(*valid_characters);
            valid_characters = new std::string("");
        }
        else
        {
            valid_characters->push_back(*current_index);
        }
        current_index++;
    }

    split_strings.push_back(*valid_characters);

    return split_strings;
}*/

void add_file(char* filename, std::vector<std::FILE*>& file_list)
{
    std::FILE* new_file = fopen(filename, "r");
    file_list.push_back(new_file);
}

int main(int argc, char* argv[])
{
    std::vector<std::FILE*> file_list;
    int cache_size;
    std::map<std::string, void*> flag_pool = {
        {"-f", add_file}, {"-s", [cache_size](int size) {cache_size = size; }}, {"-b"}, {"-a"}, {"-r"}, {"-p"}};

    if (argc == 1)
    {
        std::cout << "Error not enough flags provided." << std::endl;
        return 1;
    }

    for (int i = 1; i < argc; i++)
    {
    }
    return 0;
}
