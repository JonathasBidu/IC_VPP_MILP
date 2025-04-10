import numpy as np

'''
    Este script tem a finalidade de fornecer a um otimizador os limites máximo e mínimo que as variáveis de decisão podem assumir em cada iteração t no período da simulação Nt.

        - Parâmetros de entrada: (data: dict):
            - data: Dicionário contendo os parâmetros iniciais, projeções iniciais temporais e variáveis de decisão fornecidas pelo otimizador.

                -Projeções iniciais:
                    - Nt: Período da simulação da VPP;
                    - Nbm: Quantidade de usinas de geração à biomassa presentes na VPP;
                    - Ndl: Quantidade de cargas despacháveis presentes na VPP;
                    - Nbat: Quantidade de armazendores presentes na VPP;
                    - soc_max: SoC máximo bateria, shape (Nbat,);
                    - soc_min: SoC mínimo bateria, shape (Nbat,);
                    - p_bat_max: Potênica de carregamento/descarregamento dos armazenadores da VPP, shape (Nbat,);
                    - p_bm_min: Potênica mínima das UBTMs da VPP, shape (NBM,);
                    - p_bm_max: Potênica máxima das UBTMs da VPP, shape (NBM,);
                    - kappa_bm: tarifa de custo operacional das UBTMs da VPP, shape (Nbm,);

                - Projeções temporais iniciais:
                    - p_l: Potência das cargas NÂO despacháveis da VPP, shape (Npv, Nt);
                    - p_pv: Potência das usinas solares (FVs) da VPP, shape (Npv, Nt);
                    - p_wt: Potência das usinas eólicas (EOs) da VPP, shape (Npv, Nt);
                    - p_dl_max: Potência máxima despachável carga, shape (Ndl,)
                    - p_dl_min: Potência mínima despachável carga, shape (Ndl,)

                - Variável de decisão:
                    - p_bm: Potência da usinas de geração à biomassa (UBTMs) da VPP, shape (Nbm, Nt);

    - Retorna upper_bounds, lower_bounds:
        - upper_bonds: Vetor de limites superiores das variáveis de decisão
        - lower_bonds: Vetor de limites inferiores das variáveis de decisão        
'''

def bounds(data: dict)-> tuple[np.ndarray]:

    # Parâmetros iniciais da VPP
    Nt = data['Nt'] # Período da simulação da VPP
    Nbm = data['Nbm'] # Quantidade de UBTMs
    Ndl = data['Ndl'] # Quantidade de carga despacháveis
    Nbat = data['Nbat'] # Quantidade de armazenadores

    # Parâmetros das UBTMs
    # p_bm = data['p_bm'] # Potênica das UBTMs
    p_bm_min = data['p_bm_min'] # Potênica mínima das UBTMs
    p_bm_max = data['p_bm_max'] # Potênica máxima das UBTMS
    kappa_bm = data['kappa_bm'] # Tarifa operacional das UBTMs

    # Parâmetros das UBTMs
    p_bat_max = data['p_bat_max'] # Potênica máxima de carregamento/descarregamento dos armazenadores 
    soc_min = data['soc_min'] # Nível mínimo de carga da bateria
    soc_max = data['soc_max'] # Nível máximo de carga da bateria

    # Parâmetro das cargas despacháveis
    p_dl_max = data['p_dl_max'] # Potência mínima despachável carga
    p_dl_min = data['p_dl_min'] # Potência mínima despachável carga

    # Parâmetro das usinas solares
    p_pv = data['p_pv'] # Potência das usinas solares

    # Parâmetro das usinas eólicas
    p_wt = data['p_wt'] # Potência das usinas eólicas

    # Parâmetro das cargas não despacháveis
    p_l = data['p_l'] # Potência da cargas NÂO despacháveis

    # Calculando a potência instalada no instante t no período da simulação Nt
    p_inst = np.zeros(Nt) # Vetor de potência instalada em cada instante t
    for t in range(Nt):
        p_inst[t] = np.sum(p_pv[:, t]) + np.sum(p_wt[:, t]) + np.max(soc_max) + np.max(p_bm_max)

    # Calculando a carga demandada no instante t no período da simulação Nt
    demanded_load = np.zeros(Nt) # Vetor de carga demandada em cada instante t
    for t in range(Nt):
        demanded_load[t] = np.sum(p_l[:, t]) - np.max(soc_min)

    # Definindo a quantidade de variáveis reais (Nr) e inteiras (Ni)
    Nr =  Nt + Nt + (Nt * Nbm) + (Nt * Nbm) + (Nt * Nbat) + (Nbat * Nt) + (Nt * Nbat) + (Nt * Ndl)
    Ni = Nt + Nt + (Nt * Nbm) + (Nt * Nbat) + (Nt * Nbat) + (Nt * Ndl)

    # Iniciando os vetores limitadores superior e inferior das variáveis de decisão
    upper_bounds = np.ones(Nr + Ni)
    lower_bounds = np.zeros(Nr + Ni)
    k = 0

    # Limite de p_exp
    for t in range(Nt):
        upper_bounds[k] = p_inst[t]
        lower_bounds[k] = 0
        k += 1

    # Limite de p_imp
    for t in range(Nt):
        upper_bounds[k] = demanded_load[t]
        lower_bounds[k] = 0
        k += 1

    # Limite de p_bm
    for t in range(Nt):
        for i in range(Nbm):
            upper_bounds[k] = p_bm_max[i]
            lower_bounds[k] = p_bm_min[i]
            k += 1

    # Limite de gamma_bm
    for t in range(Nt):
        for i in range(Nbm):
            upper_bounds[k] = p_bm_max[i] * kappa_bm[i]
            lower_bounds[k] = p_bm_min[i] * kappa_bm[i]
            k += 1

    # Limite de p_chg
    for t in range(Nt):
        for i in range(Nbat):
            upper_bounds[k] = p_bat_max[i]
            lower_bounds[k] = 0
            k += 1

    # Limite de p_dch
    for t in range(Nt):
        for i in range(Nbat):
            upper_bounds[k] = p_bat_max[i]
            lower_bounds[k] = 0
            k += 1

    # Limite de soc
    for t in range(Nt):
        for i in range(Nbat):
            upper_bounds[k] = soc_max[i]
            lower_bounds[k] = soc_min[i]
            k += 1
 
    # Limite de p_dl
    for t in range(Nt):
        for i in range(Ndl):
            upper_bounds[k] = p_dl_max[i, t]
            lower_bounds[k] = p_dl_min[i, t]
            k += 1


    # u_exp, u_imp, u_bm, u_chg, u_dch, u_dl: upper_bounds = 1 and lower_bounds = 0

    return upper_bounds, lower_bounds

