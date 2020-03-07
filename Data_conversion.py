#!/usr/bin/env python
# coding: utf-8

# In[2]:

# Aim :- Converting original csv file which can be used for data segmentation
# Importing useful libraries
import pandas as pd
import numpy as np
import glob
import os
import csv

# Specify input folder path from which all the csv file will be inputted
csvdir='C:\\Users\\pranjal\\Desktop\\IITH project\\Data2\\allcsv'
csvfiles=glob.glob(os.path.join(csvdir,'*.csv'))

# Specify output folder path to which final csv file is outputted
csvdirout='C:\\Users\\pranjal\\Desktop\\IITH project\\Data2\\allcsvconvert\\'
#csvfileout=glob.glob(os.path.join(csvdirout,'*.csv'))

i=1
# Loop which takes one csv file at a time
for csvfile in csvfiles:
    j=0
    splitlist=[]
    splitlist=csvfile.split('\\')
    print(splitlist[-1])

    with open(os.path.join(csvfile), 'rt') as inp, open(os.path.join(csvdirout+splitlist[-1]), 'w',newline='') as out:
        writer = csv.writer(out)
        readCsv=csv.reader(inp,delimiter=',')
        row1=" "
        lon=""
        lat=""
        # Input Header names of columns
        col=" ","Velocity","Distance","ElapsedTime","LateralAcceleration","LongitudinalAcceleration","Latitude","Longitude","Heading"
        writer.writerow(col)
        for row in readCsv:
            if j>7:
                row1=j-8
                # Convert lat and long into decimal format from degree.
                lat=float(row[6][0:2])+float(row[6][4:16])/60
                lon=float(row[7][0:2])+float(row[7][4:16])/60
                # Input the column for data segmentation
                # Here - row1= Index, row[8]=velocity, row[16]=Distance, row[17]=Elapsed Time row[19]=Lat Acc, row[20]=Long Acc
                row=row1,row[8],row[16],row[17],row[19],row[20],lat,lon,row[9]
                writer.writerow(row)
            j=j+1
    inp.close()
    out.close()
    i=i+1
    




