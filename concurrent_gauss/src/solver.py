from __future__ import annotations
from typing import TYPE_CHECKING

import numpy as np

if TYPE_CHECKING:
    from numpy.typing import NDArray


def gaussian_elimination(A: NDArray, b: NDArray) -> tuple[NDArray, NDArray]:
    D = np.diag(np.ones(A.shape[0]))
    x = np.linalg.solve(A, b)
    return D, x
