from argparse import ArgumentParser
from concurrent.futures import ThreadPoolExecutor, as_completed
from itertools import product
from contextlib import ExitStack
import json
from glob import glob
import subprocess
import re

# Parse Arguments.
parser = ArgumentParser(
        prog='tester.exe',
        description='Tester for the caching simulator.')

parser.add_argument('-e', '--executable', required=True)
parser.add_argument('-t', '--tracefile-folder', required=True)
parser.add_argument('-p', '--parameter-file', required=True)

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

def create_line(cmd: list[str]):
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

    # Return the line back to the tasks
    return result.to_csv() + "\n"

# Get the exe file
executable = arguments.executable
trace_files = arguments.tracefile_folder
params = arguments.parameter_file

CSV_FILE_NAME = "results.csv"
with ExitStack() as context:
    # Add each of the conditions for easy cleanup.
    param_file = context.enter_context(open(params, "r"))
    csv = context.enter_context(open(CSV_FILE_NAME, "w"))
    executor_service = context.enter_context(ThreadPoolExecutor())

    # Parse the json
    json_object = json.load(param_file)
    if json_object == None:
        print("Unable to parse json file")
        exit()

    cache_sizes = json_object["cacheSize"]
    associativities = json_object["associativity"]
    block_sizes = json_object["blockSize"]
    filenames = glob(f"{trace_files}/*.trc")
    tasks_to_execute = []

    # Generate all combinations of the cache parameters.
    for file, cs, assoc, bs in product(filenames, cache_sizes, associativities, block_sizes):
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
        tasks_to_execute.append(executor_service.submit(create_line, cmd))

    csv.writelines(map(lambda future: future.result(), as_completed(tasks_to_execute)))
