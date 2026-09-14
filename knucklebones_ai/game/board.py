import numpy as np


class Board:
    def __init__(self, data: np.ndarray | None):
        # self._data[col, val] = counts of value val in column col (0 is empty)
        if data is None:
            self._data = np.zeros((3, 7), np.uint8)
        else:
            assert data.shape == (3, 7)
            assert data.dtype == np.uint8
            self._data = data

    def copy(self) -> Board:
        return Board(self._data.copy())

    def is_full(self) -> bool:
        return np.count_nonzero(self._data[:, 0]) == 0

    def is_col_available(self, col: int) -> bool:
        return self._data[col, 0] > 0

    def get_points(self) -> int:
        return sum(val * count ** 2 for col in self._data for val, count in enumerate(col))

    def place_die(self, col: int, val: int) -> Board:
        assert self.is_col_available(col)
        data = self._data.copy()
        data[col, 0] -= 1
        data[col, val] += 1
        return Board(data)

    def remove_dice(self, col: int, val: int) -> Board:
        data = self._data.copy()
        data[col, 0] += data[col, val]
        data[col, val] = 0
        return Board(data)
