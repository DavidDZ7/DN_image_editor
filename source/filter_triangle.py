"""
Script for triangle filter
This filter pixelates an image using triangle shapes
David Norman Diaz Estrada - 2023
"""
import os
import cv2
import numpy as np

def filter_triangle(filepath,size,flipX,flipY):
    #-------------------------------------------------------------------------------------
    #Load image and define size of triangle pattern
    #-------------------------------------------------------------------------------------"

    #image = cv2.imread(filepath)
    # openCV imread method doesn't support paths or filenames with unicode characters
    # If your image path contains Unicode characters, use imdecode:
    file_path_bytes = filepath.encode('utf-8')# Encode the file path to a byte string
    image = cv2.imdecode(np.fromfile(file_path_bytes, dtype=np.uint8), cv2.IMREAD_UNCHANGED)

    #-------------------------------------------------------------------------------------
    #Create kernels (matrices) for each triangle pattern
    #-------------------------------------------------------------------------------------
    kernel1=np.zeros((size,size),dtype=np.uint8)
    row = np.zeros(size,dtype=np.uint8)
    for i in range(0, size):
        row[i]=1
        #print(row)
        kernel1[i]=row

    #print(kernel1)

    kernel2=np.ones((size,size),dtype=np.uint8)
    row = np.ones(size,dtype=np.uint8)
    for i in range(0, size):
        row[i]=0
        #print(row)
        kernel2[i]=row

    #print(kernel2)

    print("Kernels created")

    #-------------------------------------------------------------------------------------
    # Compute how many squares can fit in the image:
    #-------------------------------------------------------------------------------------
    height, width, _ =image.shape #compute input image  shape

    #compute how many squares along x and y direction we can fit in the image:
    steps_y=int(height/size)
    steps_x=int(width/size)

    image=image[0:steps_y*size, 0:steps_x*size] #discard regions with uncomplete squares

    #-------------------------------------------------------------------------------------
    # Apply triangle filter:
    #-------------------------------------------------------------------------------------
    for j in range(0,steps_y):
        for i in range(0, steps_x):

            x=i*size # current x coordinate is equal to the number of i step * step size
            y=j*size # current y coordinate is equal to the number of j step * step size
            # -------------------------------------------------------------------------------------
            #get mean values for triangle 1:
            # -------------------------------------------------------------------------------------
            flattened_kernel1 = kernel1.flatten()  # flatten the kernel

            flattened_b1=image[y:y + size, x:x + size, 0].flatten() #retrieve blue channel of region and flatten the array
            #print(flattened_b1)
            mean_b1=np.mean(flattened_b1[flattened_kernel1.astype(bool)])#use flattened kernel to retrieve and compute the mean of elements inside the triangle
            mean_b1=mean_b1.astype('uint8') #make sure to return as uint8 since the mean can give float values
            #print(mean_b1)

            flattened_g1=image[y:y + size, x:x + size, 1].flatten() #retrieve green channel of region and flatten the array
            #print(flattened_g1)
            mean_g1=np.mean(flattened_g1[flattened_kernel1.astype(bool)])#use flattened kernel to retrieve and compute the mean of elements inside the triangle
            mean_g1=mean_g1.astype('uint8') #make sure to return as uint8 since the mean can give float values
            #print(mean_g1)

            flattened_r1=image[y:y + size, x:x + size, 2].flatten() #retrieve red channel of region and flatten the array
            #print(flattened_r1)
            mean_r1=np.mean(flattened_r1[flattened_kernel1.astype(bool)])#use flattened kernel to retrieve and compute the mean of elements inside the triangle
            mean_r1=mean_r1.astype('uint8') #make sure to return as uint8 since the mean can give float values
            #print(mean_r1)

            # -------------------------------------------------------------------------------------
            # get mean values for triangle 2:
            # -------------------------------------------------------------------------------------
            flattened_kernel2 = kernel2.flatten()  # flatten the kernel

            flattened_b2 = image[y:y + size, x:x + size,0].flatten()  # retrieve blue channel of region and flatten the array
            # print(flattened_b2)
            mean_b2 = np.mean(flattened_b2[flattened_kernel2.astype(bool)])  # use flattened kernel to retrieve and compute the mean of elements inside the triangle
            mean_b2 = mean_b2.astype('uint8')  # make sure to return as uint8 since the mean can give float values
            #print(mean_b2)

            flattened_g2 = image[y:y + size, x:x + size,1].flatten()  # retrieve green channel of region and flatten the array
            # print(flattened_g2)
            mean_g2 = np.mean(flattened_g2[flattened_kernel2.astype(bool)])  # use flattened kernel to retrieve and compute the mean of elements inside the triangle
            mean_g2 = mean_g2.astype('uint8')  # make sure to return as uint8 since the mean can give float values
            #print(mean_g2)

            flattened_r2 = image[y:y + size, x:x + size,2].flatten()  # retrieve red channel of region and flatten the array
            # print(flattened_r2)
            mean_r2 = np.mean(flattened_r2[flattened_kernel2.astype(bool)])  # use flattened kernel to retrieve and compute the mean of elements inside the triangle
            mean_r2 = mean_r2.astype('uint8')  # make sure to return as uint8 since the mean can give float values
            #print(mean_r2)

            # -------------------------------------------------------------------------------------
            # Replace the region in the image with the modified channels
            # -------------------------------------------------------------------------------------
            image[y:y + size, x:x + size, 0] = kernel1*mean_b1 + kernel2*mean_b2
            image[y:y + size, x:x + size, 1] = kernel1*mean_g1 + kernel2*mean_g2
            image[y:y + size, x:x + size, 2] = kernel1*mean_r1 + kernel2*mean_r2

            if flipX:
                kernel1=np.flip(kernel1, axis=1)#to flip the kernel for next column
                kernel2=np.flip(kernel2, axis=1)#to flip the kernel for next column
        if flipY:
            kernel1 = np.flip(kernel1, axis=0)#to flip the kernel for next row
            kernel2 = np.flip(kernel2, axis=0)#to flip the kernel for next row


    print("Done")
    return image

if __name__ == "__main__":
    print("-" * 20)
    print("Debug mode")
    print("-" * 20)

    filepath=r"my_image_filepath"
    size=30
    PixelatedImage=filter_triangle(filepath=filepath, size=size, flipX=True, flipY=True)
    # Save output
    filename = os.path.basename(filepath)# Get the base name of the file
    name_without_extension = os.path.splitext(filename)[0]# Split the file name and extension
    outfile=name_without_extension+"_output_size"+str(size)+".png"
    cv2.imwrite(outfile,PixelatedImage)