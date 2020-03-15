# SAPMetadata
This program creates metadata of an SAP table.

# Prerequisite

__1. Python:__
Python 3 needs to be installed for this program to run. If python is not installed yet, please download Python 3 from link below and set up python environment
Download link for python(windows): https://www.python.org/downloads/windows/

__2. Selenium:__
Program installs Selenium automatically if Selenium is missing. To manually install Selenium, use the command below in command prompt/ powershell window:

> pip install selenium --user

__3. BeautifulSoup:__
Program installs BeautifulSoup automatically, if BeautifulSoup is missing. To manually install BeautifulSoup, use the command below in command prompt/ powershell window:

> pip install bs4 --user

__4. Pandas:__
Program installs Pandas automatically, if it's missing. To manually install Pandas, use the command below in command prompt/ powershell window:

> pip install pandas --user
> pip install xlsxwriter --user

__5. ChromeDriver:__
Download chromedriver from here:https://chromedriver.chromium.org/downloads or use the one in the folder). 

# Configuration:
config.ini file could be updated to change the target directory. By default a 'target' directory is created in the current folder where the utput files are placed.
Program doesn't support change of any other config at the moment.

# How to run:
1. Open Command Prompt/ Powershell Window at the file location
2. Run the metadata.py file(or metadata.pyc) with the table names as argument. 
    > python metadata.py -t \<SAP Tables>

    example:
    > python metadata.py -t VBAP VBAK
    
    Note: Replace metadata.py with metadata.pyc if running with the compiled binary.
    > python metadata.pyc -t VBAP VBAK


# Final Column Sequence:
Number-Field-Key-Data Element-Domain-Data Type-   Length-Decimal-Description-Check Table    