#Description: Clean & prepare 3 files for visualization and analysis 
#Author: Jordan Poronovich
#Modified: Feb 2021

import math
import numpy as np
import pandas as pd
import calendar
import datetime as dt
from math import nan
from numpy.core.numeric import NaN

#Open three statsCAN CSV files
#Header set to None
GDP = pd.read_csv("Canada_GDP.csv", delimiter=",", header = None)
AlcoholSales = pd.read_csv("AlcoholSales.csv", delimiter=",", header = None)
TobaccoSales =  pd.read_csv("TobaccoSales.csv", delimiter=",", header = None)
CanPop = pd.read_csv("CanadaPopulation.csv", delimiter=",", header = None)

#--------------------------------------GDP CSV Cleaning-----------------------------------------------


#Defining headers to pre-exisiting row and resetting header.   
header_names = list(GDP.iloc[8])
header_names[0] = NaN # setting first index to NA 
GDP.columns = header_names

#Slecting relevant table
GDP = GDP.iloc[10:41]

#Converting strings to floats
#setting tabale dimensions
Num_Col = len(GDP.columns)
Num_row = len(GDP.index)

#Setting Column starting position at one to avoid string convertion error. 
i_column = 1
i_row = 0

#removing "," from numbers and converting them to floats
while i_column < Num_Col:
    while i_row < Num_row:
        GDP.iloc[i_row,i_column]  = float(GDP.iloc[i_row, i_column].replace(",",""))
        i_row += 1
    i_column += 1
    i_row = 0

#***Save to new file without index columun. Open new file to confirm***
GDP.to_csv("Canada_GDP(Clean).csv", index = False)
GDP = pd.read_csv("Canada_GDP(Clean).csv")
print(GDP.head(5))


#--------------------------------------Alcohol Sale CSV Cleaning---------------------------------------------

#Getting header & header length
header_names = list(AlcoholSales.iloc[7])
header_lgth = len(header_names)

#Declaring list with start day one month before data set Jan 2000
Date_list = [dt.date(1999,12,1)]
i =0
#creating new monthly header that will contain dates for further analysis
while i < header_lgth-1:
    Day2EOM = calendar.monthrange(Date_list[i].year,Date_list[i].month)[1]
    Date_list.insert(i+1,Date_list[i]+dt.timedelta(Day2EOM))
    Date_list[i] = int(Date_list[i].strftime("%Y%m%d")) #removing seperators "-" from date. Ease cross platform analysis.
    i += 1

#Changing final date in loop - TEMP FIX
Date_list[len(Date_list)-1] = int(Date_list[i].strftime("%Y%m%d"))

#First field of header blank
Date_list[0] = ""

AlcoholSales.columns = Date_list
#Isolating relevant info and removing irrelevant rows 
AlcoholSales = AlcoholSales.iloc[9:23]

Num_Col = len(AlcoholSales.columns)
Num_row = len(AlcoholSales.index)

i_column = 0
i_row = 0

#setting characters ".." and "x" by "Na" to varibles
TwoDots = AlcoholSales.iloc[1,1]
SingleX = AlcoholSales.iloc[1,252]

#Replacing characters ".." and "x" by "Na"
while i_column < Num_Col:
    while i_row < Num_row:
        Cell = AlcoholSales.iloc[i_row,i_column]
        if Cell == TwoDots or Cell == SingleX:
            AlcoholSales.iloc[i_row,i_column] = nan
            i_row += 1
        else:
            i_row += 1
    i_column += 1
    i_row = 0

#Converting strings to floats
#setting tabale dimensions
Num_Col = len(AlcoholSales.columns)
Num_row = len(AlcoholSales.index)

#Setting Column starting position at one to avoid string convertion error. 
i_column = 1
i_row = 0

#removing "," from numbers and converting them to floats
while i_column < Num_Col:
    while i_row < Num_row:
        if pd.isna(AlcoholSales.iloc[i_row,i_column]):
            i_row += 1
        else:
            AlcoholSales.iloc[i_row,i_column]  = float(AlcoholSales.iloc[i_row, i_column].replace(",",""))
            i_row += 1
    i_column += 1
    i_row = 0

