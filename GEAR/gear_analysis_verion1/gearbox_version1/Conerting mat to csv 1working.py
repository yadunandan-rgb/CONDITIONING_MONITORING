import pandas as pd
import numpy as np
from pandas import Series, DataFrame
import os
import scipy.io
            
os.listdir(path=r'D:\Vegam_all_csv_files_sensor_data\ATestData_Hemang_Sir\v431')

def getListOfFiles(dirName):
    # create a list of file and sub directories 
    # names in the given directory 
    listOfFile = os.listdir(dirName)
    allFiles = list()
    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(dirName, entry)
        # If entry is a directory then get the list of files in this directory 
        if os.path.isdir(fullPath):
            allFiles = allFiles + getListOfFiles(fullPath)
        else:
            allFiles.append(fullPath)
    return allFiles

dirName = r'D:\Vegam_all_csv_files_sensor_data\ATestData_Hemang_Sir\v431';
# Get the list of all files in directory tree at given path
listOfFiles = getListOfFiles(dirName)

listOfFiles = list()
for (dirpath, dirnames, filenames) in os.walk(dirName):
    listOfFiles += [os.path.join(dirpath, file) for file in filenames]

# file_name = []
for files in listOfFiles:
    # print(files)
    # name = files[-9:-4]
    # file_name.append(name)
    mat = scipy.io.loadmat(files,struct_as_record=False,squeeze_me=True)
    mat = {k:v for k, v in mat.items() if k[0] != '_'}
    df_csv = pd.DataFrame(data=mat)
    df_csv.to_csv(r'D:/Vegam_all_csv_files_sensor_data/ATestData_Hemang_Sir/CSv_from_Mat'+files[-9:-4]+'.csv', index=False) 
