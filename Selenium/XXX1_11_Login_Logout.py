from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
import string
import Header_general_def_tests as Gen # Contain general functions
    # setup_driver, loginUser_gig, generate_random_email, chk_required_field_msg

# Test 1.1: Login popup design => 
def test_1_1_login_popup_UI():
    driver = Gen.setup_driver()
    try:
    # Find and click the login button
        login_button = driver.find_element(By.XPATH, "(//*[@id='login_header'])[2]")
        login_button.click()
        login_popup = driver.find_element(By.XPATH, "//*[@id='signin']/img")
        alt_logo_text = login_popup.get_attribute("alt")
        try:            
            assert alt_logo_text == 'Gigsberg logo', f"Failed"
            print("Test 1.1 Login popup logo passed")
        except Exception as e:
            print("Popup logo does not match! Expected 'Gigsberg logo', but got {alt_logo_text}")
            assert False, "Test 1.1 Login popup UI design failed"
        time.sleep(1)
    finally:
        driver.quit()
#-------------------------------------------------------------
# Test 1.2: Login popup Sign Up => popup design, fill all fields and create user
def test_1_2_login_popup_SignUp():
    driver = Gen.setup_driver()
    try:
    # Open login popup
        login_button = driver.find_element(By.XPATH, "(//*[@id='login_btn'])[2]")
        login_button.click() ; time.sleep(1)
        signup_text = driver.find_element(By.XPATH, "//*[@id='signin']/ul/li[8]/span").text
        try:            
            assert signup_text == 'Sign Up', f"Failed"
            print("test_1_2 login popup SignUp passed")
        except Exception as e:
            print("Button Sign Up link is incorrect, got {signup_text}")
            assert False, "Test 1.2 Login popup Sign Up failed"    
        #Create new random user, mail ,password to sign in
        new_username = ''.join(random.choices(string.ascii_letters, k=10))
        random_email = Gen.generate_random_email()
        new_password = Gen.generate_random_email(domain="D")
        # Sign in process
        SignUp_popup = driver.find_element(By.XPATH, "//*[@id='signin']/ul/li[8]/span")
        SignUp_popup.click() ; time.sleep(1)
        SignUp_field = driver.find_element(By.XPATH, "//*[@id='fullname_reg']")
        SignUp_field.send_keys(new_username) ; time.sleep(1)
        SignUp_field = driver.find_element(By.XPATH, "//*[@id='email_reg']")
        SignUp_field.send_keys(random_email) ; time.sleep(1)
        SignUp_field = driver.find_element(By.XPATH, "//*[@id='password_reg']")
        SignUp_field.send_keys(new_password) ; time.sleep(1)
        SignUp_field = driver.find_element(By.XPATH, "//*[@id='register_continue']")
        SignUp_field.click() # Click Sign Up button
        time.sleep(2)
        # Examine user created and logged in
        SignUp_user = driver.find_element(By.XPATH, "(//*[@id='account_header']/a)[2]")
        chk_new_username = SignUp_user.text
        try:            
            assert new_username == chk_new_username, f"Failed"
            print("Correct username is displayed")
        except Exception as e:
            print("Incorrect username is displayed, got {chk_new_username}")
            assert False, "Test 1.2 Login popup Sign Up failed"   

        time.sleep(1)
    finally:
        print("test_1_2 login popup SignUp passed")
        driver.quit()
#-------------------------------------------------------------
# Test 1.2.1: Login popup Incorrect Sign Up
def test_1_2_1_login_popup_Incorrect_SignUp():
    driver = Gen.setup_driver()
    try: # Open login popup
        login_button = driver.find_element(By.XPATH, "(//*[@id='login_btn'])[2]")
        login_button.click() # Sign in process
        SignUp_popup = driver.find_element(By.XPATH, "//*[@id='signin']/ul/li[8]/span")
        SignUp_popup.click()        
        SignUp_field = driver.find_element(By.XPATH, "//*[@id='fullname_reg']")
        SignUp_field.send_keys(" ") # A. Insert wrong Full name       
        SignUp_field = driver.find_element(By.XPATH, "//*[@id='email_reg']")
        SignUp_field.send_keys(" ") # B. Insert wrong Email address
        SignUp_field = driver.find_element(By.XPATH, "//*[@id='password_reg']")
        SignUp_field.send_keys(" ") # C. Insert wrong Password        
        SignUp_field = driver.find_element(By.XPATH, "//*[@id='fullname_reg']")
        SignUp_field.click()
        time.sleep(3)
        check_field = driver.find_element(By.XPATH, "//*[@id='register']/ul/li[1]/div").text
        Gen.chk_required_field_msg(check_field,"Required field") # A. Check name error        
        check_field = driver.find_element(By.XPATH, "//*[@id='register']/ul/li[2]/div").text
        Gen.chk_required_field_msg(check_field,"Wrong email format") # B. Check email error                    
        check_field = driver.find_element(By.XPATH, "//*[@id='register']/ul/li[3]/div").text
        Gen.chk_required_field_msg(check_field,"Invalid password format, please see instructions below.")
        time.sleep(1) # C. Check password error
    finally:
        print("Test 1.2.1 login popup Incorrect SignUp passed")
        driver.quit()
