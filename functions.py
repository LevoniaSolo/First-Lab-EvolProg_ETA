"""Целевая функция варианта V=17: 'функция различных степеней'.

f(x) = sum_{i=1..d} |x_i|^(2 + 4*(i-1)/(d-1))
x_i in [-1, 1], d = 10.
Глобальный минимум: f(0,...,0) = 0.
"""
import numpy as np

DIM = 10
LOWER = -1.0
UPPER = 1.0


def f_variant17(x):
    """Векторизованная фитнес-функция.

    Принимает массив формы (d,) или (P, d).
    Возвращает скаляр или массив формы (P,).
    """
    x = np.asarray(x, dtype=float)
    d = x.shape[-1]
    exponents = 2.0 + 4.0 * np.arange(d) / (d - 1)
    return np.sum(np.abs(x) ** exponents, axis=-1)