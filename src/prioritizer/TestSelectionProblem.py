import numpy as np
from pymoo.core.problem import ElementwiseProblem
class TestSelectionProblem(ElementwiseProblem):
    def __init__(self, coverage, diff_coverage, execution_time, failure_rate, budget):
        self.coverage = coverage
        self.diff_coverage = diff_coverage
        self.execution_time = execution_time
        self.failure_rate = failure_rate
        self.budget = budget
        n_var = coverage.shape[0]

        super().__init__(n_var=n_var,
                         n_obj=4,
                         n_constr=1,  # enforce exact budget
                         xl=0, xu=1,
                         type_var=np.bool_)

    def _evaluate(self, x, out, *args, **kwargs):
        selected = np.where(x == 1)[0]
        cov = np.any(self.coverage[selected], axis=0)
        diff_cov = np.any(self.diff_coverage[selected], axis=0)
        exec_time = np.sum(self.execution_time[selected])
        faults = np.sum(self.failure_rate[selected])

        out["F"] = [-np.sum(cov), -np.sum(diff_cov), exec_time, -faults]  # Minimize -max objectives
        out["G"] = [np.sum(x) - self.budget]  # Constraint: exactly budget selected