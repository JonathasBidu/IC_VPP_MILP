from generator_scenarios import import_scenarios_from_pickle
from decompose_vetor import decompose
from vpp_initial_data import vpp_data
from optimazer_GA import solver
from vpp_plot import plot
from pathlib import Path
import numpy as np

'''
    Este script tem a finalidade de simular uma Virtual Power Plant (VPP) e obter despachos otimizados visando o lucro.
'''

# Definindo o período da simulação da VPP
while True:
    Nt = input('Insira o período da simulação ou tecle enter para 24h: ')
    if Nt == '':
        Nt = 24
        break
    try:
        Nt = int(Nt)
        if Nt > 0:
            break
        else:
            print('Insira um valor inteiro e positivo')
    except ValueError as v:
        print(f'Insira um valor inteiro e positivo! {v}')

# Definindo a capacidade instalada das Usina Solares
while True:
    cap_pv = input('Insira a capacidade das Usinas Solares em p.u. ou tecle enter para 2.75 p.u.: ')
    if cap_pv == '':
        cap_pv = 2.75
    try:
        cap_pv = float(cap_pv)
        if cap_pv > 0:
            break
        else:
            print('Insira um valor real positivo!')
    except ValueError as v:
        print('Insira um valor númerico válido!')

# Definindo a capacidade instalada das Usina Eólicas
while True:
    cap_wt = input('Insira a capacidade das Usinas Eólicas em p.u. ou tecle enter para 10.0 p.u.: ')
    if cap_wt == '':
        cap_wt = 10.0     
    try:
        cap_wt = float(cap_wt)
        if cap_wt > 0:
            break
        else:
            print('Insira um valor real positivo!')
    except ValueError as v:
        print('Insira um valor númerico válido!')

# Definindo a capacidade instalada das Cargas
while True:
    cap_load = input('Insira a capacidade das Cargas em p.u. ou tecle enter para 1 p.u.: ')
    if cap_load == '':
        cap_load = 1.0
    try:
        cap_load = float(cap_load)
        if cap_load > 0:
            break
        else:
            print('Insira um valor real positivo!')
    except ValueError as v:
        print('Insira um valor númerico válido!')

# Definindo o limite de corte de carga
while True:
    delta = input(f'Insira o limite inferior e superior de corte de carga ((%) acima  e abaixo da referência) ou tecle enter para 20 %: ')
    print('')
    if delta == '':
        delta = 0.2
    try:
        delta = float(delta)
        if delta >= 0:
            break
        else:
            print('Insira um valor real e positivo')
    except ValueError as v:
        print(f'Insira um valor numérico e válido {v}')

# Carregamento de dados iniciais da VPP
data = vpp_data()
data['Nt'] = Nt
Nbm = data['Nbm']
Nbat = data['Nbat']

path = Path(__file__).parent / 'scenarios_with_PVGIS.pkl'
cenarios = import_scenarios_from_pickle(path)
idx = np.random.choice(len(cenarios))
cenario = cenarios[idx]

# Definindo a quantidade de cenários da simulação
while True:
    Ns = input('Insira a quantidade de cenários desejados ou tecle enter para 1 cenário: ')
    if Ns == '':
        Ns = 1
        break
    try:
        Ns = int(Ns)
        if Ns > 0:
            break
        else:
            print('Insira um valor inteiro e positivo')
    except ValueError as v:
        print('Insira um valor numérico e válido')

data['p_l'] = cenario['p_l']
data['p_pv'] = cenario['p_pv']
data['p_wt'] = cenario['p_wt']
data['p_dl_ref'] = cenario['p_dl_ref']
data['tau_pld'] = cenario['tau_pld']
data['tau_dist'] = cenario['tau_dist']
data['tau_dl'] = cenario['tau_dl']

# Ajustando as potências pelas capacidades instaladas (em p.u)
p_l = data['p_l'] * cap_load
p_pv = data['p_pv'] * cap_pv
p_wt = data['p_wt'] * cap_wt
p_dl_ref = data['p_dl_ref'] * cap_load

#  Definindo banda de corte de carga baseado no percentual fornecido
data['p_dl_max'] = data['p_dl_ref'] + data['p_dl_ref'] * delta
data['p_dl_min'] = data['p_dl_ref'] - data['p_dl_ref'] * delta

# Obtendo a solução do otimizador (GA)
res = solver(data)

# Obtendo o vetor de soluções da VPP
x = res.X # Matriz de soluções ótimas
G = res.G # Matriz de restrições de desigualdades
# H = res.H # Matriz de restrições de igualdades

if x is not None:

    import numpy as np

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

    print(f'\nBalanço de potência\n{pwr_blc_contr}\n')
    print(f'\nNão simultaneidade\n{simult_constr}\n')
    print(f'\nEstado de carga\n{soc_constr}\n')

    # Visualizando o despacho otimizado da VPP
    plot(data)
    print('\n')
    print(f'O lucro dessa simulação foi de aproximadamente {res.F[0]:.2f}\n')
    # print(f'O total de violações dessa simulação foi de {res.CV[0]:.2f}\n')
    # print(f'{simult_constr}')

    # print(f'\nu_imp {data['u_imp']}\n')
    # print(f'u_exp {data['u_exp']}')
    # print(data['p_exp'])
    # print(data['p_imp'])
else:
    print(f'\nNão foi encontrado solução para essa simulação\n')