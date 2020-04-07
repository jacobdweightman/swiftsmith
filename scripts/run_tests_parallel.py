import base64
from concurrent.futures import ThreadPoolExecutor
import os
from queue import Queue
import random
import signal
import subprocess
import sys
from threading import Lock, Semaphore

# The maximum number of processes to use.
process_count = os.cpu_count()

class Counter(object):
    """A threadsafe counter to keep track of the number of tests that have run"""
    def __init__(self):
        self._lock = Lock()
        self.value = 0
    
    def increment(self):
        with self._lock:
            self.value += 1

# The number of tests that have been run
counter = Counter()

# I'm sure there's a better way to do this. We need to maintain a lock for each
# `generated{i}` directory so that one subprocess doesn't overwrite code that another
# process is compiling. The thread that kicks off the subprocess may aquire a lock by
# getting the next directory in line, and is then responsible for releasing it by
# putting it back in the queue.
working_dirs = Queue(maxsize=process_count)
for i in range(process_count):
    working_dirs.put(i, block=False)

def seeds():
    seed_seed = os.urandom(64)
    random.seed(seed_seed)
    while True:
        seed = random.getrandbits(256).to_bytes(32, 'big')
        yield base64.b64encode(seed)

def unit(queue: Queue):
    # Ensure that child threads do not catch ctrl+C
    signal.pthread_sigmask(signal.SIG_BLOCK, {signal.SIGINT})

    # aquire lock
    dir_number = working_dirs.get(block=True)
    seed = queue.get(block=True)
    result = subprocess.run([
        "sh", "scripts/run_test.sh", f"generated{dir_number}", seed],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    # release lock
    working_dirs.put(dir_number)
    counter.increment()
    print("counter:", counter.value, "\tseed:", seed)
    if result.stdout:
        print("[stdout]\n", result.stdout.decode("utf-8"))
    if result.stderr:
        print("[stderr]\n", result.stderr.decode("utf-8"))
    return result.returncode

if __name__ == '__main__':
    queue = Queue(maxsize=1)
    seed = seeds()
    with ThreadPoolExecutor(max_workers=4) as executor:
        try:
            while True:
                queue.put(next(seed), block=True)
                f = executor.submit(unit, queue)
        except KeyboardInterrupt:
            pass
