import numpy as np
from typing import List
from pymoo.core.problem import Problem
from pymoo.optimize import minimize
from pymoo.termination import get_termination

# Algorithms
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.algorithms.moo.nsga3 import NSGA3
from pymoo.algorithms.moo.moead import MOEAD
from pymoo.algorithms.moo.spea2 import SPEA2

# Operators
from pymoo.operators.sampling.rnd import BinaryRandomSampling
from pymoo.operators.crossover.hux import HUX
from pymoo.operators.mutation.bitflip import BitflipMutation
from pymoo.util.ref_dirs import get_reference_directions


def multiobjective_select(
    test_cases: List[str],
    budget: int,
    coverage: np.ndarray,
    diff_coverage: np.ndarray,
    execution_time: np.ndarray,
    failure_rates: np.ndarray,
    algorithm_name: str = "nsga2",
    generations: int = 50,
    pop_size: int = 500
) -> List[str]:

    num_tests = len(test_cases)

    class TestSelectionProblem(Problem):
        def __init__(self):
            super().__init__(n_var=num_tests,
                             n_obj=4,
                             n_constr=1,
                             xl=0,
                             xu=1,
                             type_var=np.bool_)

        def _evaluate(self, X, out, *args, **kwargs):
            F = np.zeros((X.shape[0], 4))
            G = np.zeros((X.shape[0], 1))

            for i, individual in enumerate(X):
                selected = np.where(individual == 1)[0]
                cov = np.any(coverage[selected], axis=0) if selected.size > 0 else np.zeros(coverage.shape[1])
                diff_cov = np.any(diff_coverage[selected], axis=0) if selected.size > 0 else np.zeros(diff_coverage.shape[1])
                total_exec_time = np.sum(execution_time[selected]) if selected.size > 0 else np.inf
                total_faults = np.sum(failure_rates[selected]) if selected.size > 0 else 0

                F[i] = [-np.sum(cov), -np.sum(diff_cov), total_exec_time, -total_faults]
                G[i, 0] = abs(np.sum(individual) - budget)

            out["F"] = F
            out["G"] = G

    def get_algorithm(name: str):
        name = name.lower()
        if name == "nsga2":
            return NSGA2(
                pop_size=pop_size,
                sampling=BinaryRandomSampling(),
                crossover=HUX(),
                mutation=BitflipMutation(prob=0.05),
                eliminate_duplicates=True
            )
        elif name == "nsga3":
            ref_dirs = get_reference_directions("das-dennis", 4, n_partitions=12)
            return NSGA3(
                ref_dirs=ref_dirs,
                pop_size=pop_size,
                sampling=BinaryRandomSampling(),
                crossover=HUX(),
                mutation=BitflipMutation(prob=0.05),
                eliminate_duplicates=True
            )
        elif name == "moead":
            ref_dirs = get_reference_directions("uniform", 4, n_partitions=12)
            return MOEAD(
                ref_dirs=ref_dirs,
                n_neighbors=15,
                sampling=BinaryRandomSampling(),
                crossover=HUX(),
                mutation=BitflipMutation(prob=0.05),
                eliminate_duplicates=True
            )
        elif name == "spea2":
            return SPEA2(
                pop_size=pop_size,
                sampling=BinaryRandomSampling(),
                crossover=HUX(),
                mutation=BitflipMutation(prob=0.05),
                eliminate_duplicates=True
            )
        else:
            raise ValueError(f"Unsupported algorithm: {name}")

    problem = TestSelectionProblem()
    algorithm = get_algorithm(algorithm_name)

    result = minimize(
        problem,
        algorithm,
        termination=get_termination("n_gen", generations),
        seed=1,
        verbose=False
    )

    # Pick best solution among all evolved solutions.
    F = result.F
    F_norm = (F - F.min(axis=0)) / (F.max(axis=0) - F.min(axis=0) + 1e-9)
    ranks = np.argsort(np.argsort(F_norm, axis=0), axis=0)
    total_ranks = np.sum(ranks, axis=1)
    best_idx = np.argmin(total_ranks)

    best = result.X[best_idx]

    selected_ids = [test_cases[i] for i, bit in enumerate(best) if bit == 1]

    return selected_ids
