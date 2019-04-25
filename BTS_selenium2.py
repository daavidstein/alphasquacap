from selenium import webdriver
from selenium.webdriver.support.ui import Select

driver = webdriver.Chrome()

#pull up the website
driver.get("https://www.transtats.bts.gov/Tables.asp?DB_ID=120&DB_Name=Airline%20On-Time%20Performance%20Data&DB_Short_Name=On-Time#")

driver.find_element_by_xpath("//a[contains(@onclick, '236')][contains(text(), 'Download')]").click() #this clicks the second download link corresponding to "Reporting Carrier On-Time Performance (1987-present)"

#check boxes of fields we want (don't click checkboxes of fields we want that are already checked by default)
#obviously this would be more compact as a for loop but for some reason the checkboxes werent behaving with for loops.
driver.find_element_by_xpath("//input[contains(@title, 'Year')]").click()
driver.find_element_by_xpath("//input[contains(@title, 'Month')]").click()
driver.find_element_by_xpath("//input[contains(@title, 'DayofMonth')]").click()
driver.find_element_by_xpath("//input[contains(@title, 'FlightDate')]").click()
driver.find_element_by_xpath("//input[contains(@title, 'Reporting_Airline')]").click()
driver.find_element_by_xpath("//input[contains(@title, 'DOT_ID_Reporting_Airline')]").click()
driver.find_element_by_xpath("//input[contains(@title, 'Tail_Number')]").click()
driver.find_element_by_xpath("//input[contains(@title, 'Flight_Number_Reporting_Airline')]").click()
driver.find_element_by_xpath("//input[@title='Origin']").click()
driver.find_element_by_xpath("//input[@title='Dest']").click() 
driver.find_element_by_xpath("//input[@title='DepTime']").click()
driver.find_element_by_xpath("//input[@title='DepDelay']").click() 
driver.find_element_by_xpath("//input[@title='DepDel15']").click() 
driver.find_element_by_xpath("//input[contains(@title, 'TaxiOut')]").click()
driver.find_element_by_xpath("//input[contains(@title, 'WheelsOff')]").click()
driver.find_element_by_xpath("//input[contains(@title, 'WheelsOn')]").click()
driver.find_element_by_xpath("//input[contains(@title, 'TaxiIn')]").click()
driver.find_element_by_xpath("//input[@title='ArrTime']").click() 
driver.find_element_by_xpath("//input[contains(@title, 'ArrDelay')]").click()
driver.find_element_by_xpath("//input[contains(@title, 'ArrDel15')]").click()
driver.find_element_by_xpath("//input[contains(@title, 'Cancelled')]").click()
driver.find_element_by_xpath("//input[contains(@title, 'CancellationCode')]").click()
driver.find_element_by_xpath("//input[contains(@title, 'Diverted')]").click()
driver.find_element_by_xpath("//input[contains(@title, 'Distance')]").click()
driver.find_element_by_xpath("//input[contains(@title, 'CarrierDelay')]").click()
driver.find_element_by_xpath("//input[contains(@title, 'ActualElapsedTime')]").click()
driver.find_element_by_xpath("//input[contains(@title, 'WeatherDelay')]").click()
driver.find_element_by_xpath("//input[contains(@title, 'NASDelay')]").click()
driver.find_element_by_xpath("//input[contains(@title, 'LateAircraftDelay')]").click()


for year in range(1987, 2020):
    for month in range(1,13):

        my_select = Select(driver.find_element_by_id('XYEAR')) #find the year dropdown bar
        my_select.select_by_value(str(year)) #select year
        my_select = Select(driver.find_element_by_id('FREQUENCY')) #find the months dropdown bar
        my_select.select_by_value(str(month))
        driver.find_element_by_xpath("//button[contains(@onclick, 'tryDownload()')]").click() #click the download buton
        
