import itertools
import subprocess
import sys
import time

def seeds():
    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    length = 1
    while True:
        for seed in itertools.product(chars, repeat=length):
            yield ''.join(seed)
        length += 1

print("Running tests ad infinitum. Press ctrl+C to quit.")

for seed in seeds():
    print("seed: ", seed)
    proc = subprocess.Popen(["sh", "scripts/generate_test.sh", seed])
    try:
        while proc.poll() is None:
            time.sleep(0.1)
    except KeyboardInterrupt:
        proc.terminate()
        sys.exit(proc.returncode)
