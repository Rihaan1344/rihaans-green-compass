# /// benchmark_test
# requires-python = ">=X.XX" TODO: Update this to the minimum Python version you want to support
# dependencies = [
#   TODO: Add any dependencies your script requires
# ]
# ///

# TODO: Update the main function to your needs or remove it.

import time
import matplotlib.pyplot as plt

#case 1: increasing value of pre defined variable; so memory address of same variable changes

case_1_times = []

for i in range (15):
    start = time.perf_counter()
    num = 0
    for i in range(10 **7):
        num = i
    end = time.perf_counter()
    case_1_times.append(end - start)

x1 = []
y1= []

for iteration_num, time_taken in enumerate(case_1_times, start=1):
    x1.append(iteration_num)
    y1.append(time_taken)

plt.plot(x1, y1, marker='o')
plt.title('Time taken for case 1')  
plt.xlabel('Iteration Number')
plt.ylabel('Time (seconds)')
plt.grid()

#case 2: creating a new variable on every iteration

case_2_times = []

for i in range (15):
    start = time.perf_counter()
    for i in range(10 **7):
        num = i
    end = time.perf_counter()
    case_2_times.append(end - start)

x2 = []
y2 = []

for iteration_num, time_taken in enumerate(case_2_times, start=1):
    x2.append(iteration_num)
    y2.append(time_taken)

plt.plot(x2, y2, marker='o')
plt.title('Time taken for case 2')  
plt.xlabel('Iteration Number')
plt.ylabel('Time (seconds)')

plt.grid()
plt.show()
