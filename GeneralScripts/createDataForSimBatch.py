"""
Python script to create *.placements files for GATE simulation.
The input can be both *.npy files and *.csv files.  The format 
of the *.npy or *.csv file should be t, x, y, z in columns.  

Author:                 Rayhaan Perin
Last Revised:           30-07-2022
Packages:               numpy
Optional Packages:      None
"""

##########
# PACKAGES #
##########

import numpy as np
import os
from natsort import os_sorted
from tqdm import tqdm 
import csv

#####################
# CLASSES AND FUNCTIONS #
#####################

def readInData(PATH: str, Type: str) -> np.ndarray:
    if Type == "csv":
        data = np.loadtxt(PATH)
    elif Type == "npy":
        data = np.load(PATH)
    return data

def writeData(data: np.ndarray, OUTPATH: str, OUTNAME: str) -> None:
    zero = np.array([0 for _ in range(len(data[:, 0]))], dtype = np.int64)
    one = np.array([1 for _ in range(len(data[:, 0]))], dtype = np.int64)

    writeData = np.array([data[:, 0], zero, zero, one, zero, data[:, 1], data[:, 2], data[:, 3]]).T # The addition - min is to start the motion at 0.0 s within FP precision

    with open("{}{}".format(OUTPATH, OUTNAME), 'w') as f:
        f.write("Time s\n")
        f.write("Rotation deg\n")
        f.write("Translation mm\n")
        csv.writer(f, delimiter=' ').writerows(writeData)

def main():
    # Controls for IO
    print("Defining IO Controls ...")
    INPATH = "/home/rayhaan/randomWalk_V3/GATE_Generation/SS_0.60_TS_0.80_means_1.0_100.0_mm_5000_locs_300um/NPY_Placements/Mean_0.001_ms/"
    OUTPATH = "/home/rayhaan/randomWalk_V3/GATE_Generation/SS_0.60_TS_0.80_means_1.0_100.0_mm_5000_locs_300um/Placements/Mean_0.001_ms/"
    # OUTNAME = "RW_Sigma_2.00mm_TS_1.20ms.placements"
    Type = "npy"
    print("Done Defining IO Controls ...")
    print("\n")
    # Read in the Data depending on input type
    print("Read and Write data...")
    files = np.array(os_sorted(os.listdir(INPATH)))
    for i in tqdm(range(len(files)), desc = "File No"):
        pathData = readInData(PATH = INPATH + files[i], Type = Type)
        fileName = os.path.splitext(files[i])[0]
        writeData(data = pathData, OUTPATH = OUTPATH, OUTNAME = fileName + ".placements")
    print("Done Reading and Writing Data ...")
    print("\n")

    # Write data to *.placements file
    # print("Write Data ...")
    # writeData(data = pathData, OUTPATH = OUTPATH, OUTNAME = OUTNAME)
    # print("Done writing Data ...")

##############
# IF CHECK MAIN #
##############

if __name__ == "__main__":
    main()