"""Реализация генетического алгоритма для вещественной оптимизации.

Схема:
    1) инициализация популяции в допустимой области;
    2) оценка фитнес;
    3) турнирная селекция родителей;
    4) арифметический кроссовер;
    5) гауссовская мутация по генам;
    6) clamping границ;
    7) элитизм;
    8) повтор, пока не исчерпан бюджет вычислений.
"""
import numpy as np


class GA:
    def __init__(self, cfg, seed, fitness_fn, dim, lower, upper):
        self.cfg = cfg
        self.fitness_fn = fitness_fn
        self.dim = dim
        self.lower = lower
        self.upper = upper
        self.rng = np.random.default_rng(seed)
        self.n_evals = 0

    # --- базовые операции ---

    def _init_population(self):
        P = self.cfg['pop_size']
        return self.rng.uniform(self.lower, self.upper, size=(P, self.dim))

    def _evaluate(self, population):
        """Векторизованная оценка всей популяции. Считает вызовы f."""
        vals = self.fitness_fn(population)
        self.n_evals += len(population)
        return np.asarray(vals, dtype=float)

    def _tournament(self, fitness, k):
        """Турнирная селекция. Возвращает индексы P родителей."""
        P = len(fitness)
        idx = self.rng.integers(0, P, size=(P, k))
        winners = np.argmin(fitness[idx], axis=1)
        return idx[np.arange(P), winners]

    def _crossover(self, p1, p2, p_c):
        """Арифметический кроссовер. Один alpha на пару (простая версия)."""
        if self.rng.random() > p_c:
            return p1.copy(), p2.copy()
        alpha = self.rng.random()
        c1 = alpha * p1 + (1.0 - alpha) * p2
        c2 = (1.0 - alpha) * p1 + alpha * p2
        return c1, c2

    def _mutate(self, x, p_m, sigma):
        """Гауссовская мутация: каждый ген независимо с вероятностью p_m."""
        mask = self.rng.random(self.dim) < p_m
        noise = self.rng.normal(0.0, sigma, size=self.dim)
        return x + mask * noise

    def _clamp(self, x):
        return np.clip(x, self.lower, self.upper)

    # --- основной цикл ---

    def run(self):
        P = self.cfg['pop_size']
        budget = self.cfg['budget']
        elitism = self.cfg['elitism']

        population = self._init_population()
        fitness = self._evaluate(population)

        best_idx = int(np.argmin(fitness))
        best_x = population[best_idx].copy()
        best_f = float(fitness[best_idx])

        # история best-so-far: список (номер поколения, лучшее значение)
        history = [(0, best_f)]

        generation = 0
        while self.n_evals < budget:
            generation += 1

            # 1. Селекция
            parent_idx = self._tournament(fitness, self.cfg['tournament_k'])
            parents = population[parent_idx]

            # 2. Кроссовер + мутация -> потомки
            offspring = np.empty_like(population)
            for i in range(0, P - 1, 2):
                c1, c2 = self._crossover(parents[i], parents[i + 1], self.cfg['p_c'])
                c1 = self._mutate(c1, self.cfg['p_m'], self.cfg['sigma'])
                c2 = self._mutate(c2, self.cfg['p_m'], self.cfg['sigma'])
                offspring[i] = self._clamp(c1)
                offspring[i + 1] = self._clamp(c2)

            # 3. Оценка потомков
            off_fitness = self._evaluate(offspring)

            # 4. Элитизм: лучшие `elitism` родителей вытесняют худших потомков
            elite_idx = np.argsort(fitness)[:elitism]
            worst_off_idx = np.argsort(off_fitness)[-elitism:]
            offspring[worst_off_idx] = population[elite_idx]
            off_fitness[worst_off_idx] = fitness[elite_idx]

            # 5. Смена поколения
            population = offspring
            fitness = off_fitness

            # 6. Обновление best-so-far
            gen_best_idx = int(np.argmin(fitness))
            if fitness[gen_best_idx] < best_f:
                best_f = float(fitness[gen_best_idx])
                best_x = population[gen_best_idx].copy()

            history.append((generation, best_f))

        return {
            'best_x': best_x,
            'best_f': best_f,
            'history': history,
            'n_evals': self.n_evals,
        }