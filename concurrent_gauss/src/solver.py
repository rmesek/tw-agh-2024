from __future__ import annotations

import threading
from concurrent.futures import ThreadPoolExecutor
from typing import TYPE_CHECKING

import numpy as np

if TYPE_CHECKING:
    from numpy.typing import NDArray


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
        m[k, i] = M[k, i] / M[i, i]

    def task_B(i: int, j: int, k: int) -> None:
        n[k, i, j] = M[i, j] * m[k, i]

    def task_C(i: int, j: int, k: int) -> None:
        M[k, j] = M[k, j] - n[k, i, j]

    # For N = 3, the FNF is:
    # [A_0_1, A_0_2]
    # [B_0_0_1, B_0_1_1, B_0_2_1, B_0_3_1, B_0_0_2, B_0_1_2, B_0_2_2, B_0_3_2]
    # [C_0_0_1, C_0_1_1, C_0_2_1, C_0_3_1, C_0_0_2, C_0_1_2, C_0_2_2, C_0_3_2]
    # [A_1_2]
    # [B_1_1_2, B_1_2_2, B_1_3_2]
    # [C_1_1_2, C_1_2_2, C_1_3_2]

    for i in range(N - 1):
        # Task A
        for k in range(i + 1, N):
            print(f"A_{i}_{k}")
            task_A(i, k)

        # Task B
        for j in range(i, N + 1):
            for k in range(i + 1, N):
                print(f"B_{i}_{j}_{k}")
                task_B(i, j, k)

        # Task C
        for j in range(i, N + 1):
            for k in range(i + 1, N):
                print(f"C_{i}_{j}_{k}")
                task_C(i, j, k)

    return M[:, :-1], M[:, -1]
