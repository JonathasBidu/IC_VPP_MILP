import numpy as np
import pandas as pd
from pathlib import Path

'''
    Script com os dados gerais da VPP 1
    Adaptado de zhou2016_Optimal scheduling of virtual power plant with
    battery degradation cost

'''
'''
    Este script contém os dados gerais de uma Virtual Power Plant (VPP) e gera um arquivo CSV com as informações de entrada para a simulação de operação de uma VPP.

    -> Estrutura de Dados:
        - Nbm: Número de usinas de biomassa.
        - p_bm_min: Potência mínima das usinas de biomassa (MW).
        - p_bm_max: Potência máxima das usinas de biomassa (MW).
        - p_bm_rup: Potência de ramp-up das usinas de biomassa (MW).
        - p_bm_rdown: Potência de ramp-down das usinas de biomassa (MW).
        - kappa_bm: Custo de operação das usinas de biomassa (R$/kWh).
        - kappa_bm_start: Custo de partida das usinas de biomassa (R$/kWh).

    - Npv: Número de usinas fotovoltaicas.
    - kappa_pv: Custo de operação das usinas fotovoltaicas (R$/kWh).

    - Nwt: Número de usinas eólicas.
    - kappa_wt: Custo de operação das usinas eólicas (R$/kWh).

    - Nbat: Número de sistemas de armazenamento de energia.
    - eta_chg: Eficiência do sistema de armazenamento durante o carregamento (%).
    - eta_dch: Eficiência do sistema de armazenamento durante a descarga (%).
    - soc_min: Nível mínimo de carga das baterias (%).
    - soc_max: Nível máximo de carga das baterias (%).
    - p_bat_max: Potência máxima das baterias (MW).
    - kappa_bat: Custo de operação das baterias (R$/kWh).

    - Ndl: Número de cargas despacháveis.
    - Nl: Número de cargas não despacháveis.

    -> Objetivo:
        A função `vpp_data()` cria um dicionário `vpp_data` contendo os parâmetros gerais da VPP, converte esses dados em um `DataFrame` e salva o arquivo CSV com esses parâmetros. 

    -> Parâmetros de Entrada:
        Nenhum parâmetro é requerido diretamente pela função.

    -> Saída:
        - vpp_data (dict): Dicionário contendo todos os parâmetros de configuração da VPP.
        - Um arquivo CSV chamado "VPPDATA.csv" é gerado no mesmo diretório do script, contendo os dados da VPP.

    -> Observações:
        - A função `vpp_data()` cria e salva os parâmetros da VPP no formato CSV para facilitar o carregamento e simulação em outros módulos do projeto.
        - Os custos de operação das usinas de biomassa, fotovoltaicas, eólicas e de baterias são valores arbitrários definidos no script.

'''

path = Path(__file__).parent

def vpp_data():

    vpp_data = {}

    #  dados usina biomassa
    vpp_data['Nbm'] = 3
    vpp_data['p_bm_min'] = np.array([0.1, 0.1, 0.1]) # Potência mínima (MW)
    vpp_data['p_bm_max'] = np.array([0.5, 0.5, 0.5]) # Potência máxima (MW)
    vpp_data['p_bm_rup'] = np.array([0.5 , 0.5, 0.5]) # Potência de ramp-up (MW)
    vpp_data['p_bm_rdown']  = np.array([0.5, 0.5, 0.5]) # Potência de ramp-down (MW)
    vpp_data['kappa_bm'] = np.array([0.025, 0.025, 0.025]) # Custo de operação (R$/kWh)		
    vpp_data['kappa_bm_start'] = np.array([10.14, 10.14, 10.14]) # Custo de partida(R$/kWh)

    # dados usina FV
    vpp_data['Npv'] = 4
    vpp_data['kappa_pv'] = np.array([0.022, 0.022, 0.022, 0.022])

    # dados usina Eolica
    vpp_data['Nwt'] = 2
    vpp_data['kappa_wt'] = np.array([0.027, 0.027])

    # dados sistema de armazenamento
    vpp_data['Nbat'] = 2
    vpp_data['eta_chg'] = np.array([0.914, 0.914]) # Eficiência da bateria no carregamento (%)
    vpp_data['eta_dch'] = np.array([0.914, 0.914]) # Eficiência da bateria na descarga (%)
    vpp_data['soc_min'] = np.array([0.50, 0.50]) # Nível de carga mínima (MW)
    vpp_data['soc_max'] = np.array([0.75, 0.75]) # Nível de carga máximo (MW)
    vpp_data['p_bat_max']  = np.array([0.1, 0.1]) # Potência máxima da bateria (MW)
    vpp_data['kappa_bat']  = np.array([0.038, 0.038]) # Custo de operação (R$/kWh)
    # OBS: custos da eólica, FV e bateria arbitrados

    # dados cargas despachaveis
    vpp_data['Ndl'] = 2
    
    # dados cargas nao despachaveis
    vpp_data['Nl'] = 3

    keys = [i for i in vpp_data.keys()]
    values = [i for i in vpp_data.values()]
    VPP_DATA = list(zip(keys, values))
    VPP_DATA_DF = pd.DataFrame(VPP_DATA, columns = ['keys', 'values'])
    VPP_DATA_DF.to_csv(path / 'VPP_DATA.csv', sep = ';', index = False)

    return vpp_data

# Exemplo de uso
if __name__ == '__main__':

    vpp_data()