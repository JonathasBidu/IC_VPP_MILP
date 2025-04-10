from pymoo.core.problem import ElementwiseProblem
from pymoo.core.variable import Real, Binary
import numpy as np

def decompose_xr(xr, data):

    # Parâmetros iniciais de VPP
    Nt = data['Nt'] # Período de simulação da VPP
    Ndl = data['Ndl'] # Quantidade de cargas despacháveis da VPP
    Nbm = data['Nbm'] # Quantidade de usinas de biomassa da VPP
    Nbat = data['Nbat'] # Quantidade de armazenadores da VPP

    # Definindo a quantidade de variáveis reais (Nr)
    # Variáveis reais: p_exp, p_imp, p_bm, gamma_bm, p_chg, p_dch, soc, p_dl
    Nr = Nt + Nt + (Nt * Nbm) + (Nt * Nbm) + (Nt * Nbat) + (Nt * Nbat) + (Nbat * Nt) + (Nt * Ndl)

    xr = np.array(xr)

    begin = 0 
    end = Nt
    p_exp = xr[begin: end]

    begin = end
    end = end + Nt
    p_imp = xr[begin: end]

    begin = end
    end = end + (Nt * Nbm)
    p_bm = xr[begin: end]

    begin = end
    end = end + (Nt * Nbm)
    gamma_bm = xr[begin: end]

    begin = end
    end = end + (Nt * Nbat)
    p_chg = xr[begin: end]

    begin = end
    end = end + (Nt * Nbat)
    p_dch = xr[begin: end]

    begin = end
    end = end + (Nt * Nbat)
    soc = xr[begin: end]

    begin = end
    end = end + (Nt * Ndl)
    p_dl = xr[begin: end]

    return p_exp, p_imp, p_bm, gamma_bm, p_chg, p_dch, soc, p_dl

def decompose_xi(xi, data):

    # Parâmetros iniciais de VPP
    Nt = data['Nt'] # Período de simulação da VPP
    Ndl = data['Ndl'] # Quantidade de cargas despacháveis da VPP
    Nbm = data['Nbm'] # Quantidade de usinas de biomassa da VPP
    Nbat = data['Nbat'] # Quantidade de armazenadores da VPP

    # Definindo a quantidade de variáveis inteiras (Ni)
    # Variáveis inteiras: u_exp, u_imp, u_bm, u_chg, u_dch, u_dl
    Ni = Nt + Nt + (Nt * Nbm) + (Nt * Nbat) + (Nt * Nbat) + (Nt * Ndl)

    xi = np.array(y)

    begin = 0
    end = Nt
    u_exp = xi[begin: end]

    begin = end
    end = end + Nt
    u_imp = xi[begin: end]

    begin = end
    end = end + (Nt * Nbm)
    u_bm = xi[begin: end]

    begin = end
    end = end + (Nt * Nbat)
    u_chg = xi[begin: end]

    begin = end
    end = end + (Nt * Nbat)
    u_dch = xi[begin: end]

    begin = end
    end = end + (Nt * Ndl)
    u_dl = xi[begin: end]

    return u_exp, u_imp, u_bm, u_chg, u_dch, u_dl

