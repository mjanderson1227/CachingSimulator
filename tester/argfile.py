import json

with open('./settings.json', 'r') as file:
    json_file = json.load(file)

    if(len(json_file["trace_files"]) > 3 ):
        exit(1)

    to_print = str(len(json_file["trace_files"])) + ' '
    file_list = json_file["trace_files"]
    to_print += ' '.join([x for x in file_list]) + ' '

    names = ["cache_size", "block_size", "associativity", "replacement_policy", "physical_size"]
    for i, name in enumerate(names):
        to_print += str(json_file[name]) + " " if i != len(names) - 1 else str(json_file[name])

    print(to_print)
