from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import string
from configparser import ConfigParser
# from selenium.webdriver.chrome.options import Options


def writeMetadata(sapTable):

    # Set file path and directory
    config = ConfigParser()
    config.read('config.ini')
    chromeDriverPath = config.get('MAIN', 'CHROMEDRIVERPATH')
    targetDir = config.get('MAIN', 'TARGETDIR')
    targetFileType = config.get('MAIN', 'TARGETFILETYPE')
    targetFile = sapTable+'.'+ targetFileType
    baseUrl = config.get('MAIN','BASEURL')

    #Declare variable
    newRow=[]
    allElement=[]
    
    # Open page and get page source
    # Get the page data without opening Browser
    # options = Options()
    # options.add_argument('--headless')
    # options.add_argument('--disable-gpu')
    # driver = webdriver.Chrome(chrome_options=options)
    # try:
    #     driver.set_page_load_timeout(10)
    #     driver.get(getProcessUrl(sapTable))
    # except Exception:
    #     print ('Time Out')
    #     driver.send_keys(Keys.CONTROL + 'Escape')


    driver = webdriver.Chrome()
    try:
        driver.get(getProcessUrl(sapTable,baseUrl))
    except Exception:
        print ('Unable to get data for: '+sapTable)
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

    #Quick Test
    # print(dfTable.head(3))
    
    #Write to a file
    writer = pd.ExcelWriter(targetDir+'\\' + targetFile,engine='xlsxwriter')
    dfTable.to_excel(writer,'Sheet1',index=False)
    writer.save()

    #Close page
    driver.quit()

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