# Exemplo de uso
if __name__ == '__main__':

    from vpp_data import vpp_data
    from decompose_vetor import decompose
    from generator_scenarios import import_scenarios_from_pickle
    from pathlib import Path

    # Obtenção dos parâmetros iniciais
    data = vpp_data()
    data['Nt'] = 24
    Nt = data['Nt']
    Ndl = data['Ndl']
    Nbm = data['Nbm']
    Nbat = data['Nbat']

    # Definindo a quantidade de variáveis reais (Nr) e variáveis inteiras (Ni)
    # p_exp, p_imp, p_bm, gamma_bm, p_chg, p_dch, p_dl
    Nr = Nt + Nt + (Nt * Nbm) + (Nt * Nbm) + (Nt * Nbat) + (Nbat * Nt) + (Nt * Nbat) + (Nt * Ndl)
    # u_exp, u_imp, u_bm, u_chg, u_dch, u_dl
    Ni = Nt + Nt + (Nt * Nbm) + (Nt * Nbat) + (Nt * Nbat) + (Nt * Ndl)

    # Gerando um poppulação inicial para teste
    x = np.random.rand(Nr + Ni)

    # Decompondo a população em variáveis de decisão
    p_exp, p_imp, p_bm, gamma_bm, p_chg, p_dch, soc, p_dl, u_exp, u_imp, u_bm, u_chg, u_dch, u_dl = decompose(x, data)

    # Acrescentando  as variáveis de decisão ao dicionário data
    data['p_exp'] = p_exp
    data['p_imp'] = p_imp
    data['p_bm'] = p_bm
    data['gamma_bm'] = gamma_bm
    data['p_chg'] = p_chg
    data['p_dch'] = p_dch
    data['soc'] = soc
    data['p_dl'] = p_dl    
    data['u_exp'] = u_exp
    data['u_imp'] = u_imp
    data['u_bm'] = u_bm
    data['u_chg'] = u_chg
    data['u_dch'] = u_dch
    data['u_dl'] = u_dl


    # Obtendo as projeções temporais iniciais
    path = Path(__file__).parent / 'Cenários.pkl'
    cenarios = import_scenarios_from_pickle(path)

    # Acrescentando as projeções ao dicionário data
    for cenario in cenarios:

        data['p_l'] = cenario['p_l']
        data['p_pv'] = cenario['p_pv']
        data['p_wt'] = cenario['p_wt']
        data['p_dl_max'] = cenario['p_dl_max']
        data['p_dl_min'] = cenario['p_dl_min']

    # Teste
    upper_bounds, lower_bounds = bounds(data)

    print(f'upper_bounds shape {upper_bounds.shape} and types {type(upper_bounds)}\n{upper_bounds}\n')
    print(f'lower_bounds shape {lower_bounds.shape} and types {type(lower_bounds)}\n{lower_bounds}\n')
