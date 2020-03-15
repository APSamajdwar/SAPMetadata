from pathlib import Path
import os.path
try:
    from selenium import webdriver
except ModuleNotFoundError:
    os.system("pip install --install-option=\"--prefix={}\" selenium".format(os.path.join(project_main_folder_path, "_depedencies")))
    from selenium import webdriver

try:
    from bs4 import BeautifulSoup
except ModuleNotFoundError:
    os.system("pip install --install-option=\"--prefix={}\" bs4".format(os.path.join(".", "_depedencies")))
    from bs4 import BeautifulSoup

try:
    import pandas as pd
except ModuleNotFoundError:
    os.system("pip install --install-option=\"--prefix={}\" pandas".format(os.path.join(".", "_depedencies")))
    os.system("pip install --install-option=\"--prefix={}\" xlsxwriter".format(os.path.join(".", "_depedencies")))
    import pandas as pd

import string
from configparser import ConfigParser

def writeMetadata(sapTable):
    #Declare variable
    newRow=[]
    allElement=[]
    
    # Open page and get page source
    content = openWebdriver(sapTable)
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

    #####Modify the dataframe in the requried format####
    # Rename columns
    dfTable = dfTable.rename(columns={'length (Decimals)' : 'len', 'headField':'Key'})

    # Add/modify columns
    dfTable['Length'], dfTable['Decimal'] = zip(*dfTable['len'].map(splitDecimal))
    dfTable['Key'].replace({'keyField':'Y','otherField':''},inplace = True)
    dfTable['Domain'] = dfTable['Field']
    dfTable.insert(0, 'Number', range(1,1+len(dfTable)))

    # Drop unnecessary columns
    dfTable = dfTable.drop(['len','Conversion Routine'],axis=1)

    #Rearrange columns
    dfTable = dfTable[['Number', 'Field', 'Key', 'Data Element', 'Domain', 'Data Type', 'Length', 'Decimal', 'Description', 'Check table']]
    
    #Call writeToExcel
    writeData = writeToExcel(dfTable, sapTable)
    if writeData != '':
        print ('New metadata created: ' + writeData)
    

def openWebdriver(tableName):
    config = ConfigParser()
    config.read('config.ini')
    baseUrl = config.get('MAIN','BASEURL')
    driver = webdriver.Chrome()
    try:
        driver.get(getProcessUrl(tableName,baseUrl))
        content = driver.page_source
        driver.quit()
        return content
    except Exception:
        print ('Unable to get data for: '+tableName+'\n')
        print('Error: ')
        raise
        driver.quit()
        exit()


#Identify the link for the SAP Table
def getProcessUrl(sapTable,baseUrl):
    sapTable=sapTable.lower()
    tableIndex = sapTable[0]
    return baseUrl+tableIndex+"/"+sapTable+"/"+sapTable+".htm"


def splitDecimal(len):
    len = str(len)
    flagDecimal = len.find('(')
    if (flagDecimal!= -1):
        return len.split('(',)[0], len.split('(',)[1].strip(')')
    else:
        return len,'0'

def writeToExcel(df, tableName):
    try:
        config = ConfigParser()
        config.read('config.ini')
        targetDir = Path(config.get('MAIN', 'TARGETDIR'))
        targetDir.mkdir(parents=True, exist_ok=True)
        targetSuffix = config.get('MAIN', 'TARGETFILETYPE')
        targetFileName = tableName +'.'+ targetSuffix
        targetFile = targetDir / targetFileName
        
        #Write to a file
        writer = pd.ExcelWriter(targetFile,engine='xlsxwriter')
        df.to_excel(writer,'Sheet1',index=False)
        writer.save()
        return str(targetFile)
    except Exception:
        print('Error:')
        raise
        return ''

