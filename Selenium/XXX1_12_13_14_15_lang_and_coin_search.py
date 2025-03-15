import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
import string
import Header_general_def_tests as Gen # Contain general functions
from bs4 import BeautifulSoup

#-------------------------------------------------------------
def init_driver():
    options = webdriver.ChromeOptions()
    options.add_experimental_option(
        "prefs",
        {
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
            "profile.default_content_setting_values.notifications": 2                       
        },
    )
    options.add_argument('--disable-notifications') 
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_argument("start-maximized")
    driver = webdriver.Chrome(options=options);
    try:
        driver.get("https://stage.gigsberg.com")
        cookie_accept = driver.find_element(By.XPATH, "//*[@id='iubenda-cs-banner']/div/div/div/div[4]/div[2]/button[2]")
        cookie_accept.click() #Close cookies popup
    finally:
        return driver
#-------------------------------------------------------------    
def chk_lang_coin_header(chk_field, chk_value):
        try:            
            assert chk_field == chk_value, f"Failed"
        except Exception as e:
            assert False, "Test failed"  
#-------------------------------------------------------------
# Test 2.2: Modal - Localization => position of language and flag
def test_2_2_modal_local_grid():
    driver = init_driver()
    try:
    # Open language modal
        language_box = driver.find_element(By.XPATH, "//*[@id='header_lang_and_coin']/div/div[1]")
        actions = webdriver.ActionChains(driver)
        actions.move_to_element(language_box).perform() 
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "header_lang_and_coin")))
        driver.find_element(By.XPATH, "//*[@id='header_lang_and_coin_box']/li[1]/div/ul/li[1]").click()

        langGrid = driver.find_element(By.XPATH, "//*[@id='header_lang_and_coin_box']/li[1]/div/ul")
        chkGrid = langGrid.get_property("innerHTML")
        soup = BeautifulSoup(chkGrid, "html.parser")
        country_data_dict = {}
        modalLang = ["English", "Español", "Français","Deutsch","Italiano","Русский","עברית","عربى","Magyar","Polski","Hrvatska","Português"]

        count=0
        for li in soup.find_all("li", class_="lang_li"):
            flag = li.find("img")["src"] if li.find("img") else "No Flag"
            language = li.find("span", class_="lang_name").get_text(strip=True) if li.find("span", class_="lang_name") else "No Language"
            country = li.find("img")["alt"].replace(" flag", "") if li.find("img") and "alt" in li.find("img").attrs else "No Country"
            country_data_dict[country] = [flag, language]
        # Compare extracted data with list of languages
        for country, details in country_data_dict.items():
            chk_lang_coin_header(details[1], modalLang[count])
            count+=1

        try:# Verify there are 12 languages
            assert len(country_data_dict) == 12, f"Failed"
        except Exception as e:
            assert False, "Test failed" 
    finally:
        time.sleep(3)
        print("Test successful 2.3 Modal - Localization Grid")
        driver.quit()
#-------------------------------------------------------------
# Test 3.2: Modal Currncy Localization => position of symbol and name
def test_3_2_modal_currency_grid():
    driver = init_driver()
    try:
    # Open currency modal wait for modal to open test 3.3
        currency_box = driver.find_element(By.XPATH, "//*[@id='header_lang_and_coin']/div/div[2]")
        actions = webdriver.ActionChains(driver)
        actions.move_to_element(currency_box).perform() 
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "header_lang_and_coin")))
        driver.find_element(By.XPATH, "//*[@id='header_lang_and_coin_box']/li[2]/div/ul/li[1]/span[2]").click()

        currencyGrid = driver.find_element(By.XPATH, "//*[@id='header_lang_and_coin_box']/li[2]/div/ul")
        chkGrid = currencyGrid.get_property("innerHTML")
        soup = BeautifulSoup(chkGrid, "html.parser")
        coins_data_dict = {}
        countries = ["UK", "Europe", "USA","Australia","Poland","Czech","Israel","Swiss","Argentina", "Denmark"]
        modalCoinNames = ["GBP", "EUR", "USD","AUD","PLN","CZK","ILS","CHF","ARS","DKK"]        

        count = 0
        for li in soup.find_all("li", class_="coin_li"):
            symbol = li.find("span", class_="coin_symbol").get_text(strip=True) if li.find("span", class_="coin_symbol") else "No symbol"
            coinName = li.find("span", class_="coin_name").get_text(strip=True) if li.find("span", class_="coin_name") else "No coin name"
            coins_data_dict[countries[count]] = [symbol, coinName]
            count+=1
        count = 0
        # Compare extracted data with list of languages
        for country, details in coins_data_dict.items():
            print(f"Country: {country}, Symbol: {details[0]}, Coin Name: {details[1]}")
            chk_lang_coin_header(details[1], modalCoinNames[count])
            count+=1

        try:# Verify there are 10 Coins names
            assert len(coins_data_dict) == 10, f"Failed"
            print(f"correct number of coins")
        except Exception as e:
            print(f"Icorrect number of coins, {len(coins_data_dict)}")
            assert False, "Test failed" 
    finally:
        time.sleep(3)
        print("Test 3.2: Modal Currncy Localization")
        driver.quit()
