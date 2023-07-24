"""
Script to compute a linear gradient between 2 colors
David Norman Diaz Estrada - 2023
"""
def getGradient(px1,px2):
    r1, g1, b1 = px1[0], px1[1], px1[2]
    r2, g2, b2 = px2[0], px2[1], px2[2]

    modulo=((r1-r2)**2+(g1-g2)**2+(b1-b2)**2)**0.5
    #calculamos componentes del vector unitario:
    uR=float(abs(r2-r1))/modulo
    uG=float(abs(g2-g1))/modulo
    uB=float(abs(b2-b1))/modulo

    particiones=7#número de tonos que forman parte del gradiente
    #inicializamos valores en cero para listas que almacenarán valores de los tonos del gradiente:
    R=[0]*(particiones+1)
    G=[0]*(particiones+1)
    B=[0]*(particiones+1)
    #resolución:
    res=modulo/particiones

    #calculamos cual es la coordenada mínima en cada eje para siempre ir aumentando de menor a mayor
    #rr=min(r1,r2)
    #gg=min(g1,g2)
    #bb=min(b1,b2)
    if r1 <= r2:signR = 1
    else: signR = -1
    if g1 <= g2:signG = 1
    else: signG = -1
    if b1 <= b2:signB = 1
    else: signB = -1

    #calculamos los tonos pertenecientes al linear gradient:
    for n in range(0,particiones+1):
        R[n] = r1 + signR*round(uR * (n*res))#valor inicial + (vector unitario)*(n*resolución)
        G[n] = g1 + signG*round(uG * (n*res))#valor inicial + (vector unitario)*(n*resolución)
        B[n] = b1 + signB*round(uB * (n*res))#valor inicial + (vector unitario)*(n*resolución)

    """
    px1 = [r1, g1, b1]
    px2 = [r2, g2, b2]
    print("px1: " + str(px1))
    print("px2: " + str(px2))
    print("modulo: " + str(modulo))
    print("particiones: " + str(particiones))
    print("resolución: " + str(res))
    print("R: " + str(R))
    print("G: " + str(G))
    print("B: " + str(B))
    """

    return R,G,B



def rgb_to_hexa(rgb):
    return '#%02x%02x%02x' % (int(rgb[0]), int(rgb[1]), int(rgb[2]))


def plotGradient(R,G,B):
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D

    particiones=7

    fig = plt.figure()
    ax = Axes3D(fig)
    for i in range(0,particiones+1):
        color=[R[i], G[i], B[i]]
        ax.scatter(R[i], G[i], B[i],  color=rgb_to_hexa(color))
    plt.show()



"""
px1=[250,160,70]
px2=[100,20,30]
R,G,B = getGradient(px1,px2)
plotGradient(R,G,B)
"""
