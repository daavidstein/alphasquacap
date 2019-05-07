from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time
import os

def download_wait(directory, timeout, nfiles=None):
    """
    Wait for downloads to finish with a specified timeout.

    Args
    ----
    directory : str
        The path to the folder where the files will be downloaded.
    timeout : int
        How many seconds to wait until timing out.
    nfiles : int, defaults to None
        If provided, also wait for the expected number of files.

    """
    driver.find_element_by_xpath("//button[contains(@onclick, 'tryDownload()')]").click() #click the download button
    
    loops = 0
    dl_wait = True
    while dl_wait:
        if loops > timeout:
            break
        time.sleep(1)
        dl_wait = False
        files = os.listdir(directory)
        if nfiles and len(files) != nfiles:
            dl_wait = True

        for fname in files:
            if fname.endswith('.crdownload'): #before you run this code, make sure you delete any .crdownload files in your downloads folder.
                dl_wait = True

        loops += 1
    return loops

driver = webdriver.Chrome()
my_download_dir = "C:\\Users\\stein\\Downloads" #replace with your downloads directory

#pull up the website
driver.get("https://www.transtats.bts.gov/Tables.asp?DB_ID=120&DB_Name=Airline%20On-Time%20Performance%20Data&DB_Short_Name=On-Time#")

#this clicks the second download link corresponding to "Reporting Carrier On-Time Performance (1987-present)"
driver.find_element_by_xpath("//a[contains(@onclick, '236')][contains(text(), 'Download')]").click() 

#check boxes of fields we want (don't click checkboxes of fields we want that are already checked by default)
#obviously this would be more compact as a for loop but for some reason the checkboxes werent behaving with for loops.
driver.find_element_by_xpath("//input[contains(@title, 'Year')]").click()
driver.find_element_by_xpath("//input[contains(@title, 'Month')]").click()
driver.find_element_by_xpath("//input[contains(@title, 'DayofMonth')]").click()
driver.find_element_by_xpath("//input[contains(@title, 'FlightDate')]").click()
driver.find_element_by_xpath("//input[contains(@title, 'Reporting_Airline')]").click()
driver.find_element_by_xpath("//input[@title='Origin']").click()
driver.find_element_by_xpath("//input[@title='Dest']").click() 
driver.find_element_by_xpath("//input[@title='DepTime']").click()
driver.find_element_by_xpath("//input[@title='DepDelay']").click() 
driver.find_element_by_xpath("//input[@title='DepDel15']").click() 
driver.find_element_by_xpath("//input[@title='ArrTime']").click() 
driver.find_element_by_xpath("//input[contains(@title, 'ArrDelay')]").click()
driver.find_element_by_xpath("//input[contains(@title, 'ArrDel15')]").click()
driver.find_element_by_xpath("//input[contains(@title, 'CarrierDelay')]").click()
driver.find_element_by_xpath("//input[contains(@title, 'WeatherDelay')]").click()
driver.find_element_by_xpath("//input[contains(@title, 'NASDelay')]").click()
driver.find_element_by_xpath("//input[contains(@title, 'LateAircraftDelay')]").click()

for year in range(2000, 2018):
    for month in range(1,13):

        my_select = Select(driver.find_element_by_id('XYEAR')) #find the year dropdown bar
        my_select.select_by_value(str(year)) #select year
        my_select = Select(driver.find_element_by_id('FREQUENCY')) #find the months dropdown bar
        my_select.select_by_value(str(month))
       
        download_wait(my_download_dir, 600, nfiles=None)
        #for an extra pause after the download (should have) completed, uncomment the line below
        #time.sleep(20)
        
