"""
Script to "fuzzyfy" colors
David Norman Diaz Estrada - 2023
"""
from matplotlib import pyplot as plt
import math

def gaussian(x, center, amplitude):
    y = (math.e) ** (-0.5 * ((x - center) / amplitude) ** 2)
    return y

def fuzzyfier(centerTones,amplitudes):
    #given crisp values for tones (splited by R,G,B components):
    Rcenters = centerTones[0]
    Gcenters = centerTones[1]
    Bcenters = centerTones[2]

    R_mv = [] #list to store the membership grade for each fuzzified R component
    G_mv = [] #list to store the membership grade for each fuzzified G component
    B_mv = [] #list to store the membership grade for each fuzzified B component


    for n in range(len(Rcenters)):
        # initialize membership values in zero:
        r_mv = [0]*256
        g_mv = [0]*256
        b_mv = [0]*256

        #get current center for each tone to be fuzzified:
        r_center = Rcenters[n]
        g_center = Gcenters[n]
        b_center = Bcenters[n]

        # get membership values:
        for x in range(0,256):
            r_mv[x] = gaussian(x, r_center, amplitudes[n])
            g_mv[x] = gaussian(x, g_center, amplitudes[n])
            b_mv[x] = gaussian(x, b_center, amplitudes[n])

        #append fuzzified RGB components of each tone:
        R_mv.append(r_mv)
        G_mv.append(g_mv)
        B_mv.append(b_mv)

    return R_mv,G_mv,B_mv #return fuzzyfied tones


def plotFuzzyTones(R,G,B):

    x = list(range(0, 256))
    # create a new figure, 3 rows 1 col, and assign each subplot to correspondant variable
    figure, (ax1, ax2, ax3) = plt.subplots(3, 1)
    #set max and min values for x and y for each subplot:
    ax1.axis([0, 255, 0, 1])  # [xmin, xmax, ymin, ymax]
    ax2.axis([0, 255, 0, 1])  # [xmin, xmax, ymin, ymax]
    ax3.axis([0, 255, 0, 1])  # [xmin, xmax, ymin, ymax]

    for n in range(0, len(R)):
        r = R[n]
        g = G[n]
        b = B[n]

        ax1.plot(x, r, 'r-')
        ax2.plot(x, g, 'g-')
        ax3.plot(x, b, 'b-')

    # set tittles for each subplot:
    ax1.set_title('R functions')
    ax2.set_title('G functions')
    ax3.set_title('B functions')

    # Set common labels
    figure.text(0.5, 0.04, 'Pixel values', ha='center', va='center')
    figure.text(0.04, 0.5, 'Membership Grade', ha='center', va='center', rotation='vertical')

    plt.show()



""""
Rtones = [255, 128, 117, 255, 205, 192, 255, 255]
Gtones = [0, 0, 83, 128, 5, 192, 255, 128]
Btones = [0, 64, 11, 0, 50, 192, 255, 128]

centerTones = [Rtones,Gtones,Btones]
R_mv,G_mv,B_mv = fuzzyfier(centerTones,amplitude=5)
plotFuzzyTones(R_mv,G_mv,B_mv)
"""


