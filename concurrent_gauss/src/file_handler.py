from __future__ import annotations
from typing import TYPE_CHECKING

import numpy as np

if TYPE_CHECKING:
    from pathlib import Path

    from numpy.typing import NDArray


def read_file(path: Path) -> tuple[NDArray, NDArray]:
    data = np.loadtxt(path, skiprows=1)
    A, b = data[:-1, :], data[-1, :]
    b = b.reshape(-1, 1)
    return A, b


def write_file(path: Path, A: NDArray, b: NDArray) -> None:
    b = b.reshape(1, -1)
    data = np.vstack((A, b))
    np.savetxt(path, data, comments="", header=f"{A.shape[0]}", fmt="%.10g")