#-------------------------------------------------------------
# Test 4.1: Searchbar - Search specific text
def test_4_1_search_specific_text():
    driver = init_driver()
    try:
    # Insert search string
        searchbar_box = driver.find_element(By.XPATH, "//*[@id='header_top']/form[2]/div[1]/input")
        searchbar_box.send_keys("coldplay")
        time.sleep(1)
        search_res = driver.find_element(By.XPATH, "//*[@id='ui-id-2']")
        actions = webdriver.ActionChains(driver)
        actions.move_to_element(search_res).perform()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "ui-id-5")))

        first_result_text = driver.find_element(By.XPATH, "//*[@id='ui-id-5']").text # Coldplay
        second_result_text = driver.find_element(By.XPATH, "//*[@id='ui-id-6']").text # Rock & Pop
        chk_lang_coin_header(first_result_text, "Coldplay")
        chk_lang_coin_header(second_result_text, "Rock & Pop")
    finally:
        time.sleep(1)
        print("Test successful Test 4.1: Searchbar - Search specific text")
        driver.quit()
#-------------------------------------------------------------
# Test 4.2: Searchbar - Search specific text
def test_4_2_search_partial_text():
    driver = init_driver()
    try:
    # Insert partial search string
        searchbar_box = driver.find_element(By.XPATH, "//*[@id='header_top']/form[2]/div[1]/input")
        searchbar_box.send_keys("cold")

        time.sleep(1)
        search_res = driver.find_element(By.XPATH, "//*[@id='ui-id-2']")
        actions = webdriver.ActionChains(driver)
        actions.move_to_element(search_res).perform()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "ui-id-5")))

        first_result_text = driver.find_element(By.XPATH, "//*[@id='ui-id-5']").text
        chk_lang_coin_header(first_result_text, "Coldplay")
        first_result_cat = driver.find_element(By.XPATH, "//*[@id='ui-id-6']").text
        chk_lang_coin_header(first_result_cat, "Rock & Pop")
    finally:
        time.sleep(3)
        print("Test successful Test 4.2: Searchbar - Search partial text")
        driver.quit()
#-------------------------------------------------------------
# Test 4.3: Searchbar - View all Search results
def test_4_3_view_search_results():
    driver = init_driver()
    try:
    # Insert search string
        searchbar_box = driver.find_element(By.XPATH, "//*[@id='header_top']/form[2]/div[1]/input")
        searchbar_box.send_keys("fc barcelona")
        searchGrid = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//*[@id='ui-id-2']"))  # Replace with the dropdown's XPath or locator
    )
        searchGrid = driver.find_elements(By.XPATH, "//*[@id='ui-id-2']/li") #//*[@id='ui-id-2']
        gridLen = len(searchGrid)
        try:# Verify number of elements in search results
            assert gridLen-1 == 4, f"Failed"
            print(f"correct number of results")
        except Exception as e:
            print(f"Icorrect number of results")
            assert False, "Test failed" 

    finally:
        time.sleep(1)
        print("Test successful Test 4.3: Searchbar - view search results")
        driver.quit()
#-------------------------------------------------------------    
# Test 4.4: Searchbar - Search specific and click result
# 1. Search string
# 2. wait for search results to appear
# 3. Wait for dropdown & click first result
# 4. Wait & Verify new page is loaded
def test_4_4_search_and_click_specific():
    driver = init_driver()
    try:
    #1 Insert search string
        searchbar_box = driver.find_element(By.XPATH, "//*[@id='header_top']/form[2]/div[1]/input")
        searchbar_box.send_keys("fc barcelona")
    #2
        actions = webdriver.ActionChains(driver)
        actions.move_to_element(searchbar_box).perform() 
    #3   
        dropdownResults = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//*[@id='ui-id-2']"))
     )
        chk_text3 = driver.find_element(By.XPATH, "//*[@id='ui-id-5']").text
        clickResult = driver.find_element(By.XPATH,"//*[@id='ui-id-2']/li[2]").click()
    #4 Full new URL --> /football/barcelona-tickets
        WebDriverWait(driver, 10).until(lambda driver: "sport-tickets/football/fc-barcelona-tickets" in driver.current_url)
        assert 'football/fc-barcelona-tickets' in driver.current_url, f"Partial URL mismatch" 
    finally:
        time.sleep(1)
        print("Test successful Test 4.4: Searchbar - Search specific and click result")
        driver.quit()
#-------------------------------------------------------------    
# Test 5.1: Header Design - Verify the header logo
def test_5_1_header_logo_design():
    driver = init_driver()
    try:
    # Get the header logo Gigsberg and verify --> displayed, src not empty
        getLogo = driver.find_element(By.XPATH, "//*[@id='logo_header']/a/img")
        assert getLogo.is_displayed(), f"Logo is not displayed"
        logo_src = getLogo.get_attribute("src")
        assert logo_src, f"Logo src is empty"
        assert "logowinter1.png" in logo_src, f"Incorrect logo source url"  
    # Compare orig pic with website logo      
        Gen.compare_images("C:\\QA\\Pics\\logo.png", logo_src)
        
        im = Gen.Image.open("C:\\QA\\Pics\\logo.png")
        print("Logo format, size & mode:", im.format, im.size, im.mode)

    finally:
        time.sleep(1)
        print("Test successful Test 5.1: Header Design - Verify the header logo")
        driver.quit()
#-------------------------------------------------------------


if __name__ == "__main__":
    test_4_4_search_and_click_specific()