def func(xr, xi, data):

    # Parametros iniciais da VPP
    Nt = data['Nt'] # Período de simulação da VPP
    Nbm = data['Nbm'] # Quantidade de usinas de biomassa da VPP
    Ndl = data['Ndl'] # Quantidade de cargas despacháveis da VPP
    Npv = data['Npv'] # Quantidade de usinas solares (FVs) da VPP
    Nwt = data['Nwt'] # Quantidade de usinas eólicas (EOs) da VPP
    Nbat = data['Nbat'] # Quantidade de armazendores da VPP
    tau_pld = data['tau_pld'] # Tarifa PLD (Preço de Liquidação de Diferença), shape (24,)
    tau_dist = data['tau_dist'] # Tarifa da distribuidora
    kappa_bm = data['kappa_bm'] # Tarifa de custo operacional, shape (2,)
    kappa_bm_start = data['kappa_bm_start'] # Tarifa de custo de partida, shape (2,)
    kappa_bat = data['kappa_bat'] # Tarifa de custo operacional dos armazenadores, shape (1,)
    tau_dl = data['tau_dl']
    kappa_pv = data['kappa_pv']
    kappa_wt = data['kappa_wt']

    # Projeções iniciais
    p_pv = data['p_pv'] # Potência das usinas solares (FVs) VPP
    p_wt = data['p_wt'] # Potênica das usinas eólicas (EOs) VPP    

    # Decompondo o vetor x em variáveis de decisão
    p_exp, p_imp, p_bm, gamma_bm, p_chg, p_dch, soc, p_dl = decompose_xr(xr)
    u_exp, u_imp, u_bm, u_chg, u_dch, u_dl = decompose_xi(xi)

    # u_exp = np.float64(u_exp > 0.5)
    # u_imp = np.float64(u_imp > 0.5)
    # u_chg = np.float64(u_chg > 0.5)
    # u_dch = np.float64(u_dch > 0.5)
    # u_dl = np.float64(u_dl > 0.5)

    # Cálculo de receita gerada pela VPP (R) em cada instante de tempo t no período Nt da simulação
    R = 0
    for t in range(Nt):
        R += p_exp[t] * tau_pld[t]

    # Cálculo de despesa com a importação de energia junto a distribuidora (D) em cada instante de tempo t no período da simulação Nt
    D = 0
    for t in range(Nt):
        D += p_imp[t] * tau_dist[t]

    # Variável de custo das UBTMs
    Cbm = 0

    # Cálculo do custo operacional das UBTMs
    for t in range(Nt):
        for i in range(Nbm):
            Cbm += gamma_bm[i, t]

    # Cálculo do custo de partida/parada das UBTMs
    for t in range(1, Nt):
        for i in range(Nbm):
            Cbm += (u_bm[i, t] - u_bm[i, t - 1]) * kappa_bm_start[i]

    # Variável de custo dos armazenadores
    Cbat = 0

    # Cálculo do custo operacional dos armazenadores
    for t in range(Nt):
        for i in range(Nbat):
            Cbat += (p_chg[i, t] - p_dch[i, t]) * kappa_bat[i]

    # Variável de custo de corte de carga
    Cdl = 0

    # Cálculo da compensação de corte da VPP
    for t in range(Nt):
        for i in range(Ndl):
            Cdl += p_dl[i, t] * tau_dl[t]

    # Variável de custo das usinas EOs
    Cwt = 0

    # Cálculo do custo operacional das usinas EOs
    for t in range(Nt):
        for i in range(Nwt):
            Cwt += p_wt[i, t] * kappa_wt[i]

    # Variável de custo das usinas FVs
    Cpv = 0

    # Cálculo do custo operacional das usinas FVs
    for t in range(Nt):
        for i in range(Npv):
            Cpv += p_pv[i, t] * kappa_pv[i]


    # Cálculo do custo total da VPP
    D = D + (Cbm + Cbat + Cdl + Cwt + Cpv)

    # Variável de lucro da VPP 
    fval = R - D

    return fval

