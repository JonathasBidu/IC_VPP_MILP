import numpy as np

"""
    Este script tem a finalidade de receber um vetor de variáveis de decisão (x), vindo de um otimizador, e o decompor em suas variáveis de decisão.

    - Parâmetros de entrada (x: np.ndarray, data: dict):

        - (x:np.ndarray): vetor de variáveis de decisões otimizadas pelo otimizador (GA). (p_exp, p_imp, p_bm, gamma_bm, p_chg, p_dch, soc, p_dl, u_exp, u_imp, u_bm, u_chg, u_dch, u_dl):
            - p_exp: potência exportada pela VPP, shape (Nt,);
            - p_imp: Pot~encia importada pela VPP, shape (Nt,);
            - p_bm: Potência das usinas de geração à biomassa (UBTMs), shape (Nbm, Nt);
            - gamma_bm: Custo operacional da das UBTMs, shape (Nbm, Nt);
            - p_chg: Potência de carregamento dos armazenadores da VPP, shape (Nbat, Nbm);
            - p_dch: Potência de descarregamento dos armazenadores da VPP, shape (Nbat, Nbm);
            - soc: Nível de energia dos armazenadores da VPP, shape (Nbat, Nt);
            - p_dl: Potência de cargas despacháveis da VPP, shape (Ndl, Nt);
            - u_exp: Estado de exportação de energia pela VPP, shape (Nt,);
            - u_imp: Estado de importação de energia pela VPP, shape (Nt,);
            - u_bm: Estado das UBTMs da VPP, shape (Nbm, Nt);
            - u_chg: Estado de carregamento dos armazenadores da VPP, shape (Nbat, Nt);
            - u_dch: Estado de descarregamento dos armazenadores da VPP, shape (Nbat, Nt);
            - u_dl: Estado das cargas despacháveis da VPP, shape (Ndl, Nt);

        - (data: dict): Dicionário contendo os parâmetros iniciais. (Nt: int, Ndl: int, Nbm: int, Nbat: int):
            - Nt: Período da simulação da VPP;
            - Ndl: Quantidade de cargas despacháveis da VPP;
            - Nbm: Quantidade de UBTMs da VPP;
            - Nbat: Quantidade de armazenadores da VPP;

    - Retorna uma tupla contendo um diversos array: -> tuple[np.ndarray]: Variáveis reais (p_exp, p_imp, p_bm, gamma_bm, p_chg, p_dch, p_dl) e inteiras (u_exp, u_imp, u_bm, u_chg, u_dch, u_dl), onde:
        
        - p_exp: Potência de exportação da VPP, shape (Nt,);
        - p_imp: Potênica de importação da VPP, shape (Nt,);
        - p_bm: Potência das UBTMs (usinas de biomassa), shape (Nbm, Nt);
        - gamma_bm: Custo das usinas de biomassa, shape (Nbm, Nt);
        - p_chg: Potência de carregamento dos armazenadores da VPP, shape (Nbat, Nt);
        - p_dch: Potência de descarregamento dos amazenadores da VPP, shape (Nbat, Nt);
        - soc: Nível de energia dos armazenadores da VPP, shape (Nbat, Nt);
        - p_dl: Potência das cargas despacháveis da VPP, shape (Ndl, Nt);
        - u_exp: Estado de exportação da VPP, shape (Nt,);
        - u_imp: Estado de impportação da VPP, shape (Nt,);
        - u_bm: Estado das UBTMs da VPP, shape (Nbm, Nt);
        - u_chg: Estado do carregamento dos armazenadores da VPP, shape (Nbat, Nt);
        - u_dch: Estado do descarregamento dos armazenadores da VPP, shape (Nbat, Nt);
        - u_dl: Estado das cargas despacháveis da VPP, shape (Ndl, Nt);

"""

