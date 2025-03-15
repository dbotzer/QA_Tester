from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
import string
from PIL import Image, ImageChops
import requests
from io import BytesIO

# setup_driver, loginUser_gig, generate_random_email, chk_required_field_msg, 

# Set up WebDriver (e.g., Chrome) 
# change language to english
def setup_driver():
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
        driver.get("https://gggggg.com") # Testing env.
        cookie_accept = driver.find_element(By.XPATH, "//*[@id='iubenda-cs-banner']/div/div/div/div[4]/div[2]/button[2]")
        cookie_accept.click() #Close cookies popup
    # Change language to English    
        language_box = driver.find_element(By.XPATH, "//*[@id='header_lang_and_coin']/div/div[1]")
        actions = webdriver.ActionChains(driver)
        actions.move_to_element(language_box).perform() 
    # Wait and open language modal
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "header_lang_and_coin")))
        driver.find_element(By.XPATH, "//*[@id='header_lang_and_coin_box']/li[1]/div/ul/li[1]").click()
    finally:
        print("Test ended correctly...")
    return driver
#-------------------------------------------------------------
# Login with user
def loginUser_gig(driver):
    try:
     # Find and click the login button
        login_button = driver.find_element(By.XPATH, "(//*[@id='login_header'])[2]")
        login_button.click()
    # Insert email and password
        input_credentials = driver.find_element(By.XPATH, "//*[@id='login_email']")
        input_credentials.send_keys("davidgigsberg@gmail.com")
        input_credentials = driver.find_element(By.XPATH, "//*[@id='login_password']")
        input_credentials.send_keys("Gigsberg2025")
        login_button = driver.find_element(By.XPATH, "//*[@id='signin_continue']")
        login_button.click()
    #Assert "Trending Events" Title is displayed 
        home_page = driver.find_element(By.XPATH, "//*[@id='homepage_events']/div[1]/div/h3")   
        wait = WebDriverWait(driver, 5)
        element = wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@id='homepage_events']/div[1]/div/h3")))
        time.sleep(4)
    finally:
        print("Login correctly")
#-------------------------------------------------------------
def generate_random_email(domain="example.com"):
    # Generate a random prefix of specified length
    length = 9
    digits = random.choice(string.digits)
    lowercase = random.choice(string.ascii_lowercase)
    uppercase = random.choice(string.ascii_uppercase)

    all_lowers = string.ascii_lowercase
    all_characters = string.ascii_letters + string.digits
    email_fill_chars = random.choices(all_lowers, k=length)
    remaining_characters = random.choices(all_characters, k=length)

    if domain == "example.com":       
        password_list = list(digits + lowercase + lowercase + ''.join(email_fill_chars))
    else:
        password_list = list(digits + lowercase + uppercase + ''.join(remaining_characters))

    random.shuffle(password_list)
    prefix = ''.join(password_list)
    # Combine the prefix with the domain
    if domain != "D":
        email = f"{prefix}@{domain}"
    else:
        email = f"{prefix}"
    return email
#-------------------------------------------------------------
def chk_required_field_msg(check_field, err_msg):
        try:            
            assert check_field == err_msg, f"Failed"
        except Exception as e:
            print("Incorrect error message displayed, got {check_field}")
            assert False, "Test failed"  
#-------------------------------------------------------------
def compare_images(image1_path, image2_url):
   # Open the original image
    original_image = Image.open(image1_path)

    # Download the image from the webpage
    response = requests.get(image2_url)
    web_image = Image.open(BytesIO(response.content))

    # Compare the two images
    diff = ImageChops.difference(original_image, web_image)

    # If images are identical, the bounding box of the difference will be None
    if diff.getbbox() is None:
        print("The images are identical.")
    else:
        print("The images are different.")
#-------------------------------------------------------------

#if __name__ == "__main__":
    