def ieq(xr, xi, data):

      # Parâmetros iniciais da VPP
    Nt = data['Nt'] # Período da simulação
    Nbm = data['Nbm'] # Quantidade de UBTMs 
    Ndl = data['Ndl'] # Quantidade de cargas despacháveis
    Nbat = data['Nbat'] # Quantidade de armazenadores 
    # Mimp = data['Mimp'] # Constante de importação
    # Mexp = data['Mexp'] # Constante de esportação
    M = 10 # Valor provisório de Mimp e Mexp
    Mimp = M # Provisório
    Mexp = M # Provisório
    alpha_bm = data['kappa_bm'] # Variáveis de custo das UBTMs
    beta_bm = [0.0, 0.0] # Provisório
    p_bm_min = data['p_bm_min'] # Potênica Mínima das UBTMs
    p_bm_max = data['p_bm_max'] # Potênca máxima das UBTMs
    p_bm_rup = data['p_bm_rup'] # Potência de rampa de subida das UBTMs
    p_bm_rdown = data['p_bm_rdown'] # Potência de rampa de descida das UBTMs
    p_bat_max = data['p_bat_max'] # Potência máxima dos armazenadores
    p_dl_min = data['p_dl_min'] # Potência das cargas despacháveis
    p_dl_max = data['p_dl_max'] # Potência das cargas despacháveis

    # Decompondo a população inicial em variáveis de decisão para teste
    p_exp, p_imp, p_bm, gamma_bm, p_chg, p_dch, soc, p_dl = decompose_xr(xr, data)
    u_exp, u_imp, u_bm, u_chg, u_dch, u_dl = decompose_xi(xi, data)

    Nimpc = Nt # Quantidade de restrições de desigaualdade de importação
    imp_constr = np.zeros(Nimpc) # Vetor de restrições de desigualdade de importação da VPP (imp_constr - import constraints)
    # Definindo as restrições de desigualdade de importação da VPP: p_imp[t] - (1 - u_exp[t]) * Mimp <= 0
    for t in range(Nt):
        imp_constr[t] = p_imp[t] - (1 - u_exp[t]) * Mimp

    Nexpc = Nt # Quantidade de restrições de desigaualdade de exportação
    exp_constr = np.zeros(Nexpc) # Vetor de restrições de desigualdade de expportação da VPP (exp_constr - export constraints)
    # Calculando as restrições de desigualdade de exportação da VPP: p_exp[t] - (1- u_imp[t]) * Mexp <= 0
    for t in range(Nt):
        exp_constr[t] = p_exp[t] - (1- u_imp[t]) * Mexp
    
    Nbmc = (Nbm * Nt) + (Nbm * Nt) + (Nbm * Nt) + (Nbm * (Nt - 1)) + (Nbm * (Nt - 1)) # Quantidade de restrições de desigualdade das UBTMs
    bm_constr = np.zeros(Nbmc) # Vetor de restrições de desigualdade das UBTMs (bm_constraints)
    k = 0
    # Calculando as restrições de desigualdade das UBTMs da VPP: alpha[i] * p_bm[i, t] + beta[i] - gamma_bm[i, t] <= 0
    for t in range(Nt):
        for i in range(Nbm):
            bm_constr[k] = alpha_bm[i] * p_bm[i, t] + beta_bm[i] - gamma_bm[i, t]
            k += 1
    
    # Calculando a potência mínima das UBTMs: p_bm_min[i] * u_bm[i, t] - p_bm[i, t] <= 0
    for t in range(Nt):
        for i in range(Nbm):
            bm_constr[k] = p_bm_min[i] * u_bm[i, t] - p_bm[i, t]
            k += 1

    # Calculando a potência máxima das UBTMs: p_bm[i, t] - p_bm_max[i] * u_bm[i, t] <= 0
    for t in range(Nt):
        for i in range(Nbm):
            bm_constr[k] = p_bm[i, t] - p_bm_max[i] * u_bm[i, t]
            k += 1

    # Calculando a potência subida das UBTMs: p_bm[i, t] - p_bm[i, t - 1] - p_bm_rup[i] <= 0
    for t in range(1, Nt):
        for i in range(Nbm):
            bm_constr[k] = p_bm[i, t] - p_bm[i, t - 1] * p_bm_rup[i]
            k += 1

    # Calculando a potência descida das UBTMs: p_bm[i, t - 1] - p_bm[i, t] - p_bm_rdonw[i] >= 0
    for t in range(1, Nt):
        for i in range(Nbm):
            bm_constr[k] =  p_bm[i, t - 1] - p_bm[i, t] - p_bm_rdown[i]
            k += 1

    Nbatc = (Nbat * Nt) + (Nbat * Nt) + (Nbat * Nt) # Quantidade de restrições de desigualdade dos armazenadores
    bat_constr =  np.zeros(Nbatc) # Vetor de restrições de desigualdade dos armazendores (bat_constr - batery constraints)
    k = 0
    # Calculando as restrições de carregamento máximo dos armazenadores: p_chg[i, t] - p_bat_max[i] * u_chg[i, t] <= 0
    for t in range(Nt):
        for i in range(Nbat):
            bat_constr[k] = p_chg[i, t] - p_bat_max[i] * u_chg[i, t]
            k += 1

    # Calculando as restrições de descarregamento máximo dos armazenadores: p_dch[i, t] - p_bat_max[i] * u_dch[i, t] <= 0
    for t in range(Nt):
        for i in range(Nbat):
            bat_constr[k] = p_dch[i, t] - p_bat_max[i] * u_dch[i, t]
            k += 1

    # Calculando as restrições de simultaneidade do estado dos armazenadores: u_chg[i, t] + u_dch[i, t] - 1 <= 0
    for t in range(Nt):
        for i in range(Nbat):
            bat_constr[k] = u_chg[i, t] + u_dch[i, t] - 1 
            k += 1
    
    Ndlc = (Ndl * Nt) + (Ndl * Nt) # Quantidade de restrições de desigualdade das cargas despacháveis
    dl_constr = np.zeros(Ndlc) # Vetor de restrições de desigualdade das cargas despacháveis (dl_constr - dload constraints)
    k = 0
    # Calculando as restrições de potência mínima das cargas despacháveis: p_dl_min[i, t] * u_dl[i, t] - p_dl[i, t] <= 0
    for t in range(Nt):
        for i in range(Ndl):
            dl_constr[k] = p_dl_min[i, t] * u_dl[i, t] - p_dl[i, t]
            k += 1

    # Calculando as restrições de potência máxima das cargas despacháveis: p_dl[i, t] - p_dl_max[i, t] * u_dl[i, t] <= 0
    for t in range(Nt):
        for i in range(Ndl):
            dl_constr[k] = p_dl[i, t] - p_dl_max[i, t] * u_dl[i, t]
            k += 1

    # Vetor com todas as restrições de desigualdade da VPP
    c_ieq = np.concatenate((imp_constr,
                                 exp_constr,
                                 bm_constr,
                                 bat_constr,
                                 dl_constr
                                 ))

    return c_ieq

