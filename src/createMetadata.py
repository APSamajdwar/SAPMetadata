from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import string


def writeMetadata(sapTable):
    
    #Declare variable
    newRow=[]
    allElement=[]
    
    #Open page and get page source
    driver = webdriver.Chrome()
    driver.get(getProcessUrl(sapTable))
    content = driver.page_source
    soup = BeautifulSoup(content, features="html.parser")

    #Iterate through page source and store data in array
    for tr in soup.findAll('tr',attrs={'class':['headField','keyField', 'otherField']}):
        for td in tr:
            newRow.append(td.string)
        newRow = newRow + tr['class']
        allElement.append(newRow)
        newRow=[]

    #Add to a data fram for further manipulation
    dfTable=pd.DataFrame(allElement)

    #Make 1st row as header
    newHeader=dfTable.iloc[0]
    dfTable=dfTable[1:]
    dfTable.columns = newHeader

    #Modify the dataframe in the requried format

    print(dfTable.head(3))

    # rename columns
    dfTable = dfTable.rename(columns={'length (Decimals)' : 'len', 'headField':'key'})

    # Add/modify columns
    dfTable['Length'], dfTable['Decimal'] = zip(*dfTable['len'].map(splitDecimal))
    dfTable['key'].replace({'keyField':'Y','otherField':''},inplace = True)

    #drop unnecessary columns
    dfTable.drop(['len'],axis=1)

    #Rearrange columns


    #Quick test
    print(dfTable.head(3))
    
    #Write to a file
    writer = pd.ExcelWriter('./target/metadata.xlsx',engine='xlsxwriter')
    dfTable.to_excel(writer,'Sheet1',index=False)
    writer.save()

    #Close page
    driver.quit()

#Identify the link for the SAP Table
def getProcessUrl(sapTable):
    sapTable=sapTable.lower()
    baseUrl = "https://www.se80.co.uk/saptables/"
    tableIndex = sapTable[0]
    return baseUrl+tableIndex+"/"+sapTable+"/"+sapTable+".htm"

def splitDecimal(len):
    len = str(len)
    flagDecimal = len.find('(')
    if (flagDecimal!= -1):
        return len.split('(',)[0], len.split('(',)[1].strip(')')
    else:
        return len,'0'