def decompose(x: np.ndarray, data: dict)-> tuple[np.ndarray]:

    # Parâmetros iniciais de VPP
    Nt = data['Nt'] # Período de simulação da VPP
    Ndl = data['Ndl'] # Quantidade de cargas despacháveis da VPP
    Nbm = data['Nbm'] # Quantidade de usinas de biomassa da VPP
    Nbat = data['Nbat'] # Quantidade de armazenadores da VPP

    # Definindo a quantidade de variáveis reais (Nr) e variáveis inteiras (Ni)
    # Variáveis reais: p_exp, p_imp, p_bm, gamma_bm, p_chg, p_dch, soc, p_dl
    Nr = Nt + Nt + (Nt * Nbm) + (Nt * Nbm) + (Nt * Nbat) + (Nt * Nbat) + (Nbat * Nt) + (Nt * Ndl)
    # Variáveis inteiras: u_exp, u_imp, u_bm, u_chg, u_dch, u_dl
    Ni = Nt + Nt + (Nt * Nbm) + (Nt * Nbat) + (Nt * Nbat) + (Nt * Ndl)


    # Definindo o vetor de variáveis reais (xr)
    begin = 0
    end = Nr
    xr = np.array(x[begin: end])

    # Definindo o vetor de variáveis inteiras (xi)
    begin = end
    end = end + Ni
    xi = np.array(x[begin: end])

    # Obtenção da potência de exportação (p_exp)
    begin = 0
    end =  Nt
    p_exp = xr[begin: end]

    # Obtenção da potência de importação (p_imp)
    begin = end
    end = end + Nt
    p_imp = xr[begin: end]

    # Obtenção da variável de decisão p_bm (potência da biomassa)
    begin = end
    end = end + (Nt * Nbm)
    p_bm = xr[begin: end]
    p_bm = p_bm.reshape((Nbm, Nt)) # Ajustando a dimensão de p_bm para (Nbm, Nt)

    # Obtenção da variável de decisão gamma_bm (custo da biomassa)
    begin = end
    end = end + (Nt * Nbm)
    gamma_bm = xr[begin: end]
    gamma_bm = gamma_bm.reshape((Nbm, Nt)) # Ajustando a dimensão de gamma para (Nbm, Nt)

    # Obtenção da variável de decisão p_chg (potência de carregamento dos armazenadores)
    begin = end
    end = end + (Nt * Nbat)
    p_chg = xr[begin: end]
    p_chg = p_chg.reshape((Nbat, Nt)) # Ajustando a dimensão de p_dch para (Nbat, Nt)

    # Obtenção da variável de decisão p_dch (potência de descarregamento dos armazenadores)
    begin = end
    end = end + (Nt * Nbat)
    p_dch = xr[begin: end]
    p_dch = p_dch.reshape((Nbat, Nt)) # Ajustando a dimensão de p_chg para (Nbat, Nt)

    # Obtenção da variável de decisão soc (State of Charge - Estado de Carga)
    begin = end
    end = end + (Nt * Nbat)
    soc = xr[begin: end]
    soc = soc.reshape((Nbat, Nt)) # Ajustando a dimensão de soc para (Nbat, Nt)

    # Obtenção da variável de decisão p_dl (potência das cargas despacháveis)
    begin = end
    end = end + (Nt * Ndl)
    p_dl = xr[begin: end]
    p_dl = p_dl.reshape((Ndl, Nt)) # Ajustando a dimensão de p_dl para (Ndl, Nt)

    # Obtenção da variável de estado de exportação (u_exp), onde: (0 = desligado e 1 ligado)
    begin = 0
    end = Nt
    u_exp = xi[begin: end]
    u_exp = np.float64(u_exp > 0.5) # Lógica para que u_exp seja binário, se > 0.5, então, u_exp = 1, cc. u_exp = 0

    # Obtenção da variável de estado da potência de importação pela VPP (u_imp), onde: (0 = desligado e 1 ligado)
    begin = end
    end = end + Nt
    u_imp = xi[begin: end]
    u_imp = np.float64(u_imp > 0.5) # Lógica para que u_imp seja binário

    # Obtenção da variável de estado da usinas de biomassa (u_bm), onde: (0 = desligado e 1 ligado)
    begin = end
    end = end + (Nt * Nbm)
    u_bm = xi[begin: end]
    u_bm = np.float64(u_bm > 0.5) # Lógica para que u_bm seja binário
    u_bm = u_bm.reshape((Nbm, Nt)) # Ajustando a dimensão de u_bm para (Nbm, Nt) 

    # Obtenção da variável de estado de carregamento dos armazenadores da VPP (u_chg), onde: (0 = desligado e 1 ligado)
    begin = end
    end = end + (Nt * Nbat)
    u_chg = xi[begin: end]
    u_chg = np.float64(u_chg > 0.5) # Lógica para que u_chg seja binário
    u_chg = u_chg.reshape((Nbat, Nt)) # Ajustando a dimensão de u_bm para (Nbat, Nt) 

    # Obtenção da variável de estado de descarregamento dos armazenadores da VPP (u_dch), onde: (0 = desligado e 1 ligado)
    begin = end
    end = end + (Nt * Nbat)
    u_dch = xi[begin: end]
    u_dch = np.float64(u_dch > 0.5) # Lógica para que u_bm seja binário
    u_dch = u_dch.reshape((Nbat, Nt)) # Ajustando a dimensão de u_bm para (Nbat, Nt) 

    # Obtenção da variável de estado das cargas despacháveis da VPP (u_dl), onde: (0 = desligado e 1 ligado)
    begin = end
    end = end + (Nt * Ndl)
    u_dl = xi[begin: end]
    u_dl = np.float64(u_dl > 0.5) # Lógica para que u_bm seja binário
    u_dl = u_dl.reshape((Ndl, Nt)) # Ajustando a dimensão de u_bm para (Nbat, Nt) 

    return p_exp, p_imp, p_bm, gamma_bm, p_chg, p_dch, soc, p_dl, u_exp, u_imp, u_bm, u_chg, u_dch, u_dl

# Exemplo de uso
if __name__ == '__main__':

    from vpp_initial_data import vpp_data

    # Obtendo os parâmetros iniciais
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

    # Gerando um população inicial de teste
    x = np.random.rand(Nr + Ni)

    # Decompondo a população inicial em variáveis de decisão para teste
    p_exp, p_imp, p_bm, gamma_bm, p_chg, p_dch, soc, p_dl, u_exp, u_imp, u_bm, u_chg, u_dch, u_dl = decompose(x, data)

    # Visualizando as variáveis de decisão
    print(f'p_exp shape {p_exp.shape}\n{p_exp}\n')
    print(f'p_imp shape {p_imp.shape}\n{p_imp}\n')
    print(f'p_bm shape {p_bm.shape}\n{p_bm}\n')
    print(f'gamma_bm shape {gamma_bm.shape}\n{gamma_bm}\n')
    print(f'p_chg shape {p_chg.shape}\n{p_chg}\n')
    print(f'p_dch shape {p_dch.shape}\n{p_dch}\n')
    print(f'soc shape {soc.shape}\n{soc}\n')
    print(f'p_dl shape {p_dl.shape}\n{p_dl}\n')
    print(f'u_exp shape {u_exp.shape}\n{u_exp}\n')
    print(f'u_imp shape {u_imp.shape}\n{u_imp}\n')
    print(f'u_bm shape {u_bm.shape}\n{u_bm}\n')
    print(f'u_chg shape {u_chg.shape}\n{u_chg}\n')
    print(f'u_dch shape {u_dch.shape}\n{u_dch}\n')
    print(f'u_dl shape {u_dl.shape}\n{u_dl}\n')
        