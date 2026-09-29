from math import sqrt, log

SQRT_2 = sqrt(2)

def calculate_ucb(score: float, n: int, parent_n: int):
    if n == 0:
        return float("inf")

    avg = score / n
    optimism = SQRT_2 * sqrt(log(parent_n)) / sqrt(n)

    return avg + optimism
