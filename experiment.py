from os import system
from time import time

startup_times = []

for _ in range(1_000):
    start_time = time()
    system("python3 editor.py")

    startup_times.append(time() - start_time)

print("mean:", sum(startup_times) / len(startup_times))
