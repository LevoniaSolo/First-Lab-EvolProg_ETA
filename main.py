"""Точка входа.

    python main.py --stage all          # эксперименты + графики
    python main.py --stage experiments  # только прогон серий
    python main.py --stage plots        # только графики
"""
import argparse

from experiments import run_series
from plots import main as make_plots


def cli():
    p = argparse.ArgumentParser()
    p.add_argument('--stage', choices=['experiments', 'plots', 'all'], default='all')
    args = p.parse_args()

    if args.stage in ('experiments', 'all'):
        run_series()
    if args.stage in ('plots', 'all'):
        make_plots()


if __name__ == '__main__':
    cli()