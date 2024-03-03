import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException

# Define the URL of the website you want to scrape
url = 'https://www.citygross.se/matvaror'

# Initialize Chrome webdriver
driver = webdriver.Chrome()

# Send an HTTP GET request to the URL
driver.get(url)

#maximize window to be able to see the navbar
driver.maximize_window()
ignored_exceptions=(NoSuchElementException,StaleElementReferenceException,)



with open("website_products.csv", mode = 'w', newline = '') as file:
    writer = csv.writer(file)
    writer.writerow(["Product", "Brand", "Price", "Ean"])
    try:
        elements = WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located((By.XPATH, "//span[contains(@class, 'sc-evzXkX')]")))
        

        #get all sections from the navbar
        for elem in elements:
            #for the first 10 pages
            a_tag = elem.find_element(By.TAG_NAME, 'a')
            href_value = a_tag.get_attribute('href')
            page = 1

            #access each page from the section
            page_driver = webdriver.Chrome()
            page_driver.get(href_value + "?page=" + str(page))

            page_driver.maximize_window()
            page_driver.implicitly_wait(2)
        

            #click cookie button to be able to click
            #other buttons
            WebDriverWait(page_driver, 20).until(EC.visibility_of_element_located((By.ID, 'CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll')))
            cookie_button = page_driver.find_element(By.ID, 'CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll')
            cookie_button.click()


            # get the requested information for each product
            WebDriverWait(page_driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//h2[@class="details__name h3 text-center mt-0"]')))
            products = page_driver.find_elements(By.XPATH, '//h2[@class="details__name h3 text-center mt-0"]')
            brands = page_driver.find_elements(By.XPATH, '//h3[@class="text-center mb-5 mt-0"]')
            prices = page_driver.find_elements(By.XPATH, '//span[@class="grey compare-price"]')
            elements = page_driver.find_elements(By.XPATH, '//div[@class="l-column-30_xs-30_sm-20_md-15_lg-12_xlg-10-mobileGutter"]')
            for product, brand, price, element in zip(products, brands, prices, elements):
                ean = element.get_attribute("data-productid")
                #write into a csv file
                writer.writerow([product.text, brand.text, price.text, ean])
                print(product.text + "    " + brand.text + "    " + price.text + "     " + ean)
                

            #for the pages 10+
            #same algorithm
            while products:
                page = page + 1
                page_driver = webdriver.Chrome()
                page_driver.get(href_value + "?page=" + str(page))
                page_driver.maximize_window()
                page_driver.implicitly_wait(2)


                WebDriverWait(page_driver, 20).until(EC.visibility_of_element_located((By.ID, 'CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll')))
                cookie_button = page_driver.find_element(By.ID, 'CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll')
                cookie_button.click()

                products = page_driver.find_elements(By.XPATH, '//h2[@class="details__name h3 text-center mt-0"]')
                brands = page_driver.find_elements(By.XPATH, '//h3[@class="text-center mb-5 mt-0"]')
                prices = page_driver.find_elements(By.XPATH, '//span[@class="grey compare-price"]')
                elements = page_driver.find_elements(By.XPATH, '//div[@class="l-column-30_xs-30_sm-20_md-15_lg-12_xlg-10-mobileGutter"]')
                for product, brand, price, element in zip(products, brands, prices, elements):
                    ean = element.get_attribute("data-productid")
                    writer.writerow([product.text, brand.text, price.text, ean])
                    print(product.text + "    " + brand.text + "    " + price.text + "     " + ean)

    except TimeoutException:
        print("Elements not found or unable to retrieve.")

# Close the driver
driver.quit()
