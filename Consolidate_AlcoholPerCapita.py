from numpy.core.numeric import NaN
import pandas as pd
import numpy as np
import math
import datetime

from pandas._libs.missing import NA
#from pandas.io.parsers import read_csv

AlSale = pd.read_csv("AlcoholSales(Clean).csv")
CanPop = pd.read_csv("CanadaPopulation(Clean).csv")


#Alcohol sales - Annual consolidation

#Renaming Provinces & adding Id list 
NameList = ["Canada","NL","PE","NS","NB","QC","ON","MB","SK","AB","BC","YK","NT","NU"]
IDList = [NaN,"10","11","12","13","24","35","46","47","48","59","60","61","62"]

AlSale.iloc[:,0] = NameList
AlSale["PRUID"] = IDList

#saving previous header in new header
NewHeader = list(AlSale.columns)

#starting year
Year = 2000
i = 0 

#Index for year range 
StartYIndex = 1  
EndYIdex = StartYIndex + 12


#suming each year and adding new col at end of df
while Year < 2021:
    RowNum = len(AlSale.iloc[0])+i 
    AlSale[RowNum] = round((AlSale.iloc[:,StartYIndex:EndYIdex].sum(axis = 1)),0)
    NewHeader.insert(RowNum, "EOY" + str(Year) + "-AnnualSale")
    Year += 1
    StartYIndex += 12
    EndYIdex += 12

#set new header that includes years
AlSale.columns = NewHeader

#removed Monthly info. "-22" 21 years of data 2000 to 2020 + extra column for columns id  
AlSale = AlSale.drop(AlSale.iloc[:,1:(len(AlSale.columns)-22)],axis=1)

#Alcohol sales adding CAGR for Canada. Col 22 = 21 years + id
AlSale["CAN_CAGR_PCT"] = round(((AlSale.iloc[0,22]/AlSale.iloc[0,2])**(1/20)-1)*100,2)

#-------------------------------consolidating QTR population into annual

#Adding new header
NewHeader = list(CanPop.columns)

FourthQuarter = 4
Year=2000

#Selecting last quarter population size recorded
while Year < 2021:
    RowNum = len(CanPop.iloc[0])+i 
    CanPop[RowNum] = CanPop.iloc[:,FourthQuarter]
    NewHeader.insert(RowNum, "EOY" + str(Year) + "Pop")
    Year += 1
    FourthQuarter += 4

#Set new header
CanPop.columns = NewHeader

#removed Monthly informaiton  
CanPop = CanPop.drop(CanPop.iloc[:,1:(len(CanPop.columns)-21)],axis=1)

#--------------Merging both files

#merging headers
NewHeader = list(AlSale.columns)
CanPopHEader = list(CanPop.columns)
CanPopHEader.pop(0)
NewHeader = NewHeader + (CanPopHEader)

i=0

#Merging both files 
while i < 21 :
    AlSale[(len(AlSale.columns)+1)] = CanPop.iloc[:,1+i]
    i += 1

#saving new header
AlSale.columns = NewHeader

AlSale.to_csv("consolidatedAlcoholPercapita.csv", index=False)
AlcPerCap = pd.read_csv("consolidatedAlcoholPercapita.csv")

#Saving for new header
NewHeader = list(AlcPerCap.columns)

#column & row numbers
SalesYearCol = 2 
PopYearCol = 24
SalePerCapCol = len(AlcPerCap.columns)
Year = 2000

#calculating Alcohol per capita
while Year < 2021: 
    AlcPerCap[SalePerCapCol] = round((AlcPerCap.iloc[:,SalesYearCol]*1000) / AlcPerCap.iloc[:,PopYearCol],)
    NewHeader.insert(SalePerCapCol, "FY"+str(Year)+"-Alc.Per.Capita")
    Year += 1
    SalePerCapCol += 1
    SalesYearCol += 1
    PopYearCol += 1

#reset header
AlcPerCap.columns = NewHeader
AlcPerCap.to_csv("consolidatedAlcoholPercapita.csv", index=False)

#read from source
AlcPerCap = pd.read_csv("consolidatedAlcoholPercapita.csv")

#Seeting cells with 0 to blank
Total_NumCol = len(AlcPerCap.columns)
Total_NumRow = len(AlcPerCap.iloc[:,0])

ColNum = 0
RowNum = 0

while ColNum < Total_NumCol:
    while RowNum < Total_NumRow:
        if AlcPerCap.iloc[RowNum,ColNum] == 0:
             AlcPerCap.iloc[RowNum,ColNum] = NaN
             RowNum += 1
        else:
            RowNum += 1
    ColNum += 1
    RowNum = 0

AlcPerCap.to_csv("consolidatedAlcoholPercapita_GDP_Pop.csv", index=False)

# Removing all columns expect GDP per capita. manually counted columns
AlcPerCap = AlcPerCap.drop(AlcPerCap.iloc[:,2:45], axis= 1 )

