"""Построение графиков по результатам experiments.py.

Готовит два файла:
    results/report_convergence.png  — сходимость (mean ± [min, max]) по 20 запускам;
    results/report_histogram.png    — распределение финальных f по 20 запускам,
                                      по одной панели на серию с линейной осью X.
"""
import csv
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt


def load_histories(path):
    """Возвращает список: histories[run] = [best-so-far по поколениям]."""
    with open(path) as f:
        r = csv.reader(f)
        next(r)  # header
        columns = []
        for row in r:
            columns.append(row[1:])
    n_runs = len(columns[0]) if columns else 0
    runs = [[] for _ in range(n_runs)]
    for row in columns:
        for i, val in enumerate(row):
            if val != '':
                runs[i].append(float(val))
    return runs


def load_summary(path):
    with open(path) as f:
        r = csv.DictReader(f)
        return [float(row['best_f']) for row in r]


SERIES = [
    ('A (p_m=0.1)',    'ga_A_histories.csv',   'ga_A_summary.csv'),
    ('B (p_m=0.3)',    'ga_B_histories.csv',   'ga_B_summary.csv'),
    ('random search',  'random_histories.csv', 'random_summary.csv'),
]


def plot_convergence(ax, histories, label):
    min_len = min(len(h) for h in histories)
    h = np.array([hi[:min_len] for hi in histories])
    mean = h.mean(axis=0)
    lo   = h.min(axis=0)
    hi_  = h.max(axis=0)
    x = np.arange(min_len)
    ax.plot(x, mean, label=label)
    ax.fill_between(x, lo, hi_, alpha=0.2)


def make_convergence_figure(results_dir):
    fig, ax = plt.subplots(figsize=(9, 5))
    for name, hist_file, _ in SERIES:
        plot_convergence(ax, load_histories(results_dir / hist_file), name)

    ax.set_xlabel('Поколение')
    ax.set_ylabel('best-so-far f(x)')
    ax.set_yscale('log')
    ax.set_title('Сходимость ГА: среднее и [min, max] по 20 запускам')
    ax.legend()
    ax.grid(True, which='both', alpha=0.3)

    fig.tight_layout()
    out = results_dir / 'report_convergence.png'
    fig.savefig(out, dpi=150)
    plt.close(fig)
    print(f'Сохранено: {out}')


def make_histogram_figure(results_dir):
    fig, axes = plt.subplots(len(SERIES), 1, figsize=(9, 10))

    for ax, (name, _, sum_file) in zip(axes, SERIES):
        values = np.asarray(load_summary(results_dir / sum_file))
        ax.hist(values, bins=10, color='tab:blue', alpha=0.75,
                edgecolor='black', linewidth=0.5)
        ax.set_title(f'Распределение финального f — {name} '
                     f'(min={values.min():.2e}, max={values.max():.2e})')
        ax.set_xlabel('f')
        ax.set_ylabel('Число запусков')
        ax.grid(True, alpha=0.3)

    fig.tight_layout()
    out = results_dir / 'report_histogram.png'
    fig.savefig(out, dpi=150)
    plt.close(fig)
    print(f'Сохранено: {out}')


def main():
    results = Path('results')
    make_convergence_figure(results)
    make_histogram_figure(results)


if __name__ == '__main__':
    main()