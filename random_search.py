"""Baseline: случайный поиск с тем же бюджетом вычислений.

На каждой "итерации" генерируется P случайных точек и оценивается f.
Это позволяет сравнить ГА со случайным тыком при одинаковом числе
обращений к фитнес-функции.
"""
import numpy as np


def random_search(cfg, seed, fitness_fn, dim, lower, upper):
    rng = np.random.default_rng(seed)
    P = cfg['pop_size']
    budget = cfg['budget']

    n_evals = 0
    best_f = float('inf')
    best_x = None

    history = [(0, best_f)]

    generation = 0
    while n_evals < budget:
        generation += 1
        pop = rng.uniform(lower, upper, size=(P, dim))
        vals = np.asarray(fitness_fn(pop), dtype=float)
        n_evals += P

        idx = int(np.argmin(vals))
        if vals[idx] < best_f:
            best_f = float(vals[idx])
            best_x = pop[idx].copy()

        history.append((generation, best_f))

    return {
        'best_x': best_x,
        'best_f': best_f,
        'history': history,
        'n_evals': n_evals,
    }