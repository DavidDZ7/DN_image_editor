"""
Script to perform different types of color mapping
David Norman Diaz Estrada - 2023
"""
import cv2
import numpy as np
from time import perf_counter
#import colorsys
import source.fuzzyfier as fuzzyfier


def colorMap(pxR,pxG,pxB, Rtones, Gtones, Btones):
    #recuperamos componentes RGB del pixel original:
    b=pxB
    g=pxG
    r=pxR
    #medimos distancias entre pixel original y cada tono de la lista
    distances=[]
    for i in range (0,len(Rtones)):
        R = Rtones[i]
        G = Gtones[i]
        B = Btones[i]
        dist=((R-r)**2+(G-g)**2+(B-b)**2)**0.5 #euclidean distance
        #dist=abs(R - r) + abs(G - g) + abs(B - b) # "pseudo euclidean distance"
        distances.append(dist)
    dist_min=min(distances)#identificamos distancia minima
    index=0
    #identificamos en que posición estaba la distancia mínima:
    for element in  distances:
        if dist_min==element: break
        index+=1
    #recuperamos componentes RGB del tono a asignar
    newR = Rtones[index]
    newG = Gtones[index]
    newB = Btones[index]
    #return value of selected tone:
    return [newR,newG,newB]

def fuzzyColorMap(pxR,pxG,pxB, tones, membershipValues):
    R_mv, G_mv, B_mv = membershipValues[0], membershipValues[1],membershipValues[2]
    Rtones, Gtones, Btones = tones[0], tones[1],tones[2]
    #recuperamos componentes RGB del pixel original:
    b=pxB
    g=pxG
    r=pxR

    #medimos similitud entre pixel original y cada tono de la lista
    similitudes=[]
    for i in range (0,len(Rtones)):
        sim = R_mv[i][r]*G_mv[i][g]*B_mv[i][b] #fuzzy similitude of original pixel with current tone
        similitudes.append(sim)
    similitud_max=max(similitudes)#identificamos similitud máxima

    index=0
    #identificamos en que posición estaba la similitud máxima:
    for element in  similitudes:
        if similitud_max==element: break
        index+=1
    #recuperamos componentes RGB del tono a asignar
    newR = Rtones[index]
    newG = Gtones[index]
    newB = Btones[index]
    #return value of selected tone:
    return [newR,newG,newB]

def lightcolorMap(pxR,pxG,pxB, Rtones, Gtones, Btones):
    #retrieve RGB components of original pixel:
    b=pxB
    g=pxG
    r=pxR

    #compute lightness level of pixel:
    light=int((b+g+r)/3)
    index=0
    if light in range(  0,  32): index = 0
    if light in range( 32,  64): index = 1
    if light in range( 64,  96): index = 2
    if light in range( 96, 128): index = 3
    if light in range(128, 160): index = 4
    if light in range(160, 192): index = 5
    if light in range(192, 224): index = 6
    if light in range(224, 256): index = 7

    #Retrieve and set RGB values of new assigned tone:
    #Method 1: assign new color according to lightness range: assigns only a tone from palette
    #newR = Rtones[index]
    #newG = Gtones[index]
    #newB = Btones[index]
    #Method 2: assign new color according to lightness range (proportionally): gives more tones within the palette
    newR = int(Rtones[index]*(light/((index+1)*32-1)))
    newG = int(Gtones[index]*(light/((index+1)*32-1)))
    newB = int(Btones[index]*(light/((index+1)*32-1)))

    #return value of selected tone:
    return [newR,newG,newB]

def main(fileName,Rtones,Gtones,Btones,amplitudes,colorMode,mappingMode,visualize):

    t1_start = perf_counter()  # store start time, to measure execution time
    print(fileName)
    #fileName='Lena.jpg'

    #img = cv2.imread(fileName,cv2.IMREAD_COLOR)
    # openCV imread method doesn't support paths or filenames with unicode characters
    # If your image path contains Unicode characters, you can use the following code to read the image:
    img = cv2.imdecode(np.fromfile(fileName, dtype=np.uint8), cv2.IMREAD_UNCHANGED)

    rows,cols,channels = img.shape
    #print(img)
    print('------------')

    #Rtones =[87,144,199,255,255,26,38,251,239, 237,161,113, 17]
    #Gtones =[24, 12,  0, 87,195,19,41,191,106,   3, 42,  1,  1]
    #Btones =[69, 62, 57, 51,  0,52,74, 69, 50,  69, 94, 98, 65]


    if colorMode == "RGB": #RGB mode (BGR in openCV image)
        #initialize values:
        B,G,R=0,0,0
        membershipValues=[]
        centerTones=[]

        if mappingMode=="fuzzy":
            #for fuzzy color mapping:
            centerTones = [Rtones, Gtones, Btones]
            membershipValues = fuzzyfier.fuzzyfier(centerTones, amplitudes)

        for i in range(rows):
            for j in range(cols):
                 pxB = img.item(i, j, 0)  # get original pixel value (B,G,R)
                 pxG = img.item(i, j, 1)  # get original pixel value (B,G,R)
                 pxR = img.item(i, j, 2)  # get original pixel value (B,G,R)
                 if mappingMode== "euclidean":
                    R, G, B = colorMap(pxR, pxG, pxB, Rtones, Gtones, Btones)  # call color mapping function (euclidean based)
                 if mappingMode=="fuzzy":
                    R, G, B = fuzzyColorMap(pxR,pxG,pxB, centerTones, membershipValues)  # call fuzzy color mapping function
                 if mappingMode=="light":
                    R, G, B = lightcolorMap(pxR, pxG, pxB, Rtones, Gtones, Btones)  # call color mapping function (light based)
                 img.itemset((i, j, 0), B)
                 img.itemset((i, j, 1), G)
                 img.itemset((i, j, 2), R)

        if visualize and mappingMode=="fuzzy": #visualize membership values, fuzzyTones
            rr,gg,bb = membershipValues
            fuzzyfier.plotFuzzyTones(rr,gg,bb)

    t2_stop = perf_counter()  # stop measuring time
    print("Time elapsed: ", t2_stop - t1_start)  # CPU seconds elapsed (floating point)

    #newFile = fileName+'_colorMap.png'
    #cv2.imwrite(newFile,img)

    #show processed Image:
    #cv2.imshow('image',img)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()


    return img