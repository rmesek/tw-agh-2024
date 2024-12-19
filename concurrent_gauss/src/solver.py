from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from typing import TYPE_CHECKING

import numpy as np

if TYPE_CHECKING:
    from numpy.typing import NDArray
    from concurrent.futures import Future


def gaussian_elimination(A: NDArray, b: NDArray) -> tuple[NDArray, NDArray]:
    # Indivisible tasks:
    #   A_i_k: m[k, i] = M[k, i] / M[i, i]
    #          (find the multiplier for subtracting i-th row from k-th row)
    #   B_i_j_k: n[k, i, j] = M[i, j] * m[k, i]
    #            (find the product of multiplier and i-th row element)
    #   C_i_j_k: M[k, j] = M[k, j] - n[k, i, j]
    #            (subtract the product from k-th row)
    # Foata normal form:
    #   FNF_N = [A_0_k][B_0_j_k][C_0_j_k]...[A_N-1_k][B_N-1_j_k][C_N-1_j_k]

    N = A.shape[0]
    M = np.hstack((A, b))
    # Is there a better way to remember the multipliers and products?
    m = np.zeros((N, N))
    n = np.zeros((N, N, N + 1))

    def task_A(i: int, k: int) -> None:
        print(f"A_{i}_{k} started")
        m[k, i] = M[k, i] / M[i, i]
        print(f"A_{i}_{k} done")

    def task_B(i: int, j: int, k: int) -> None:
        print(f"B_{i}_{j}_{k} started")
        n[k, i, j] = M[i, j] * m[k, i]
        print(f"B_{i}_{j}_{k} done")

    def task_C(i: int, j: int, k: int) -> None:
        print(f"C_{i}_{j}_{k} started")
        M[k, j] = M[k, j] - n[k, i, j]
        print(f"C_{i}_{j}_{k} done")

    with ThreadPoolExecutor(max_workers=None) as executor:
        for i in range(N - 1):
            # Task A
            features_A: list[Future] = []
            for k in range(i + 1, N):
                features_A.append(executor.submit(task_A, i, k))
            for feature in features_A:
                feature.result()

            # Task B
            features_B: list[Future] = []
            for j in range(i, N + 1):
                for k in range(i + 1, N):
                    features_B.append(executor.submit(task_B, i, j, k))
            for feature in features_B:
                feature.result()

            # Task C
            features_C: list[Future] = []
            for j in range(i, N + 1):
                for k in range(i + 1, N):
                    features_C.append(executor.submit(task_C, i, j, k))
            for feature in features_C:
                feature.result()

    # Back substitution
    for i in range(N - 1, -1, -1):
        for j in range(0, i):
            M[i, j] = 0.0
        for j in range(N - 1, i, -1):
            M[i, N] -= M[j, N] * M[i, j]
            M[i, j] = 0.0
        M[i, N] /= M[i, i]
        M[i, i] = 1.0

    return M[:, :-1], M[:, -1]