#-------------------------------------------------------------
# Test 1.3: Login popup Forgot my password
def test_1_3_login_popup_ForgotPassword():
    driver = Gen.setup_driver()
    try: # Open login popup
        login_button = driver.find_element(By.XPATH, "(//*[@id='login_btn'])[2]"); login_button.click()
        forgotPasw = driver.find_element(By.XPATH, "//*[@id='signin']/ul/li[7]/span")
        forgotPasw.click() ; time.sleep(1) # Click Forgot the password        
        forgotPasw = driver.find_element(By.XPATH, "//*[@id='email_reset']")
        forgotPasw.send_keys("dbotzer@yahoo.com") # Insert email & click Reset
        driver.find_element(By.XPATH, "//*[@id='reset_continue']").click(); time.sleep(1)        
        correct_msg = driver.find_element(By.XPATH, "//*[@id='signin']/ul/div").text # Correct reset action msg
        Gen.chk_required_field_msg(correct_msg,"Please check your email to verify your account") # A. Check name error        
        time.sleep(1) 
    finally:
        print("Test 1.3 login popup Forgot my password passed")
        driver.quit()
#-------------------------------------------------------------
# Test 1.4: Login correctly => connect to website, close cookies, change to english
def test_1_4_login_correctly():
    driver = Gen.setup_driver()
    try:
        Gen.loginUser_gig(driver) # Login function with user
    finally:
        print("Test 1.4 Login correctly finished successfully")
        driver.quit()
#-------------------------------------------------------------
# Test 1.5: Login incorrect massages
def test_1_5_login_incorrect():
    driver = Gen.setup_driver()
    try:
        login_button = driver.find_element(By.XPATH, "(//*[@id='login_header'])[2]")
        login_button.click()
        login_button = driver.find_element(By.XPATH, "//*[@id='signin_continue']")
        login_button.click()
        incorrect_msg = driver.find_element(By.XPATH, "//*[@id='signin']/ul/li[1]/div").text # inorrect email msg
        Gen.chk_required_field_msg(incorrect_msg,"Required field") # check error message
        incorrect_msg = driver.find_element(By.XPATH, "//*[@id='signin']/ul/li[2]/div").text # inorrect psw msg
        Gen.chk_required_field_msg(incorrect_msg,"Required field") # check error message        
    finally:
        print("Test 1.5 Login incorrect finished successfully")
        driver.quit()
#-------------------------------------------------------------
# Test 1_6: Logout correctly => connect to website, close cookies, change to english
def test_1_6_logout_correctly():
    driver = Gen.setup_driver()
    try: 
        Gen.loginUser_gig(driver) # Login function with user
     # Test Logout ==> My account dropdown
        logout_button = driver.find_element(By.XPATH, "(//*[@id='user_menu']/a[4])[2]")
        actions = webdriver.ActionChains(driver)
        actions.move_to_element(logout_button).perform() 
        logout_button = driver.find_element(By.XPATH, "(//*[@id='user_menu']/a[4])[2]")
        logout_button.click()
        time.sleep(3)
    finally:
        print("Test 1.6 Logout correctly finished successfuly")
        driver.quit()
#-------------------------------------------------------------
# Test 1.7: Login correctly => connect to website, close cookies, change to english
def test_1_7_relogin_correct():
    driver = Gen.setup_driver()
    try:
        Gen.loginUser_gig(driver) # Login with user        
        logout_button = driver.find_element(By.XPATH, "(//*[@id='user_menu']/a[4])[2]")
        actions = webdriver.ActionChains(driver)
        actions.move_to_element(logout_button).perform() 
        logout_button = driver.find_element(By.XPATH, "(//*[@id='user_menu']/a[4])[2]")
        logout_button.click() # Logout with user
        time.sleep(1)        
        # Relogin with the same user
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
        time.sleep(1)
    finally:
        print("Test 1.7 Re-Login correctly finished successfully")
        driver.quit()
#-------------------------------------------------------------
def main():
    functions = [test_1_1_login_popup_UI, test_1_2_login_popup_SignUp, test_1_2_1_login_popup_Incorrect_SignUp, 
                 test_1_3_login_popup_ForgotPassword, test_1_4_login_correctly, test_1_5_login_incorrect, 
                 test_1_6_logout_correctly, test_1_7_relogin_correct]
    for func in functions:
        try:
            func()
            time.sleep(1)
        except AssertionError as ae:
            print(f"{func,__name__} failed with error: {ae}")
            
# Run the tests
if __name__ == "__main__":
    main()
    # try:
    #     test_1_2_1_login_popup_Incorrect_SignUp()
    # except AssertionError as ae:
    #     print(f"{test_1_2_1_login_popup_Incorrect_SignUp,__name__} failed with error: {ae}")