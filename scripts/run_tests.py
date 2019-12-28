import subprocess
import itertools

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
    subprocess.call(["sh", "scripts/generate_test.sh", seed])
