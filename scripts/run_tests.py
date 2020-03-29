import base64
import subprocess
import sys

def encode_seed(seed: int, length: int):
    binarystr = seed.to_bytes(length, 'big', signed=False)
    return base64.b64encode(binarystr)

def decode_seed(b64str: str):
    binarystr = base64.b64decode(b64str)
    return int.from_bytes(binarystr, 'big', signed=False)

########################################
#   Argument Parsing                   #
########################################

if len(sys.argv) > 1:
    start_seed = decode_seed(sys.argv[1])
else:
    start_seed = 0

########################################
#   Logic                              #
########################################

def seeds(start_seed):
    seed = start_seed
    length = 1
    while True:
        try:
            while True:
                yield encode_seed(seed, length)
                seed += 1
        except OverflowError:
            length += 1

print("Running tests ad infinitum. Press ctrl+C to quit.")

for seed in seeds(start_seed):
    print("seed: ", seed)
    subprocess.run(["sh", "scripts/generate_test.sh", seed], check=True)
    subprocess.run(["./generated/test"], check=True)
