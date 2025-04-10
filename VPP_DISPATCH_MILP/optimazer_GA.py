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

'''
    Este script tem a finalidade de construir um otimizador (GA) para encontrar soluções ótimas (maximizar o lucro) de uma função objetivo de VPP.
        
        - Parâmetros de entrada (data: dict):
            - data: Dicionário contendo os parâmetros inciais e as projeções temporais iniciais;

                - Projeções iniciais:
                    - Nt: Período da simulação da VPP;
                    - Ndl: Quantidade de cargas despacháveis da VPP;
                    - Nbm: Quantidade de UBTMs da VPP;
                    - Nbat: Quantidade de armazenadores da VPP;

        - Retorna:
'''

def solver(data: dict):

    # Parâmetros iniciais da VPP
    Nt = data['Nt'] # Períod ad simulação da VPP
    Ndl = data['Ndl'] # Quantida de cargas despacháveis da VPP
    Nbm = data['Nbm'] # Quantidade de UBTMs da VPP
    Nbat = data['Nbat'] # Quantidade de armazenadores da VPP

    # Variáveis reais: p_exp, p_imp, p_bm, gamma_bm, p_chg, p_dch, soc, p_dl
    Nr = Nt + Nt + (Nt * Nbm) + (Nt * Nbm) + (Nt * Nbat) + (Nt * Nbat) + (Nbat * Nt) + (Nt * Ndl)
    # Variáveis inteiras: u_exp, u_imp, u_bm, u_chg, u_dch, u_dl
    Ni = Nt + Nt + (Nt * Nbm) + (Nt * Nbat) + (Nt * Nbat) + (Nt * Ndl)
    # Definido a quantidade de variáveis
    nvars = Nr + Ni

    # Definindo a quantidade de restrições de igualdade da VPP
    Npbc = Nt # quantidade de restrições de igualdade do balanço de potência da VPP
    Nsimc = Nt # Quantidade de restrição igualdade de simultaneidade VPP
    Nsc = (Nbat * Nt) # Quantidade restrições de igualdade do estado de carga dos armazenadores da VPP
    c_eq = Npbc + Nsimc + Nsc # Total de restrições de igualdade da VPP

    # Definindo a quantidade de restrições de desigualdades da VPP
    Nimpc = Nt # Quantidade de restrições de desigualdade de importação da VPP
    Nexpc = Nt # Quantidade de restrições de desigualdade de exportação da VPP
    Nbmc = (Nbm * Nt) + (Nbm * Nt) + (Nbm * Nt) + (Nbm * (Nt - 1)) + (Nbm * (Nt - 1)) # Quantidade de restrições de desigualdade da VPP
    Nbatc = (Nbat * Nt) + (Nbat * Nt) + (Nbat * Nt) # Quantidade de restrições de desigualdade dos armazenadores da VPP
    Ndlc = (Ndl * Nt) + (Ndl * Nt) # Quantidade de restrições de desigualdade das cargas despacháveis da VPP
    c_ieq = Nimpc + Nexpc + Nbmc + Nbatc + Ndlc # Total de restrições de desigualdade da VPP

    # Obtendo os limites superior (ub) e inferior (lb) das variáveis de decisão
    ub, lb = bounds(data)

    # Criando uma classe que define o problema
    class MyProblem(ElementwiseProblem):

        def __init__(self, data: dict, **kwargs):
            super().__init__(data, **kwargs)
            self.data = data # Atribuindo o dicionário data a classe

        def _evaluate(self, x, out, *args, **kwargs):

            out['F'] = - obj_function(x, self.data)
            out['G'] = ieq_constr(x, self.data)
            out['H'] = eq_constr(x, self.data)

    # Instanciando a classe problema
    problem = MyProblem(data,
                        n_obj = 1,
                        n_var = nvars,
                        n_eq_constr = c_eq,
                        n_ieq_constr = c_ieq,
                        xu = ub,
                        xl = lb
                        )
    
    # Definindo o algoritmo 
    algorithm = GA(pop_size = 30)
    termination = ('n_gen', 100)

    # Obtendo a solução
    # res = minimize(problem, algorithm, termination, verbose = True, seed = 1)

    # MODELO FEITO COM PENALIDADES NAS RESTRIÇÕES
    from pymoo.constraints.as_penalty import ConstraintsAsPenalty
    from pymoo.core.evaluator import Evaluator
    from pymoo.core.individual import Individual

    res = minimize(ConstraintsAsPenalty(problem, penalty = 100.0), algorithm, termination, seed = 1, verbose = True)
    res = Evaluator().eval(problem, Individual(X = res.X))

    # print("\nFunção Objetivo:", res.F)
    # print("\nViolação de desigualdade (G):", res.G)
    # print("\nViolação de igualdade (H):", res.H)


    return res

 