import numpy as np
from decompose_vetor import decompose

'''
    Este script tem a finalidade de fornecer uma função de restrições de desigualdades de uma VPP a um otimizador (GA), para que o mesmo encontre a solução ótima da função objetivo, sem que haja violação das restrições.

    - Parâmetros de entrada (x: np.ndarray, data: dict):
        - (data: dict): Dicionário contendo os parâmetros iniciais e projeções iniciais temporais.           
             - Parâmetros inicias da VPP:
                - Nt: Período da simulação da VPP;
                - Nbm: Quantidade de usinas de geração à biomassa presentes na VPP;
                - Ndl: Quantidade de cargas despacháveis da VPP;
                - Nbat: Quantidade de armazenadores presentes na VPP;
                - eta_chg: Rendimento de carregamento dos armazenadores da VPP;
                - eta_dch: Rendimento de descarregamento dos armazenadores da VPP;
                - Mimp: Constante de importação da VPP;
                - Mexp: Constante de exportação da VPP;

            - Projeções iniciais da VPP:
                - p_wt: Potência das usinas EOs, shape (Nwt, Nt);
                - p_pv: Potência das usinas FVs, shape (Npv, Nt);
                - p_l: Potência das cargas NÃO despacháveis, shape (Nl, Nt);
                - p_dl_max: Potência máxima das cargas despacháveis da VPP, shape (Ndl, Nt)
                - p_dl_min: Potência mínima das cargas despacháveis da VPP, shape (Ndl, Nt)

        - (x: np.ndarray): Vetor de variáveis de decisão fornecidas pelo otimizador.
            - Variáveis de decisão:
                - p_exp: Potência de exportação da VPP, shape (Nt,);
                - p_imp: Potência de importação da VPP, shape (Nt,);
                - p_bm: Potência das UBTMs da VPP, shape (Nbm, Nt);
                - gamma_bm: Custo máximo das UBTMs, shape (Nbm, Nt);
                - p_dl: Potência das cargas despacháveis da VPP, shape (Ndl, Nt);
                - p_chg: Potência de carregamento dos armazenadores da VPP, shape (Nbat, Nt);
                - p_dch: Potência de descarga dos armazenadores da VPP, shape (Nbar, Nt)
                - soc: Estado de carga (SoC - State fo Charge) dos armazenadroes da VPP;
                - p_dl: Potência das cargas despacháveis da VPP, shape (Ndl, Nt);
                - u_imp: Estado de importação de potência da VPP, shape (Nt,);
                - u_exp: Estado de expportação de potência da VPP, shape (Nt,);
                - u_bm: Estado das UBTMs das VPP, shape (Nbm, Nt);
                - u_chg: Estado do carregamento dos armazenadores da VPP, shape (Nbat, Nt);
                - u_dch: Estado do descarregamento dos armazenadores da VPP, shape (Nbat, Nt);
                - u_dl: Estado das cargas despacháveis da VPP, shape (Ndl, Nt);

    - Retorna (c_ieq: np.ndarray)
        c_ieq: Vetor contendo outros vetores com todas as restrições de desigualdade da VPP.
            - exp_constr: Vetor contendo as restrições de desigualdade de exportação da VPP em cada instante t no período da simulação NT;
            - imp_constr: Vetor contendo as restrições de desigualdade de importação da VPP em cada instante t no período da simulação NT;
            - bm_constr: Vetor contendo as restrições de desigualdade das UBTMs da VPP em cada instante t no período da simulação NT;
            - bat_constr: Vetor contendo as restrições de desigualdade dos armazenadores da VPP em cada instante t no período da simulação NT;
            - dl_constr: Vetor contendo as restrições de desigualdade das cargas despacháveis da VPP em cada instante t no período da simulação NT;
'''

