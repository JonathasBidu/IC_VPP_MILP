import numpy as np

def decomp(x, data):

    Nt = data['Nt']
    Nbm = data['Nbm']

    Nr = (Nbm * Nt)
    Ni = (Nbm * Ni)

    begin = 0
    end = Nr
    xr = np.array(x[begin: end])

    begin = end
    end = Nr + Ni
    xi = np.array(x[begin: end])

    begin = 0
    end = (Nbm * Nt)
    p_bm = xr[begin: end]
    p_bm = p_bm.reshape((Nbm, Nt))

    begin = 0
    end = (Nbm * Nt)
    u_bm = xi[begin: end]
    u_bm = u_bm.reshape((Nbm, Nt))

    return p_bm, u_bm
