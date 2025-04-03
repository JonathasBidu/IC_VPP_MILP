import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

'''
    Este programa coleta dados de irradiação solar (G(i)) e temperatura (T2m) de três cidades
    (Búzios, Niterói e Angra dos Reis) para visualização e armazenamento em uma planilha Excel,
    organizada em abas por cidade. A primeira semana (168 horas) dos dados de irradiação e temperatura
    é visualizada por meio de gráficos.
    fonte: https://pvgis.com/

'''

# Obtendo os caminhos das bases de dados
# path_1 = "C:\\Users\\Jonathas Aguiar\\Desktop\\IC_VPP_II\\GERADORES_DE_SERIES\\BASE_DE_DADOS\\solar_time_series_buzios.csv"
path_1 = Path(__file__).parent / "BASE_DE_DADOS" / "solar_time_series_buzios.csv"
# path_2 = 'C:\\Users\\Jonathas Aguiar\\Desktop\\IC_VPP_II\\GERADORES_DE_SERIES\\BASE_DE_DADOS\\solar_time_seires_niteroi.csv'
path_2 = Path(__file__).parent / "BASE_DE_DADOS" / "solar_time_seires_niteroi.csv"
# path_3 = "C:\\Users\\Jonathas Aguiar\\Desktop\\IC_VPP_II\\GERADORES_DE_SERIES\\BASE_DE_DADOS\\solar_time_series_angra_dos_reis.csv"
path_3 = Path(__file__).parent / "BASE_DE_DADOS" / "solar_time_series_angra_dos_reis.csv"
# Obtendo os dados de irradiâcia e temperatura
buzio_time_series = pd.read_csv(path_1, skiprows = 8, nrows = 8760, sep = ',', usecols = ['G(i)', 'T2m'])
niteroi_time_series = pd.read_csv(path_2, skiprows = 8, nrows = 8760, sep = ',', usecols = ['G(i)', 'T2m'])
angra_time_series = pd.read_csv(path_3, skiprows = 8, nrows = 8760, sep = ',', usecols = ['G(i)', 'T2m'])

# Transformando os DataFrame em matrizes numpy
buzio_tsdata = buzio_time_series.to_numpy()[3: ,]
niteroi_tsdata = niteroi_time_series.to_numpy()[3: ,]
angra_tsdata = angra_time_series.to_numpy()[3: ,]

# gráfico da irradiânica nas primeiras 168 horas (1 semana)
plt.figure(figsize = (10, 5))
plt.title('Irradiância')
plt.plot(buzio_tsdata[: 168, 0])
plt.plot(niteroi_tsdata[: 168, 0])
plt.plot(angra_tsdata[: 168, 0])
plt.xlabel('hora')
plt.ylabel('magnitude')
plt.legend(['Búzios', 'Niterói', 'Angra'])
plt.show()

# gráfico da temperatura das primeiras 168 horas (1 semana)
plt.figure(figsize = (10, 5))
plt.title('Temperatura')
plt.plot(buzio_tsdata[: 168, 1])
plt.plot(niteroi_tsdata[: 168, 1])
plt.plot(angra_tsdata[: 168, 1])
plt.xlabel('hora')
plt.ylabel('magnitude')
plt.legend(['Búzios', 'Niterói', 'Angra'])
plt.show()

# Direcionando o caminho onde o arquivo será salvo
output_path = Path(__file__).parent / 'BASE_DE_DADOS' /'solar_hourly_series.xlsx'

# Criando uma planilha do tipo xlsx
with pd.ExcelWriter(output_path) as writer:
    buzio_time_series = pd.DataFrame(buzio_tsdata)
    niteroi_time_series = pd.DataFrame(niteroi_tsdata)
    angra_time_series = pd.DataFrame(angra_tsdata)
    buzio_time_series.to_excel(writer, sheet_name = 'Búzios', index = False, header = None)
    niteroi_time_series.to_excel(writer, sheet_name = 'Niterói', index = False, header = None)
    angra_time_series.to_excel(writer, sheet_name = 'Angra dos Reis', index = False, header = None)