import json
import pytest
from playwright.sync_api import Playwright
from PageObjects.Login_Page import LoginPage
from Utils.API_Utils.apiBase import APIUtils

# Create json file with required test data -> Create Utility file to convert json data
# into Python data object like List/Dictonary -> Then access the data in test files

with open('Resources/TestData/credentials.json') as f:
    test_data = json.load(f)
    print(test_data)
    user_credential_list = test_data['user_credential']

@pytest.mark.parametrize('credentials', user_credential_list)
def test_e2e_api_web(playwright:Playwright, browserInstance, credentials):

    api_utils = APIUtils()
    orderId = api_utils.create_order(playwright, credentials)

    logiPage = LoginPage(browserInstance)
    logiPage.navigateToLogin()
    userEmail = credentials["userEmail"]
    userPassword = credentials["userPassword"]
    dashboard_page = logiPage.login(userEmail, userPassword)
    orderhistory_page = dashboard_page.goToOrderHistory()
    orderdetails_page = orderhistory_page.getOrderDetails(orderId)
    orderdetails_page.verifySuccessOrderMessage()