def eq(xr, xi, data):

        # Parâmetros iniciais da VPP:
    Nt = data['Nt'] # Período da simulação
    Nbat = data['Nbat'] # Quantidade de armazenadores da VPP
    eta_chg = data['eta_chg'] # Rendimento do carregamento da bateria
    eta_dch = data['eta_dch'] # Rendimento do descarregamento da bateria

    # Projeções iniciais:
    p_wt = data['p_wt'] # Potência das EOs da VPP
    p_pv = data['p_pv'] # potência das FVs da VPP
    p_l = data['p_l'] # Potência das cargas Não despacháveis da VPP

    # Decompondo a população inicial em variáveis de decisão para teste
    p_exp, p_imp, p_bm, gamma_bm, p_chg, p_dch, soc, p_dl = decompose_xr(xr, data)
    u_exp, u_imp, u_bm, u_chg, u_dch, u_dl = decompose_xi(xi, data)

    
    Npbc = Nt # Quantidade de restrições de igualdade de balanço de potência
    pwr_blc_constr = np.zeros(Npbc) # Vetor de restrição de igualdade do balanço de potência da VPP (pwr_blc_contr - power balance constraints)
    # Calculando as restrições de balanço de potência:
    for t in range(Nt):
        pwr_blc_constr[t] = (- p_exp[t] +
                      np.sum(p_wt[:, t]) +
                      np.sum(p_pv[:, t]) +
                      np.sum(p_bm[:, t]) +
                      p_imp[t] - 
                      np.sum(p_l[:, t]) -
                      np.sum(p_dl[:, t]) -
                      np.sum((p_chg[:, t] - p_dch[:, t]))
                      )

    Nsimc = Nt # Quantidade de restrições de simulatneidade
    simul_constr = np.zeros(Nsimc) # Vetor de restrições de igualdades de simultaneidade do estado de impotação/exportação (simul_constr - simultaneity constraints)
    # Calculando as restrições de simultaneidade em cada instante t no período da simulação Nt: u_exp[t] + u_imp[t] - 1 = 0 
    for t in range(Nt):
        simul_constr[t] = 1 - (u_exp[t] + u_imp[t]) 
   
    Nsc = (Nbat * Nt) # Quantidade de restrições de igualdade de estado de carga
    soc_constr = np.zeros(Nsc) # Vetor de restrições de igualdades do estado de carga (SoC) dos armazenadores
    k = 0
    for t in range(1, Nt): 
        for i in range(Nbat):
            soc_constr[k] = soc[i, t] - soc[i, t - 1] - (p_chg[i, t] * eta_chg[i]) + (p_dch[i, t] / eta_dch[i])
            k += 1

    # Vetor com todas as restrições de igualdade da VPP
    c_eq = np.concatenate((pwr_blc_constr, simul_constr, soc_constr))

    return c_eq