Year = 2000
NewHeader = ["Province","PRUID",]

while  Year < 2021:
    NewHeader.append("FY"+str(Year))
    Year +=1

AlcPerCap.columns = NewHeader

#saving file
AlcPerCap.to_csv("consolidatedAlcoholPercapita.csv", index=False)

#------------------------GDP Growth per quarter
GDP = pd.read_csv("Canada_GDP(Clean).csv")

#Header length
OriginalHeaderlength = len(GDP.iloc[0])

Year = 2000
i = 0 

#Index for year range 
StartQIndex = 1  
EndQIndex = StartQIndex + 4

#suming each year and adding new col at end of df
while Year < 2021:
    RowNum = len(GDP.iloc[0])+i 
    GDP[RowNum] = round((GDP.iloc[:,StartQIndex:EndQIndex].mean(axis = 1)),0)
    NewHeader.insert(RowNum, "EOY" + str(Year) + "-GDP.Pcrt.Chg")
    Year += 1
    StartQIndex += 4
    EndQIndex += 4

#2020 only has 4Qs 
GDP[104] = round((GDP.iloc[:,81:84].mean(axis = 1)),0)

#Header length
NewHeaderLength = len(GDP.iloc[0])
NumIndex2000TO2020 = NewHeaderLength - OriginalHeaderlength

#removed Quarterly informaiton
GDP = GDP.drop(GDP.iloc[:,1:(len(GDP.columns)-NumIndex2000TO2020)],axis=1)

Year = 2000
Year1Index = 1

#adding Percentage change (i.e growth/decline) informaiton
while Year < 2020:
     GDP[len(GDP.iloc[0])+1] = round(((GDP.iloc[:,Year1Index+1]/GDP.iloc[:,Year1Index])-1)*100,2)
     Year1Index += 1
     Year += 1

GDP.to_csv("GDPAnnual(With_indicators).csv", index=False)
GDP = pd.read_csv("GDPAnnual(With_indicators).csv")

ColumnIndex = NumIndex2000TO2020+1 # 22 This is the first column of %

RowNum = 0 # row num 
NumOFRows = len(GDP.iloc[:,0]) #31

NumOfColumnsIndex = len(GDP.iloc[0])-1 #41

#change row need to things starting row and ending row

#save answers to new column at the end of sheet
    #Declare columns
    #populate columns
#switch columns for every index column of the percantage 
#this can be done by measuring by 
#headerlength minus NumIndex2000TO2020 minus one (for additonal row)

NumOfPercentageIndex = len(GDP.iloc[0]) - NumIndex2000TO2020 - 1
NumCol = 0

#assigns a value of Rec. or exp depending if the year was a recession or expansion.
while NumCol < NumOfPercentageIndex:   #for every columns that is a percentage 
    GDP[NumOfColumnsIndex+1] = NaN #create new column filled with no values
    while RowNum < NumOFRows: #filling empty rows loop
        if GDP.iloc[RowNum,ColumnIndex] < 0:#if statement to verif if negative or positive
            GDP.iloc[RowNum,NumOfColumnsIndex+1] = "Rec."
            RowNum += 1 
        else:
            GDP.iloc[RowNum,NumOfColumnsIndex+1] = "Exp."
            RowNum += 1 
    NumOfColumnsIndex += 1 #adds one more column
    ColumnIndex += 1
    NumCol += 1
    RowNum = 0


#Final header completed by hand
#Temp fix need Automation
GDP.columns = [NaN,'GDP.2000','GDP.2001','GDP.2002','GDP.2003','GDP.2004','GDP.2005','GDP.2006','GDP.2007','GDP.2008','GDP.2009','GDP.2010','GDP.2011',
            'GDP.2012','GDP.2013','GDP.2014','GDP.2015','GDP.2016','GDP.2017','GDP.2018','GDP.2019','GDP.2020','Prct.Chg.2001','Prct.Chg.2002',
            'Prct.Chg.2003', 'Prct.Chg.2004', 'Prct.Chg.2005', 'Prct.Chg.2006','Prct.Chg.2007', 'Prct.Chg.2008','Prct.Chg.2009', 'Prct.Chg.2010',
            'Prct.Chg.2011', 'Prct.Chg.2012', 'Prct.Chg.2013','Prct.Chg.2014','Prct.Chg.2015','Prct.Chg.2016','Prct.Chg.2017','Prct.Chg.2018','Prct.Chg.2019','Prct.Chg.2020','Status.2001',
            'Status.2002','Status.2003','Status.2004','Status.2005','Status.2006','Status.2007','Status.2008','Status.2009','Status.2010','Status.2011','Status.2012',
            'Status.2013','Status.2014','Status.2015','Status.2016','Status.2017','Status.2018','Status.2019','Status.2020',]

#writing file
GDP.to_csv("GDPAnnual(With_indicators).csv", index=False)