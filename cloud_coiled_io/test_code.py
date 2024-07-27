import random


def estimate_pi_simple(n: int) -> float:
    total = 0
    for _ in range(n):
        x = random.random()
        y = random.random()
        if x**2 + y**2 < 1:
            total += 1
    return total / n * 4
