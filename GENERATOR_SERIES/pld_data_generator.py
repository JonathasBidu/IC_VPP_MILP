import pandas as pd
import numpy as np
from pathlib import Path

""" 
    SCRIPT PARA GERAÇÃO DE SÉRIES DE PLD(PREÇO DE LIQUIDAÇÃO DE DIFERENÇA) A PARTIR DE UM HISTÓRICO DE PREÇOS.
    FONTE DOS DADOS: <>
"""

# Caminho das séries históricas
path = Path(__file__).parent / 'BASE_DE_DADOS' / 'Historico_do_Preco_Horario(SE)_-_17_de_abril_de_2018_a_5_de_abril_de_2022.xlsx'

# Importando a tabela PLD e convertendo em séries históricas
PLD_Table = pd.read_excel(path, header = None)


# Obtendo os dados das 24 linhas(horas) e das 1437 colunas e atribuindo na váriavel Daily_PLD
Daily_PLD = PLD_Table.iloc[1: 25, 2:] # Período de 24 horas

# Obtendo as dimensões da matriz M = 24 linhas e N = 1437 colunas
M, N = Daily_PLD.shape

# Transformando os dados obtidos acima em vetor coluna(série temporal)
PLD_daily_tsdata = Daily_PLD.values.reshape((M * N, 1)) 
# Obtendo o tamanho da série temporal por ano
len_pld_timeseries = len(PLD_daily_tsdata) # 345122
# Variável com a quantidades de horas em um ano 24h x 365 = 8760h
Npoints = 8760
# Obtendo a quantidade de cenários(anos) em um número inteiro
Nscenarios = len_pld_timeseries // Npoints
# Criando uma matriz preenchida com zeros com dimenões Ncenários x Npoints
PLD_hourly_series = np.zeros((Nscenarios, Npoints))

for s in range(Nscenarios):
    inicio = Npoints * s
    fim = Npoints * (s + 1)
    PLD_hourly_series [s, :] = PLD_daily_tsdata[inicio: fim].flatten()

# Salvar o DataFrame em um arquivo CSV, Excel ou outro formato
PLD_hourly_df = pd.DataFrame(PLD_hourly_series)
path = Path(__file__).parent.parent / 'SERIES_GERADAS' / 'PLD_hourly_series.csv'
PLD_hourly_df.to_csv(path, index = False, sep = ';', header = None)

# Visualização da série de PLD
if __name__ == '__main__':

    import matplotlib.pyplot as plt

    for i in range(PLD_hourly_series.shape[0]):

        plt.plot(PLD_hourly_series[i, :24])
        plt.title(f'Série {i + 1}')
        plt.show()
