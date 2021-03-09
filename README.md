# Automate Data Cleansing & Consolidate files  **'Python'**
Last updated: March, 2021 <br />
By: Jordan 

*All data publicly avaiable on StatsCan [(Click Here)](https://www150.statcan.gc.ca/n1//en/type/data?MM=1#tables).*

*Prepared the below CSV files for analysis. Removed all non-pertinent information. (e.g. Drop rows and columns, new headers, ensure CSVs are ready to be manipulated). Merge alcohol sales and populaiton informaiton create new "Alcohol spending per capita" from 2000 to 2021 by province.*

* [x] Automate Cleanse 
  * [x] Canada_GDP.CSV 
  * [x] AlcoholSales.CSV
  * [x] TabaccoSales.CSV
  * [x] CanadaPopulation.csv
* [x] Merge files and create new data 
  * [x] AlcoholSales.CSV
  * [x] CanadaPopulation.csv
* [ ] Pull CSV From Source<sup>1</sup> (TBD)

*<sup>1</sup>Source: Statistics Canada*

## Snippet from 'CleanCSVFiles'
<details>
  <Summary> Click here </Summary>

``` python 

    #This block of code  takes dat from StatsCan isolates the data table, 
    #removes "clutter" and transposes the table from horizontal to vertical

    #Defining headers to pre-exisiting row and resetting header.   
    header_names = list(GDP.iloc[8])
    header_names[0] = NaN # setting first index to NA
    GDP.columns = header_names

    #Selecting relevant table
    GDP = GDP.iloc[10:41]

    #Converting strings to floats
    #Getting table dimensions
    Num_Col = len(GDP.columns)
    Num_row = len(GDP.index)

    #Indexing position at one to avoid string convertion error. 
    i_column = 1
    i_row = 0

    #removing "," from numbers and converting to floats
    while i_column < Num_Col:
        while i_row < Num_row:
            GDP.iloc[i_row,i_column]  = float(GDP.iloc[i_row, i_column].replace(",",""))
            i_row += 1
        i_column += 1
        i_row = 0

    #Saving to new file
    GDP.to_csv("Canada_GDP(Clean).csv", index = False)
```
</details>

