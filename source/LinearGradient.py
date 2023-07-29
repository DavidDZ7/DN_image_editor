"""
Script to compute a linear gradient between 2 colors
David Norman Diaz Estrada - 2023
"""
def getGradient(px1,px2):
    """
    Function to compute linear gradient between 2 colors
    :param px1: color 1
    :param px2: color 2
    :return: returns 3 lists with R,G,B components of colors inside the gradient
    """
    r1, g1, b1 = px1[0], px1[1], px1[2]
    r2, g2, b2 = px2[0], px2[1], px2[2]
    #Compute modulus (magnitude) of vector between px1 and px2:
    modulus=((r1-r2)**2+(g1-g2)**2+(b1-b2)**2)**0.5
    #Compute components of unit vector:
    uR=float(abs(r2-r1))/modulus
    uG=float(abs(g2-g1))/modulus
    uB=float(abs(b2-b1))/modulus

    partitions=7 # Number of partitions in the gradient (number of tones-1)
    #Initialize list to store RGB values of colors in gradient:
    R=[0]*(partitions+1)
    G=[0]*(partitions+1)
    B=[0]*(partitions+1)
    #resolution:
    res=modulus/partitions

    #Identify the minimum coordinate in each axis, so we can compute gradient from smaller to greatest value:
    #rr=min(r1,r2)
    #gg=min(g1,g2)
    #bb=min(b1,b2)
    if r1 <= r2:signR = 1
    else: signR = -1
    if g1 <= g2:signG = 1
    else: signG = -1
    if b1 <= b2:signB = 1
    else: signB = -1

    #Compute tones inside the linear:
    for n in range(0,partitions+1):
        R[n] = r1 + signR*round(uR * (n*res))#initial value + (unit vector)*(n*resolution)
        G[n] = g1 + signG*round(uG * (n*res))#initial value + (unit vector)*(n*resolution)
        B[n] = b1 + signB*round(uB * (n*res))#initial value + (unit vector)*(n*resolution)

    """
    px1 = [r1, g1, b1]
    px2 = [r2, g2, b2]
    print("px1: " + str(px1))
    print("px2: " + str(px2))
    print("modulus: " + str(modulus))
    print("partitions: " + str(partitions))
    print("resolutions: " + str(res))
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

    partitions=7

    fig = plt.figure()
    ax = Axes3D(fig)
    for i in range(0,partitions+1):
        color=[R[i], G[i], B[i]]
        ax.scatter(R[i], G[i], B[i],  color=rgb_to_hexa(color))
    plt.show()


if __name__ == "__main__":
    print("-" * 20)
    print("Debug mode")
    print("-" * 20)

    px1 = [250, 160, 70]
    px2 = [100, 20, 30]
    R, G, B = getGradient(px1, px2)
    plotGradient(R, G, B)