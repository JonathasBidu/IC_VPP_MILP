import numpy as np
from decompose_vetor import decompose

"""
    Este script tem a finalidade de, a partir dos parâmetros de entrada, das projeções iniciais e das variáveis de decisão, calcular uma função de lucro. Dessa forma, a função será fornecida a um otimizador para que o mesmo encontre a solução ótima, onde a VPP forneça uma maior margen de lucro.

        - Parâmetros de entrada (x:np.ndarray, data: dict):
            - (data: dict): Dicionário contendo os parâmetros iniciais e projeções iniciais. 
                - Parâmetros iniciais:
                    - Nt: Período da simulação;
                    - Nbm: Quantidade de usinas de geração à biomassa (UBTMs) da VPP;
                    - Ndl: Quantidade de cargas despacháveis da VPP;
                    - Npv: Quantidade de usinas solares (FVs) da VPP;
                    - Nwt: Quantidade de usinas eólicas (EOs) da VPP; 
                    - Nbat: Quantidade de armazenadores da VPP;
                    - kappa_bm: Tarifa de custo operacional das UBTMs;
                    - kappa_bm_start: Tarifa de custo de partida/parada das UBTMs;
                    - kappa_pv: Tarifa de custo operacioanl das FVs;
                    - kappa_wt: Tarifa de custo operacional das EOs;
                    - kappa_bat: Tarifa de custo operacional dos armazenadores;

                - Projeções iniciais:
                    - p_pv: Potência das usinas solares (FVs) da VPP, shape (Npv, Nt);
                    - p_wt: Potência das usians eólica (EOs) da VPP, shape (Nwt, Nt);
                    - tau_pld: Tarifa de Preço de Liquidação de Diferença (PLD), shape (Nt,);
                    - tau_dist: Tarifa da distribuidora, shape (Nt,);
                    - tau_dl: Tarifa de compesação de corte de carga, shape (Nt,);

            - (x: np.ndarray): Vetro contendo as variáveis de decisão provindos de um otimizador (GA).
                - Variáveis de decisão:
                    - p_exp: Potência de exportação da VPP, shape (Nt,);
                    - p_imp: Potênica de importação da VPP, shape (Nt,);
                    - gamma_bm: Custo das usinas de biomassa, shape (Nbm, Nt);
                    - p_chg: Potência de carregamento dos armazenadores da VPP, shape (Nbat, Nt);
                    - p_dch: Potência de descarregamento dos amazenadores da VPP, shape (Nbat, Nt);
                    - p_dl: Potência das cargas despacháveis da VPP, shape (Ndl, Nt);
                    - u_exp: Estado de exportação da VPP, shape (Nt,);
                    - u_imp: Estado de impportação da VPP, shape (Nt,);
                    - u_bm: Estado das UBTMs da VPP, shape (Nbm, Nt);
                    - u_chg: Estado do carregamento dos armazenadores da VPP, shape (Nbat, Nt);
                    - u_dch: Estado do descarregamento dos armazenadores da VPP, shape (Nbat, Nt);
                    - u_dl: Estado das cargas despacháveis da VPP, shape (Ndl, Nt);

        - Retorna um número real (Lucro) -> np.float64:

            - fval: Número real (Lucro da VPP)
"""

def obj_function(x: np.ndarray, data: dict)-> np.float64:

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
    p_exp, p_imp, p_bm, gamma_bm, p_chg, p_dch, soc, p_dl, u_exp, u_imp, u_bm, u_chg, u_dch, u_dl = decompose(x, data)

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
            Cbm += gamma_bm[i, t] * kappa_bm[i]

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

# Exemplo de uso
if __name__ == '__main__':

    from vpp_data import vpp_data
    from decompose_vetor import decompose
    from generator_scenarios import import_scenarios_from_pickle
    from pathlib import Path

    data = vpp_data()

    # Parâmetros iniciais de VPP
    data['Nt'] = 24
    Nt = data['Nt'] # Período de simulação da VPP
    Nbm = data['Nbm'] # Quantidade de usinas de biomassa da VPP
    Nbat = data['Nbat'] # Quantidade de armazenadores da VPP
    Ndl = data['Ndl'] # Quantidade de cargas despacháveis da VPP

    # Definindo a quantidade de variáveis reais (Nr) e variáveis inteiras (Ni)
    # Variáveis reais: p_exp, p_imp, p_bm, gamma_bm, p_chg, p_dch, soc, p_dl
    Nr = Nt + Nt + (Nt * Nbm) + (Nt * Nbm) + (Nt * Nbat) + (Nt * Nbat) + (Nbat * Nt) + (Nt * Ndl)
    # Variáveis inteiras: u_exp, u_imp, u_bm, u_chg, u_dch, u_dl
    Ni = Nt + Nt + (Nt * Nbm) + (Nt * Nbat) + (Nt * Nbat) + (Nt * Ndl)
    
    # Gerando um população inicial para teste
    x = np.random.rand(Nr + Ni)

    # Obtendo as projeções temporais iniciais a partir de um cenário gerado anteriormente
    path = Path(__file__).parent / 'Cenários.pkl'
    cenarios = import_scenarios_from_pickle(path)

    # Acrescentando as projeções ao dicionário data
    for cenario in cenarios:

        data['p_l'] = cenario['p_l']
        data['p_pv'] = cenario['p_pv']
        data['p_wt'] = cenario['p_wt']
        data['tau_pld'] = cenario['tau_pld']
        data['tau_dist'] = cenario['tau_dist']
        data['tau_dl'] = cenario['tau_dl']

    # Teste
    fval = obj_function(x, data)

    print(f' O valor da função objetivo é {fval:.2f}\n')