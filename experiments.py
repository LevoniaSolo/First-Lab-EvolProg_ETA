"""Проведение серий экспериментов:
   - Конфигурация A: 20 запусков ГА;
   - Конфигурация B: 20 запусков ГА;
   - Random search: 20 запусков с тем же бюджетом.

Результаты сохраняются в results/ в виде CSV:
   - <name>_summary.csv   — итоговое f, число вызовов f, seed
   - <name>_histories.csv — best-so-far по поколениям для каждого запуска
"""
import csv
from pathlib import Path

from configs import CONFIGS, SEEDS
from functions import f_variant17, DIM, LOWER, UPPER
from ga import GA
from random_search import random_search

RESULTS_DIR = Path('results')


def _save_summary(path, rows):
    with open(path, 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)


def _save_histories(path, histories):
    max_len = max(len(h) for h in histories)
    with open(path, 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['generation'] + [f'run_{i+1}' for i in range(len(histories))])
        for g in range(max_len):
            row = [g]
            for h in histories:
                row.append(h[g][1] if g < len(h) else '')
            w.writerow(row)


def run_series():
    RESULTS_DIR.mkdir(exist_ok=True)

    # --- ГА, конфигурации A и B ---
    for name, cfg in CONFIGS.items():
        print(f'[GA {name}] p_m={cfg["p_m"]}, P={cfg["pop_size"]}, budget={cfg["budget"]}')
        rows, histories = [], []
        for seed in SEEDS:
            ga = GA(cfg, seed=seed, fitness_fn=f_variant17,
                    dim=DIM, lower=LOWER, upper=UPPER)
            res = ga.run()
            rows.append({'seed': seed,
                         'best_f': res['best_f'],
                         'n_evals': res['n_evals']})
            histories.append(res['history'])
            print(f'  seed={seed:>2}  best_f={res["best_f"]:.6e}')
        _save_summary(RESULTS_DIR / f'ga_{name}_summary.csv', rows)
        _save_histories(RESULTS_DIR / f'ga_{name}_histories.csv', histories)

    # --- Random search как baseline ---
    print('[Random search] тот же бюджет')
    rows, histories = [], []
    for seed in SEEDS:
        res = random_search(CONFIGS['A'], seed=seed, fitness_fn=f_variant17,
                            dim=DIM, lower=LOWER, upper=UPPER)
        rows.append({'seed': seed,
                     'best_f': res['best_f'],
                     'n_evals': res['n_evals']})
        histories.append(res['history'])
        print(f'  seed={seed:>2}  best_f={res["best_f"]:.6e}')
    _save_summary(RESULTS_DIR / 'random_summary.csv', rows)
    _save_histories(RESULTS_DIR / 'random_histories.csv', histories)


if __name__ == '__main__':
    run_series()