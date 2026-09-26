from math import sqrt, log

SQRT_2 = sqrt(2)

def calculate_ucb(avg: float, n: int, parent_n: int):
    if n == 0:
        return float("inf")

    return avg + SQRT_2 * sqrt(log(parent_n)) / sqrt(n)
