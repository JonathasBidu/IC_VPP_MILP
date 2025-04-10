from pymoo.core.problem import ElementwiseProblem
from pymoo.algorithms.soo.nonconvex.ga import GA
from objetive_function import obj_function
from decompose_vetor import decompose
from ieq_constraints import ieq_constr
from eq_constraints import eq_constr
from get_limits import bounds
import numpy as np
from pymoo.optimize import minimize

from pymoo.config import Config
Config.warnings['not_compiled'] = False

def solver(data: dict):

    # Parâmetros iniciais da VPP
    Nt = data['Nt']
    Ndl = data['Ndl']
    Nbm = data['Nbm']
    Nbat = data['Nbat']

    # Variáveis reais
    Nr = Nt + Nt + (Nt * Nbm) + (Nt * Nbm) + (Nt * Nbat) + (Nt * Nbat) + (Nbat * Nt) + (Nt * Ndl)
    # Variáveis inteiras
    Ni = Nt + Nt + (Nt * Nbm) + (Nt * Nbat) + (Nt * Nbat) + (Nt * Ndl)
    # Total de variáveis
    nvars = Nr + Ni

    # Cálculo automático do tamanho da população
    fator_pop = 2.0  # Ajuste aqui conforme sua necessidade
    pop_size = int(nvars * fator_pop)

    print(f"Total de variáveis de decisão: {nvars}")
    print(f"Tamanho da população definido: {pop_size}")

    # Restrições de igualdade
    Npbc = Nt
    Nsimc = Nt
    Nsc = Nbat * Nt
    c_eq = Npbc + Nsimc + Nsc

    # Restrições de desigualdade
    Nimpc = Nt
    Nexpc = Nt
    Nbmc = (Nbm * Nt) * 3 + (Nbm * (Nt - 1)) * 2
    Nbatc = (Nbat * Nt) * 3
    Ndlc = (Ndl * Nt) * 2
    c_ieq = Nimpc + Nexpc + Nbmc + Nbatc + Ndlc

    # Limites das variáveis
    ub, lb = bounds(data)

    from pymoo.operators.crossover.sbx import SBX
    from pymoo.operators.mutation.pm import PM
    from pymoo.operators.sampling.rnd import FloatRandomSampling, IntegerRandomSampling
    from pymoo.operators.sampling.rnd import FloatRandomSampling, IntegerRandomSampling
    from pymoo.operators.crossover.sbx import SBX
    from pymoo.operators.mutation.pm import PM

    # Máscara para tipos de variáveis
    mask = ["real"] * Nr + ["int"] * Ni

    # # Operadores para GA com variáveis mistas
    # sampling = MixedVariableSampling(mask, {
    #     "real": FloatRandomSampling(),
    #     "int": IntegerRandomSampling()
    # })

    # crossover = MixedVariableCrossover(mask, {
    #     "real": SBX(eta=15, prob=0.9),
    #     "int": SBX(eta=15, prob=0.9)
    # })

    # mutation = MixedVariableMutation(mask, {
    #     "real": PM(eta=20),
    #     "int": PM(eta=20)
    # })

    # Criando classe do problema
    class MyProblem(ElementwiseProblem):

        def __init__(self, data: dict, **kwargs):
            super().__init__(data, **kwargs)
            self.data = data

        def _evaluate(self, x, out, *args, **kwargs):
            out['F'] = - obj_function(x, self.data)
            out['G'] = ieq_constr(x, self.data)
            out['H'] = eq_constr(x, self.data)

    problem = MyProblem(data,
                        n_obj=1,
                        n_var=nvars,
                        n_eq_constr=c_eq,
                        n_ieq_constr=c_ieq,
                        xu=ub,
                        xl=lb)

    # Definindo algoritmo GA com parâmetros automáticos
    algorithm = GA(
        pop_size=pop_size,
        sampling=sampling,
        crossover=crossover,
        mutation=mutation,
        eliminate_duplicates=True
    )

    termination = ('n_gen', int((nvars * 20) / pop_size))

    # Executando otimização com penalidades
    from pymoo.constraints.as_penalty import ConstraintsAsPenalty
    from pymoo.core.evaluator import Evaluator
    from pymoo.core.individual import Individual

    res = minimize(ConstraintsAsPenalty(problem, penalty=100.0), algorithm, termination, seed=1, verbose=True)
    res = Evaluator().eval(problem, Individual(X=res.X))

    return res