def solver_GA(data):

    from get_limits import bounds as b
    from pymoo.core.mixed import MixedVariableGA
    from pymoo.optimize import minimize

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
    ub, lb = b(data)

    class MixedVariableProblem(ElementwiseProblem):

        def __init__(self, data, **kwargs):


            vars = {
                "xr" : Real(bounds=(0, 10), shape = Nr),
                "xi" : Binary(shape = Ni)
            }
            super().__init__(vars = vars, **kwargs)
            self.data = data

        def _evaluate(self, X, out, *args, **kwargs):

            xr, xi = X["xr"], X["xi"]

            
            out['F'] = - func(xr, xi, self.data)
            out['G'] = ieq(xr, xi, self.data)
            out['H'] = eq(xr, xi, self.data)
    
    problem = MixedVariableProblem(data, n_obj = 1, n_var = nvars, n_eq_constr = c_eq, n_ieq_constr = c_ieq, xu = ub, xl = lb)
    algorithm = MixedVariableGA(pop_size = 500)
    termination = ('n_gen', 50)

    res = minimize(problem,
                   algorithm,
                   termination,
                   verbose = True,
                   seed = 1)


    return res

from vpp_data import vpp_data
from pathlib import Path
from generator_scenarios import import_scenarios_from_pickle

data = vpp_data()

data['Nt'] = 24
Nt = 24
Nbm = data['Nbm']
Nbat = data['Nbat']

path = Path(__file__).parent / "Cenários.pkl"
cenarios = import_scenarios_from_pickle(path)

for cenario in cenarios:

    data['p_l'] = cenario['p_l']
    data['p_pv'] = cenario['p_pv']
    data['p_wt'] = cenario['p_wt']
    data['p_dl_ref'] = cenario['p_dl_ref']
    data['p_dl_min'] = cenario['p_dl_min']
    data['p_dl_max'] = cenario['p_dl_max']
    data['tau_pld'] = cenario['tau_pld']
    data['tau_dist'] = cenario['tau_dist']
    data['tau_dl'] = cenario['tau_dl']

# Obtendo a solução do otimizador (GA)
res = solver_GA(data)

# Obtendo o vetor de soluções da VPP
x = res.X # Matriz de soluções ótimas
G = res.G # Matriz de restrições de desigualdades
H = res.H # Matriz de restrições de igualdades

if x is not None:

    import numpy as np
    from decompose_vetor import decompose
    from vpp_plot import plot

    # Decompondo o vetor de soluções nas suas variáveis de decisão
    data['p_exp'], data['p_imp'], data['p_bm'], data['gamma_bm'], data['p_chg'], data['p_dch'], data['soc'], data['p_dl'], data['u_exp'], data['u_imp'], data['u_bm'], data['u_chg'], data['u_dch'], data['u_dl'] = decompose(x, data)
       
    begin = 0
    end = Nt
    pwr_blc_contr = G[begin: end]
    # pwr_blc_contr = (pwr_blc_contr < 0)

    begin = end
    end = end + Nt
    simult_constr = G[begin: end]
    # simult_constr = (simult_constr < 0)

    begin = end
    end = end + (Nbat * Nt)
    soc_constr = G[begin: end]
    # soc_constr = (soc_constr < 0)

    # print(f'\nBalanço de potência\n{pwr_blc_contr}\n')
    # print(f'\nNão simultaneidade\n{simult_constr}\n')
    # print(f'\nEstado de carga\n{soc_constr}\n')

    # Visualizando o despacho otimizado da VPP
    plot(data)
    print('\n')
    print(f'O lucro dessa simulação foi de aproximadamente {res.F[0]:.2f}\n')
    print(f'O total de violações dessa simulação foi de {res.CV[0]:.2f}\n')

    print(f'\nu_imp {data['u_imp']}\n')
    print(f'u_exp {data['u_exp']}')
else:
    print('Não foi encontrado solução para essa simulação')


