import math

import numpy as np

quantization_matrices = {
    8: np.array([
        [16, 11, 10, 16, 24, 40, 51, 61],
        [12, 12, 14, 19, 26, 58, 60, 55],
        [14, 13, 16, 24, 40, 57, 69, 56],
        [14, 17, 22, 29, 51, 87, 80, 62],
        [18, 22, 37, 56, 68, 109, 103, 77],
        [24, 35, 55, 64, 81, 104, 113, 92],
        [49, 64, 78, 87, 103, 121, 120, 101],
        [72, 92, 95, 98, 112, 100, 103, 99]
    ]),
    16: np.block([[np.ones((8, 8)), np.zeros((8, 8))], [np.zeros((8, 16))]]),
    32: np.block([[np.ones((16, 16)), np.zeros((16, 16))], [np.zeros((16, 32))]])
}


def __normalize_to_zero(matrix: np.ndarray) -> np.ndarray:
    """Normalize YCrCb values- remove 128 from each object

    Arguments:
        submatrix {ndarray} -- 8*8 Submatrix

    Returns:
        ndarray -- 8*8 normalized submatrix
    """
    return matrix - 128


def __un_normalize(matrix: np.ndarray):
    return matrix + 128


def __cos_element(x, u):
    return math.cos((2 * x + 1) * u * math.pi / 16)


def __alpha(u):
    return 1 / math.sqrt(2) if u == 0 else 1


def __G_uv(u, v, matrix):
    return (1 / 4) * __alpha(u) * __alpha(v) * sum(
        matrix[x][y] * __cos_element(x, u) * __cos_element(y, v)
        for x in range(len(matrix))
        for y in range(len(matrix[0])))


def __discrete_cosine_transform(matrix: np.ndarray) -> np.ndarray:
    return np.array([[__G_uv(y, x, matrix)
                      for x in range(len(matrix[y]))]
                     for y in range(len(matrix))])


def __invert_discrete_cosine_transform(matrix: np.ndarray):
    return np.array([[__f_xy(x, y, matrix)
                      for x in range(len(matrix[y]))]
                     for y in range(len(matrix))])


def __f_xy(x, y, matrix):
    return round(
        0.25 *
        sum(
            __alpha(u) * __alpha(v) * matrix[v][u] *
            __cos_element(x, u) * __cos_element(y, v)
            for u in range(len(matrix[0]))
            for v in range(len(matrix)))
    )


def quantization(submatrix: np.ndarray) -> np.ndarray:
    return np.array([[round(submatrix[row, col] / quantization_matrices[submatrix.shape[0]][row, col])
                      for col in range(len(submatrix[row]))]
                     for row in range(len(submatrix))])


def un_quantization(matrix: np.ndarray) -> np.ndarray:
    return np.array([[matrix[row, col] * quantization_matrices[matrix.shape[0]][row, col]
                      for col in range(len(matrix[row]))]
                     for row in range(len(matrix))])


def DCT(matrix: np.ndarray) -> np.ndarray:
    return __discrete_cosine_transform(__normalize_to_zero(matrix))


def inverse_DCT(matrix):
    return __un_normalize(__invert_discrete_cosine_transform(matrix))
