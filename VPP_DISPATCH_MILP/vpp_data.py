import numpy as np
import pandas as pd
from pathlib import Path

'''
    Script com os dados gerais da VPP 1
    Adaptado de zhou2016_Optimal scheduling of virtual power plant with
    battery degradation cost

'''

path = Path(__file__).parent

def vpp_data():

    vpp_data = {}

    #  dados usina biomassa
    vpp_data['Nbm'] = 2
    vpp_data['p_bm_min'] = np.array([0.1, 0.15]) # Potência mínima (MW)
    vpp_data['p_bm_max'] = np.array([1.5, 2.5]) # Potência máxima (MW)
    vpp_data['p_bm_rup'] = np.array([0.5 , 0.5]) # Potência de ramp-up (MW)
    vpp_data['p_bm_rdown']  = np.array([0.5, 0.5]) # Potência de ramp-down (MW)
    vpp_data['kappa_bm'] = np.array([0.85, 0.85]) # Custo de operação (R$/kWh)		
    vpp_data['kappa_bm_start'] = np.array([20.14, 20.14]) # Custo de partida(R$/kWh)

    # dados usina FV
    vpp_data['Npv'] = 3
    vpp_data['kappa_pv'] = np.array([0.022, 0.022, 0.22])

    # dados usina Eolica
    vpp_data['Nwt'] = 3
    vpp_data['kappa_wt'] = np.array([0.027, 0.027, 0.027])

    # dados sistema de armazenamento
    vpp_data['Nbat'] = 1
    vpp_data['eta_chg'] = np.array([0.914]) # Eficiência da bateria no carregamento (%)
    vpp_data['eta_dch'] = np.array([0.914]) # Eficiência da bateria na descarga (%)
    vpp_data['soc_min'] = np.array([0.50]) # Nível de carga mínima (MW)
    vpp_data['soc_max'] = np.array([0.75]) # Nível de carga máximo (MW)
    vpp_data['p_bat_max']  = np.array([0.75]) # Potência máxima da bateria (MW)
    vpp_data['kappa_bat']  = np.array([0.038]) # Custo de operação (R$/kWh)
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