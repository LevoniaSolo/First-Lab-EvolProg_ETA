# ЛР № 1 — ГА для многомерной оптимизации (V=17)

## Задача

Минимизировать

    f(x) = sum_{i=1..10} |x_i|^(2 + 4(i-1)/9),   x_i in [-1, 1].

Глобальный минимум: f(0,...,0) = 0.

## Установка зависимостей

Debian/Ubuntu:

    sudo apt update
    sudo apt install python3-numpy python3-matplotlib

## Запуск

    python3 main.py --stage all

Скрипт:
1) прогоняет 20 запусков ГА в конфигурации A, 20 в конфигурации B и 20 запусков random search;
2) сохраняет CSV в `results/`;
3) строит графики и сохраняет `results/report_histogram.png` и `results/report_convergence.png`.

## Структура

- `functions.py` — целевая функция V=17.
- `configs.py` — параметры конфигураций A и B, список seed'ов.
- `ga.py` — реализация ГА (турнир, арифметический кроссовер, гауссовская мутация, элитизм).
- `random_search.py` — baseline.
- `experiments.py` — прогон серий.
- `plots.py` — визуализация.
- `main.py` — CLI.
- `summarize.py` - статистика.

## Конфигурации

| Параметр        | A       | B       |
|-----------------|---------|---------|
| pop_size        | 100     | 100     |
| p_c             | 0.9     | 0.9     |
| p_m             | 0.1     | 0.3     |
| sigma           | 0.1     | 0.1     |
| tournament_k    | 3       | 3       |
| elitism         | 2       | 2       |
| budget (f-eval) | 50 000  | 50 000  |

Отличие B от A — **только** вероятность мутации p_m.

## Воспроизводимость

Все запуски используют seed из `configs.SEEDS` (1..20). Изменив список,
можно повторить или расширить серию.