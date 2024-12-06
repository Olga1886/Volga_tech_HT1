import numpy as np

#Задача 1. Create a random vector of size N and find the mean value

def rand_mean(N: int) -> float:
    random_vector = np.random.rand(N)
    mean_value = np.mean(random_vector)
    return mean_value

mean_value_of_array_size_10 = rand_mean(10)
print(f"Mean value of random array of size 10: {mean_value_of_array_size_10}")

#Задача 2. Create a 8x8 matrix and fill it with a checkerboard pattern

def print_checkerboard():
    checkerboard = np.zeros((8, 8), dtype=int)
    checkerboard[1::2, ::2] = 1
    checkerboard[::2, 1::2] = 1


    for row in checkerboard:
        print(' '.join(map(str, row)))


print("Checkerboard pattern:")
print_checkerboard()

#Задача 3. Print the minimum and maximum representable value for each numpy scalar type

def min_max_repr():

    print("NumPy Scalar Types Min and Max Values:")

    for dtype in [np.int8, np.int16, np.int32, np.int64]:
        min_val = np.iinfo(dtype).min
        max_val = np.iinfo(dtype).max
        print(f"{dtype.__name__}: Min = {min_val}, Max = {max_val}")


    for dtype in [np.float32, np.float64]:
        min_val = np.finfo(dtype).min
        max_val = np.finfo(dtype).max
        print(f"{dtype.__name__}: Min = {min_val}, Max = {max_val}")


min_max_repr()

#Задача 4. How to get the n largest values of an array?

def n_largest(n: int) -> np.ndarray:
    A = np.arange(10000)
    np.random.shuffle(A)
    indices = np.argpartition(A, -n)[-n:]
    largest_values = A[indices]
    largest_values.sort()
    return largest_values

result = n_largest(5)
print(f"The 5 largest values are: {result}")

# Пример:
print(n_largest(5))


#Задача 5. How to compute ((A+B)*(-A/2)) in place (without copy)?
# выдает ошибку при запуске:
#   File "C:\Users\Lenovo\PycharmProjects\Volga_tech_HT1\HW3\HW3_task2.py", line 68, in <module>
#     from memory_profiler import memory_usage
# ModuleNotFoundError: No module named 'memory_profiler'
# пыталась установить пакет pip uninstall memory_profiler - выдает еще больше ошибок. Не могу понять, как исправить.

import numpy as np
from memory_profiler import memory_usage

def compute_in_place():

    A = np.ones(3)  # Initialize A and B directly
    B = np.ones(3)*2

    np.add(A, B, out=B)

    np.divide(A, 2, out=A)

    np.negative(A, out=A)

    np.multiply(A, B, out=A)
    return A

def compute_in_place_better():

    A = np.ones(3)
    B = np.ones(3)*2

    np.add(A, B, out=B)
    np.divide(A, -2, out=A)
    np.multiply(A, B, out=A)

    return A


def compute_not_in_place():
    A = np.ones(3)
    B = np.ones(3)*2
    C = (A+B)*(-A/2)
    return C

# Measure memory usage
mem_usage_inplace = memory_usage((compute_in_place, ()))
print(f"Memory usage (compute_in_place): {mem_usage_inplace}")

mem_usage_inplace_better = memory_usage((compute_in_place_better, ()))
print(f"Memory usage (compute_in_place_better): {mem_usage_inplace_better}")

mem_usage_notinplace = memory_usage((compute_not_in_place, ()))
print(f"Memory usage (compute_not_inplace): {mem_usage_notinplace}")