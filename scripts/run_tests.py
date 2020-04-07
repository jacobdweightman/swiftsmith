import base64
import logging
import os
import random
import subprocess
import sys

logging.basicConfig(filename="bug_candidates.txt", filemode='a', level=logging.DEBUG)

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
    result = subprocess.run(
        ["sh", "scripts/run_test.sh", "generated", seed],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    if result.stdout:
        logging.info("iteration: " + str(iteration) + "\tseed: " + str(seed))
        logging.info(result.stdout.decode("utf-8"))
        print(result.stdout.decode("utf-8"))
    if result.stderr:
        logging.info("iteration: " + str(iteration) + "\tseed: " + str(seed))
        logging.error(result.stderr.decode("utf-8"))
        print(result.stderr.decode("utf-8"))
    iteration += 1