#saving, opening and reprinting new file for confirmaiton
AlcoholSales.to_csv("AlcoholSales(Clean).csv", index=False)
AlcoholSales = pd.read_csv("AlcoholSales(Clean).csv")
print(AlcoholSales)

#--------------------------------------Tabaco Sale CSV Cleaning---------------------------------------------

#setting header names
header_names = list(TobaccoSales.iloc[7])
header_lgth = len(header_names)

#Declaring list with start date one month before data set Jan 2004
Date_list = [dt.date(2003,12,1)]
i =0
#creating new monthly header that will contain dates for further analysis
while i < header_lgth-1:
    Day2EOM = calendar.monthrange(Date_list[i].year,Date_list[i].month)[1]
    Date_list.insert(i+1,Date_list[i]+dt.timedelta(Day2EOM)) # Moving to next month
    Date_list[i] = Date_list[i].strftime("%Y%m%d") #removing seperators "-" from date. Ease cross platform analysis.
    i += 1

#Changing final date in loop - TEMP FIX
Date_list[len(Date_list)-1] = int(Date_list[i].strftime("%Y%m%d"))

#First field of header blank
Date_list[0] = ""

TobaccoSales.columns = Date_list

#Selecting revelant rows.  
TobaccoSales = TobaccoSales.iloc[9:13]

#setting table dimentions for while loop
Num_Col = len(TobaccoSales.columns)
Num_row = len(TobaccoSales.index)

i_column = 0
i_row = 0

#Letter "x" to be replaced by "NaN"
Letter_Ex = TobaccoSales.iloc[2,204]

#replacing "x" with "Na"
while i_column < Num_Col:
    while i_row < Num_row:
        Cell = TobaccoSales.iloc[i_row,i_column]
        if Cell == Letter_Ex:
            TobaccoSales.iloc[i_row,i_column]= nan
            i_row += 1
        else:
            i_row += 1
    i_column += 1
    i_row =0


#Converting strings to floats
#setting tabale dimensions
Num_Col = len(TobaccoSales.columns)
Num_row = len(TobaccoSales.index)

#Setting Column starting position at one to avoid string convertion error. 
i_column = 1
i_row = 0

#removing "," from numbers and converting them to floats
while i_column < Num_Col:
    while i_row < Num_row:
        if pd.isna(TobaccoSales.iloc[i_row,i_column]):
            i_row += 1
        else:
            TobaccoSales.iloc[i_row,i_column]  = float(TobaccoSales.iloc[i_row, i_column].replace(",",""))
            i_row += 1
    i_column += 1
    i_row = 0

TobaccoSales.to_csv("TobaccoSales(Clean).csv", index = False)
TobaccoSales = pd.read_csv("TobaccoSales(Clean).csv")

print(TobaccoSales)

#--------------------------------------Population CSV Cleaning---------------------------------------------

#Defining headers to pre-exisiting row and resetting header.   
header_names = list(CanPop.iloc[5])
header_names[0] = NaN # setting first index to NA 
CanPop.columns = header_names

#Slecting relevant table
CanPop = CanPop.iloc[7:21]

#Converting numbers from strings to floats
#setting tabale dimensions
Num_Col = len(CanPop.columns)
Num_row = len(CanPop.index)

#Setting Column starting position at one to avoid string convertion error. 
i_column = 1
i_row = 0

#removing "," from numbers and converting them to floats
while i_column < Num_Col:
    while i_row < Num_row:
        CanPop.iloc[i_row,i_column]  = float(CanPop.iloc[i_row, i_column].replace(",",""))
        i_row += 1
    i_column += 1
    i_row = 0

#***Save to new file without index columun. Open new file to confirm***
CanPop.to_csv("CanadaPopulation(Clean).csv", index = False)
CanPop = pd.read_csv("CanadaPopulation(Clean).csv")
print(CanPop.head(5))
