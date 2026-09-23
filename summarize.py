"""Описательная статистика по сериям запусков.

Читает results/*_summary.csv и выдаёт таблицу:
    серия | best | mean | median | std | worst

Сохраняет:
    results/report_summary.csv   — машиночитаемая версия (для отчёта и проверки)
    results/report_summary.md    — Markdown-таблица, готовая к вставке в отчёт
"""
import csv
from pathlib import Path

import numpy as np


SERIES = [
    ('A (p_m=0.1)',    'ga_A_summary.csv'),
    ('B (p_m=0.3)',    'ga_B_summary.csv'),
    ('random search',  'random_summary.csv'),
]


def load_best_f(path):
    with open(path) as f:
        return np.array([float(row['best_f']) for row in csv.DictReader(f)])


def main():
    results = Path('results')

    rows = []
    for name, file in SERIES:
        values = load_best_f(results / file)
        rows.append({
            'series': name,
            'best':   float(values.min()),
            'mean':   float(values.mean()),
            'median': float(np.median(values)),
            'std':    float(values.std(ddof=1)),  # выборочное ст. отклонение
            'worst':  float(values.max()),
        })

    # --- CSV ---
    csv_path = results / 'report_summary.csv'
    with open(csv_path, 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print(f'Сохранено: {csv_path}')

    # --- Markdown ---
    md_path = results / 'report_summary.md'
    with open(md_path, 'w') as f:
        header = '| Серия | best | mean | median | std | worst |'
        sep    = '|---|---|---|---|---|---|'
        f.write(header + '\n' + sep + '\n')
        for r in rows:
            f.write(
                f'| {r["series"]} '
                f'| {r["best"]:.3e} '
                f'| {r["mean"]:.3e} '
                f'| {r["median"]:.3e} '
                f'| {r["std"]:.3e} '
                f'| {r["worst"]:.3e} |\n'
            )
    print(f'Сохранено: {md_path}')

    # --- Красивый вывод в консоль ---
    print()
    print(f'{"Серия":<16} {"best":>12} {"mean":>12} {"median":>12} {"std":>12} {"worst":>12}')
    print('-' * 82)
    for r in rows:
        print(f'{r["series"]:<16} '
              f'{r["best"]:>12.3e} {r["mean"]:>12.3e} '
              f'{r["median"]:>12.3e} {r["std"]:>12.3e} '
              f'{r["worst"]:>12.3e}')


if __name__ == '__main__':
    main()