def ieq_constr(x: np.ndarray, data: dict)-> np.ndarray[np.ndarray]:

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
    p_exp, p_imp, p_bm, gamma_bm, p_chg, p_dch, soc, p_dl, u_exp, u_imp, u_bm, u_chg, u_dch, u_dl = decompose(x, data)
    
    Nimpc = Nt # Quantidade de restrições de desigaualdade de importação
    imp_constr = np.zeros(Nimpc) # Vetor de restrições de desigualdade de importação da VPP (imp_constr - import constraints)
    # Definindo as restrições de desigualdade de importação da VPP: (1- u_exp[t]) * Mimp - p_imp[t] >= 0
    for t in range(Nt):
        imp_constr[t] = (1- u_exp[t]) * Mimp - p_imp[t]

    Nexpc = Nt # Quantidade de restrições de desigaualdade de exportação
    exp_constr = np.zeros(Nexpc) # Vetor de restrições de desigualdade de expportação da VPP (exp_constr - export constraints)
    # Calculando as restrições de desigualdade de exportação da VPP: (1- u_imp[t]) * Mexp - p_exp[t] >= 0
    for t in range(Nt):
        exp_constr[t] = (1- u_imp[t]) * Mexp - p_exp[t]
    
    Nbmc = (Nbm * Nt) + (Nbm * Nt) + (Nbm * Nt) + (Nbm * (Nt - 1)) + (Nbm * (Nt - 1)) # Quantidade de restrições de desigualdade das UBTMs
    bm_constr = np.zeros(Nbmc) # Vetor de restrições de desigualdade das UBTMs (bm_constraints)
    k = 0
    # Calculando as restrições de desigualdade das UBTMs da VPP: gamma_bm[i, t] - alpha_bm[i] * p_bm[i, t] - beta_bm[i] >= 0
    for t in range(Nt):
        for i in range(Nbm):
            bm_constr[k] = gamma_bm[i, t] - alpha_bm[i] * p_bm[i, t] - beta_bm[i]
            k += 1
    
    # Calculando a potência mínima das UBTMs: p_bm[i, t] - p_bm_min[i] * u_bm[i, t] >= 0
    for t in range(Nt):
        for i in range(Nbm):
            bm_constr[k] = p_bm[i, t] - p_bm_min[i] * u_bm[i, t]
            k += 1

    # Calculando a potência máxima das UBTMs: p_bm_max[i] * u_bm[i, t] - p_bm[i, t] >= 0
    for t in range(Nt):
        for i in range(Nbm):
            bm_constr[k] = p_bm_max[i] * u_bm[i, t] - p_bm[i, t]
            k += 1

    # Calculando a potência subida das UBTMs: p_bm_rup[i] + p_bm[i, t - 1] - p_bm[i, t] >= 0
    for t in range(1, Nt):
        for i in range(Nbm):
            bm_constr[k] = p_bm_rup[i] + p_bm[i, t - 1] - p_bm[i, t]
            k += 1

    # Calculando a potência descida das UBTMs: p_bm_rdown[i] + p_bm[i, t] - p_bm[i, t - 1] >= 0
    for t in range(1, Nt):
        for i in range(Nbm):
            bm_constr[k] = p_bm_rdown[i] + p_bm[i, t] - p_bm[i, t - 1]
            k += 1

    Nbatc = (Nbat * Nt) + (Nbat * Nt) + (Nbat * Nt) # Quantidade de restrições de desigualdade dos armazenadores
    bat_constr =  np.zeros(Nbatc) # Vetor de restrições de desigualdade dos armazendores (bat_constr - batery constraints)
    k = 0
    # Calculando as restrições de carregamento máximo dos armazenadores: p_bat_max[i] * u_chg[i, t] - p_chg[i, t] >= 0
    for t in range(Nt):
        for i in range(Nbat):
            bat_constr[k] = p_bat_max[i] * u_chg[i, t] - p_chg[i, t]
            k += 1

    # Calculando as restrições de descarregamento máximo dos armazenadores: p_bat_max[i] * u_dch[i, t] - p_dh[i, t] >= 0
    for t in range(Nt):
        for i in range(Nbat):
            bat_constr[k] = p_bat_max[i] * u_dch[i, t] - p_dch[i, t]
            k += 1

    # Calculando as restrições de simultaneidade do estado dos armazenadores: 1 - u_chg[i, t] - u_dch[i, t] >= 0
    for t in range(Nt):
        for i in range(Nbat):
            bat_constr[k] =  1 - u_chg[i, t] - u_dch[i, t]
            k += 1
    
    Ndlc = (Ndl * Nt) + (Ndl * Nt) # Quantidade de restrições de desigualdade das cargas despacháveis
    dl_constr = np.zeros(Ndlc) # Vetor de restrições de desigualdade das cargas despacháveis (dl_constr - dload constraints)
    k = 0
    # Calculando as restrições de potência mínima das cargas despacháveis: p_dl[i, t] - p_dl_min[i] * u_dl[i, t] >= 0
    for t in range(Nt):
        for i in range(Ndl):
            dl_constr[k] = p_dl[i, t] - p_dl_min[i, t] * u_dl[i, t]
            k += 1

    # Calculando as restrições de potência máxima das cargas despacháveis: p_dl_max[i] * u_dl[i, t] - p_dl[i, t] >= 0
    for t in range(Nt):
        for i in range(Ndl):
            dl_constr[k] = p_dl_max[i, t] * u_dl[i, t] - p_dl[i, t]
            k += 1

    # Vetor com todas as restrições de desigualdade da VPP
    c_ieq = np.concatenate((imp_constr,
                                 exp_constr,
                                 bm_constr,
                                 bat_constr,
                                 dl_constr
                                 ))

    return c_ieq

# Exemplo de uso
if __name__ == '__main__':

    from decompose_vetor import decompose
    from generator_scenarios import import_scenarios_from_pickle
    from pathlib import Path
    from vpp_data import vpp_data

    # Obtendo as projeões inicias
    data = vpp_data()
    data['Nt'] = 24
    Nt = data['Nt']
    Ndl = data['Ndl']
    Nbm = data['Nbm']
    Nbat = data['Nbat']

    # Definindo a quantidade de variáveis reais (Nr) e variáveis inteiras (Ni)
    # p_exp, p_imp, p_bm, gamma_bm, p_chg, p_dch, soc, p_dl
    Nr = Nt + Nt + (Nt * Nbm) + (Nt * Nbm) + (Nt * Nbat) + (Nbat * Nt) + (Nt * Nbat) + (Nt * Ndl)
    # u_exp, u_imp, u_bm, u_chg, u_dch, u_dl
    Ni = Nt + Nt + (Nt * Nbm) + (Nt * Nbat) + (Nt * Nbat) + (Nt * Ndl)

    # Gerando um população inicial de indivíduos
    x = np.random.rand(Nr + Ni)

    # Obtendo as projeções a partir de cenários gerados anteriormente
    path = Path(__file__).parent / 'Cenários.pkl'
    cenarios = import_scenarios_from_pickle(path)

    # Acrescentando as projeções iniciais ao dicionário data
    for cenario in cenarios:

        data['p_l'] = cenario['p_l']
        data['p_pv'] = cenario['p_pv']
        data['p_wt'] = cenario['p_wt']
        data['p_dl_max'] = cenario['p_dl_max']
        data['p_dl_min'] = cenario['p_dl_min']

    # Teste
    constr = ieq_constr(x, data)

    print(f'bm_contraints shape {constr.shape} and type {type(constr)}\n{constr}')
