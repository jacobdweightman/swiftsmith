import base64
import os
import random
import subprocess
import sys

def seeds():
    seed_seed = os.urandom(64)
    random.seed(seed_seed)
    while True:
        seed = random.getrandbits(256).to_bytes(32, 'big')
        yield base64.b64encode(seed)

print("Running tests ad infinitum. Press ctrl+C to quit.")

iteration = 0
for seed in seeds():
    print("iteration:", iteration, "\tseed: ", seed)
    subprocess.run(["sh", "scripts/generate_test.sh", seed], check=True)
    subprocess.run(["./generated/test"], check=True)
    iteration += 1
