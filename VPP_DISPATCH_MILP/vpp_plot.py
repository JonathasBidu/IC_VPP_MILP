import numpy as np
from matplotlib import pyplot as plt

'''
    Este script tem a finalidade de mostrar graficamente as projeções e os despachos otimizados de uma VPP.

        - Parâmetros de entrada:
            - (data: dict): dicionário contendo os parâmetros iniciais, as projeções temporais iniciais e os desapchos da solução ótima encotrada pelo otimizador (GA).
                - Nt: Período da simulação da VPP;
                - Nl: Quantidade de carga NÃO despachável da VPP;
                - Ndl: Quantidade de carga despachável da VPP;
                - Nbm: Quantidade de usinas de geração à biomassa (UBTMs) da VPP;
                - Nwt: Quantidade de usinas eólicas (EOs) da VPP;
                - Npv: Quantidade de usinas solares (FVs) da VPP;
                - Nbat: Quantidade de armazenadores (SAs) da VPP;

        - Retorna (None): Não há retorno nessa função.
'''

def plot(data: dict)-> None:

    # Parâmetros iniciais da VPP
    Nt = data['Nt']
    Nbm = data['Nbm']
    Npv = data['Npv']
    Nwt = data['Nwt']
    Ndl = data['Ndl']
    Nbat = data['Nbat']

    # Parâmetros das UBTMs
    p_bm = data['p_bm']
    p_bm_max = data['p_bm_max']
    p_bm_min = data['p_bm_min']
    u_bm = data['u_bm']

    # Parâmetros dos SAs
    p_dch = data['p_dch']
    p_chg = data['p_chg']
    u_dch = data['u_dch']
    u_chg = data['u_chg']
    soc = data['soc']
    soc_min = data['soc_min']
    soc_max = data['soc_max']
    p_bat_max = data['p_bat_max']

    # Cargas despachaveis        
    p_dl = data['p_dl']
    p_dl_ref = data['p_dl_ref']
    p_dl_min = data['p_dl_min']
    p_dl_max = data['p_dl_max']

    # Projeções das FVs
    p_pv = data['p_pv']

    # Projeções das EOs
    p_wt = data['p_wt']

    # Vetor temporal do período da simulação
    t = np.arange(Nt)

    # Plotagem das UBMTs
    for i in range(Nbm):
        
        title = f'Usina de Biomassa {i + 1}' 
        plt.figure(figsize = (10, 5))
        plt.plot(t, p_bm[i, :], 'b')
        plt.plot(t, np.ones(Nt) * p_bm_max[i], '--r')
        plt.plot(t, np.ones(Nt) * p_bm_min[i], '--r')
        plt.title(title)
        plt.xlabel('Hora')
        plt.ylabel('Potência em MW')
        plt.legend(['p_bm', 'max', 'min'])
        plt.show()

        title = f'Estado da usina de Biomassa {i + 1}' 
        plt.figure(figsize = (10, 5))
        plt.bar(t, u_bm[i, :], color=['gray' if v == 0 else 'green' for v in u_bm[i, :]], width=1, edgecolor='black', align = 'edge')
        plt.title(title)
        plt.xlabel('Hora')
        plt.yticks([0, 1], ['Off', 'On'])
        plt.show()



    # Potagem dos SAs
    for i in range(Nbat):

        title_name = f'Carga Bateria {i + 1}'
        plt.figure(figsize = (10, 4))
        plt.plot(t, p_bat_max[i] * np.ones(Nt), 'b--')
        plt.step(t, p_chg[i,:] * u_chg[i,:], 'r')
        plt.title(title_name)
        plt.xlabel('Hora')
        plt.ylabel('Potência')
        plt.legend(['max', 'load'])
        plt.show()

        title_name = f'Descarga Bateria {i + 1}'
        plt.figure(figsize = (10, 4))
        plt.plot(t, p_bat_max[i] * np.ones(Nt), 'b--')
        plt.step(t, p_dch[i,:] * u_dch[i,:], 'r')
        plt.title(title_name)
        plt.xlabel('Hora')
        plt.ylabel('Potência')
        plt.legend(['max', 'discharge'])
        plt.show()

        title_name = f'Soc Bateria {i + 1}'
        plt.figure(figsize = (10, 4))
        plt.plot(t, soc_min[i] * np.ones(Nt) , 'b--')
        plt.plot(t, soc_max[i] * np.ones(Nt) , 'b--')
        plt.step(t, soc[i,:], 'r')
        plt.title(title_name)        
        plt.xlabel('Hora')
        plt.ylabel('Carga')
        plt.legend(['min', 'max', 'soc'])
        plt.show()

    # plotagem das cargas despacháveis
    for i in range(Ndl):

        title_name = f'Cargas despachaveis {i + 1}'
        plt.figure(figsize = (10, 4))
        plt.plot(t, p_dl_ref[i,:], 'r')
        plt.plot(t, p_dl_min[i,:], 'b--')
        plt.plot(t, p_dl_max[i,:], 'b--')
        plt.plot(t, p_dl[i,:], 'k')
        plt.title(title_name)
        plt.xlabel('hora')
        plt.ylabel('Potência em MW')
        plt.legend(['ref', 'min', 'max', 'desp'])
        plt.show()

    # Plotagem das FVs
    for i in range(Npv):

        title_name = f'Usina Solar FV {i + 1}'
        plt.figure(figsize = (10, 4))
        plt.plot(t, p_pv[i], 'r')
        plt.title(title_name)
        plt.xlabel('hora')
        plt.ylabel('Potência em MW')
        plt.show()

    # Plotagem das EOs
    for i in range(Nwt):

        title_name = f'Usina Eólica {i + 1}'
        plt.figure(figsize = (10, 4))
        plt.plot(t, p_wt[i], 'r')
        plt.title(title_name)
        plt.xlabel('hora')
        plt.ylabel('Potência em MW')
        plt.show()

    # Despachos de importação e exportação
    p_exp = data['p_exp']
    p_imp = data['p_imp']
    u_exp = data['u_exp']
    u_imp = data['u_imp']

    # Potagem de Imprtação e exportação
    fig, ax = plt.subplots(2, 1, figsize = (10, 5), sharex = True)

    ax[0].plot(t, p_imp, 'r', label="Potência Importada (MW)")
    ax[0].set_title('Importação')
    ax[0].set_ylabel('Potência em MW')

    ax[1].plot(t, p_exp, 'b', label="Potência Importada (MW)")
    ax[1].set_title('Exportação')
    ax[1].set_xlabel('Hora')
    ax[1].set_ylabel('Potência em MW')
    plt.show()

    fig, ax = plt.subplots(2, 1, figsize = (10, 5), sharex = True)

    ax[0].bar(t, u_imp, color = ['gray' if v == 0 else 'red' for v in u_imp], width = 1, edgecolor = 'black', align='edge')
    ax[0].set_title('Estado de Importação')
    ax[0].set_yticks([0, 1])
    ax[0].set_yticklabels(['Off', 'On'])

    ax[1].bar(t, u_exp, color = ['gray' if v == 0 else 'blue' for v in u_exp], width = 1, edgecolor = 'black', align='edge')
    ax[1].set_title('Estado de Exportação')
    ax[1].set_xlabel('Hora')
    ax[1].set_yticks([0, 1])
    ax[1].set_yticklabels(['Off', 'On'])
    plt.show()
