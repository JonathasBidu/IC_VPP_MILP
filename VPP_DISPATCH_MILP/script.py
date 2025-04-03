from generator_scenarios import import_scenarios_from_pickle
from decompose_vetor import decompose
from optimazer_GA import solver
from vpp_data import vpp_data
from vpp_plot import plot
from pathlib import Path

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

data = vpp_data()
data['Nt'] = Nt
Nbm = data['Nbm']

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
res = solver(data)

# Obtendo o vetor de soluções da VPP
x = res.X

if x is not None:

    # Decompondo o vetor de soluções nas suas variáveis de decisão
    data['p_exp'], data['p_imp'], data['p_bm'], data['gamma_bm'], data['p_chg'], data['p_dch'], data['soc'], data['p_dl'], data['u_exp'], data['u_imp'], data['u_bm'], data['u_chg'], data['u_dch'], data['u_dl'] = decompose(x, data)

    # Visualizando o despacho otimizado da VPP
    plot(data)
    print('\n')
    print(f'O lucro dessa simulação foi de aproximadamente {res.F[0]:.2f}\n')
    print(f'O total de violações dessa simulação foi de {res.CV[0]:.2f}\n')

else:
    print('Não foi encontrado solução para essa simulação')