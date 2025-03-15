import XXX1_11_Login_Logout as a
import XXX1_12_13_14_15_lang_and_coin_search as b
import time

def main():
#Running test for tasks wlb-11
    # functions_11_login = [a.test_1_1_login_popup_UI, 
    #              a.test_1_2_login_popup_SignUp, 
    #              a.test_1_2_1_login_popup_Incorrect_SignUp, 
    #              a.test_1_3_login_popup_ForgotPassword, 
    #              a. test_1_4_login_correctly, 
    #              a.test_1_5_login_incorrect, 
    #              a.test_1_6_logout_correctly, 
    #              a.test_1_7_relogin_correct]
    # for funca in functions_11_login:
    #     try:
    #         funca()
    #         time.sleep(1)
    #     except AssertionError as ae:
    #         print(f"{funca,__name__} failed with error: {ae}")

#Running test for tasks wlb-12, wlb-13, wlb-14, wlb10
    functions_12_13_14_15 = [b.test_2_2_modal_local_grid,
                             b.test_3_2_modal_currency_grid,
                             b.test_4_1_search_specific_text,
                             b.test_4_2_search_partial_text,
                             b.test_4_3_view_search_results,
                             b.test_4_4_search_and_click_specific,
                             b.test_5_1_header_logo_design]
    for funcb in functions_12_13_14_15:
        try:
            funcb()
            time.sleep(1)
        except AssertionError as ae:
            print(f"{funcb,__name__} failed with error: {ae}")

# Run the tests
if __name__ == "__main__":
    main()
    # try:
    #     test_1_7_relogin_correct()
    # except AssertionError as ae:
    #     print(f"{test_1_7_relogin_correct,__name__} failed with error: {ae}")
    