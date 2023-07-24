"""
Script to compute the dominant colors from an image using k-means
David Norman Diaz Estrada - 2023
"""


import cv2
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from time import perf_counter
import numpy as np

class DominantColors:
    CLUSTERS = None
    IMAGE = None
    COLORS = None
    LABELS = None

    def __init__(self, image, clusters):
        self.CLUSTERS = clusters
        self.IMAGE = image

    def resize(self, img):
        maxValue = 512  # set max allowed value for dimentions

        # get original dimentions:
        width,heigth = img.shape[1],img.shape[0]
        print("width: %d, height: %d" % (width, heigth))

        if width > maxValue:
            Wpercent = float(maxValue)/float(width)
            new_heigth = int(Wpercent*float(heigth))
            # dsize
            dsize = (maxValue, new_heigth)
            # resize image:
            img = cv2.resize(img, dsize)

        # get dimentions:
        width,heigth = img.shape[1],img.shape[0]
        #print("width: %d, height: %d" % (width, heigth))

        if heigth > maxValue:
            Hpercent = float(maxValue)/float(heigth)
            new_width = int(Hpercent*float(width))
            # dsize
            dsize = (new_width, maxValue)
            # resize image:
            img = cv2.resize(img, dsize)

        width, heigth = img.shape[1], img.shape[0]
        print("New width: %d, New height: %d" % (width,heigth))

        return img

    def dominantColors(self):
        # read image
        #img = cv2.imread(self.IMAGE)
        # openCV imread method doesn't support paths or filenames with unicode characters
        # If your image path contains Unicode characters, you can use the following code to read the image:
        img = cv2.imdecode(np.fromfile(self.IMAGE, dtype=np.uint8), cv2.IMREAD_UNCHANGED)

        # Scale image:
        img = self.resize(img)

        # convert to rgb from bgr
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # reshaping to a list of pixels
        img = img.reshape((img.shape[0] * img.shape[1], 3))

        # save image after operations
        self.IMAGE = img

        # using k-means to cluster pixels
        kmeans = KMeans(n_clusters=self.CLUSTERS)
        kmeans.fit(img)

        # the cluster centers are our dominant colors.
        self.COLORS = kmeans.cluster_centers_

        # save labels
        self.LABELS = kmeans.labels_

        # returning after converting to integer from float
        return self.COLORS.astype(int)

    def rgb_to_hex(self, rgb):
        return '#%02x%02x%02x' % (int(rgb[0]), int(rgb[1]), int(rgb[2]))

    def plotClusters(self):
        # plotting
        fig = plt.figure()
        ax = Axes3D(fig)
        for label, pix in zip(self.LABELS, self.IMAGE):
            ax.scatter(pix[0], pix[1], pix[2], color=self.rgb_to_hex(self.COLORS[label]))
        plt.show()

    def plotTones(self):
        colors = self.COLORS
        # plotting
        fig = plt.figure()
        ax = Axes3D(fig)
        for i in range(0, self.CLUSTERS):
            ax.scatter(colors[i][0], colors[i][1], colors[i][2], color=self.rgb_to_hex(colors[i]))
        plt.show()



def main(img, clusters):

    t1_start = perf_counter()  # guardamos tiempo inicial, para medir tiempo de ejecución

    dc = DominantColors(img, clusters) #create object
    colors = dc.dominantColors() # compute significant tones

    t2_stop = perf_counter()  # tiempo final
    print("Time elapsed: ", t2_stop - t1_start)  # CPU seconds elapsed (floating point)

    #print(colors)

    # plotting
    #dc.plotTones()

    Rtones = [0] * clusters
    Gtones = [0] * clusters
    Btones = [0] * clusters
    #loop through the colors and split into RGB channels, convert int32 to int using .item()
    for a in range(0, clusters):
        Rtones[a] = colors[a][0].item()
        Gtones[a] = colors[a][1].item()
        Btones[a] = colors[a][2].item()
    print("Rtones = " + str(Rtones))
    print("Gtones = " + str(Gtones))
    print("Btones = " + str(Btones))

    return Rtones,Gtones,Btones


"""
img = 'tmp3.png'
clusters = 8
R,G,B=main(img, clusters)
"""
