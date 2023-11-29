from argparse import ArgumentParser
from io import TextIOWrapper
import json
from glob import glob
import subprocess
import re

# Parse Arguments.
parser = ArgumentParser(
        prog='tester.exe',
        description='Tester for the caching simulator.')

parser.add_argument('-e', '--executable')
parser.add_argument('-t', '--tracefile-folder')
parser.add_argument('-p', '--parameter-file')

arguments = parser.parse_args()

class CacheResults:
    accesses: str
    hits: str
    misses: str
    compulsory_misses: str
    conflict_misses: str
    hit_rate: str
    miss_rate: str
    cpi: str

    def __init__(self, matches: list[str]):
        self.accesses = matches[0]
        self.hits = matches[1]
        self.misses = matches[2]
        self.compulsory_misses = matches[3]
        self.conflict_misses = matches[4]
        self.hit_rate = matches[5]
        self.miss_rate = matches[6]
        self.cpi = matches[7]

    def to_csv(self):
        return f"{self.accesses},{self.hits},{self.misses},{self.compulsory_misses},{self.conflict_misses},{self.hit_rate},{self.miss_rate},{self.cpi}"


def handle_args(cmd: list[str], csv: TextIOWrapper):
    # Supply arguments from the automated file.
    ps = None

    try:
        # Run the program with the arguments.
        ps = subprocess.Popen(cmd, stdout=subprocess.PIPE, text=True)
    except subprocess.CalledProcessError as e:
        print("Error running process.", e)
        exit()

    return_code = ps.wait()

    if return_code != 0:
        print("Process did not exit successfully.")
        exit()

    # Collect output from the program.
    if (stream := ps.stdout) is not None:
        output = stream.read()
        sliced = output[output.find("Total Cache Accesses:"):]
        matches = re.findall(r"[0-9.]+", sliced)
        result = CacheResults(matches)
    else:
        print("No output from process.")
        exit()

    # Write values to csv file.
    csv.write(result.to_csv() + "\n")

# Get the exe file
executable = arguments.executable
trace_files = arguments.tracefile_folder
params = arguments.parameter_file

with open(params) as file, open("results.csv", "w") as csv:
    # Parse the json
    json_object = json.load(file)
    if json_object == None:
        print("Unable to parse json file")
        exit()

    cache_sizes = json_object["cacheSize"]
    associativities = json_object["associativity"]
    block_sizes = json_object["blockSize"]
    filenames = glob(f"{trace_files}/*.trc")

    for file in filenames:
        for cs in cache_sizes:
            for assoc in associativities:
                for bs in block_sizes:
                    cmd = ["python3",
                           f"{executable}",
                           "-f",
                           f"{file}",
                           "-s",
                           f"{cs}",
                           "-b",
                           f"{bs}",
                           "-a",
                           f"{assoc}",
                           "-r RND",
                           f"-p 4194304"]
                    print(' '.join(cmd))
                    handle_args(cmd, csv)
    csv.close()
