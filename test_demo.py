import os
import unittest
import sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from sauceclient import SauceClient

username = os.environ["SAUCE_USERNAME"]
access_key = os.environ["SAUCE_ACCESS_KEY"]

class SampleTest(unittest.TestCase):

    # setUp runs before each test case
    def setUp(self):
        caps = {
            "build": "Py-unittest",
            "name": 'firefox-test',
            "platform": 'Windows 10',
            "browserName": 'firefox',
            "version": 'latest',
        }

        self.driver = webdriver.Remote(
           command_executor="http://{}:{}@ondemand.saucelabs.com/wd/hub".format(username, access_key),
           desired_capabilities=caps)

    # tearDown runs after each test case
    def tearDown(self):
        self.driver.quit()
        sauce_client = SauceClient(username, access_key)
        status = (sys.exc_info() == (None, None, None))
        sauce_client.jobs.update_job(self.driver.session_id, passed=status)

    def test_valid_login(self):
        self.driver.get('http://www.saucedemo.com')

        self.driver.find_element_by_id('user-name').send_keys('standard_user')
        self.driver.find_element_by_id('password').send_keys('secret_sauce')
        self.driver.find_element_by_css_selector('.btn_action').click()

        assert 'inventory.html' in self.driver.current_url

    def test_invalid_login(self):
        self.driver.get('http://www.saucedemo.com')

        self.driver.find_element_by_id('user-name').send_keys('')
        self.driver.find_element_by_id('password').send_keys('')
        self.driver.find_element_by_css_selector('.btn_action').click()

        assert self.driver.find_element_by_css_selector('.error-button').is_displayed()

    def test_add_to_cart(self):
        self.driver.get('http://www.saucedemo.com/inventory.html')
        self.driver.find_element_by_class_name('btn_primary').click()

        assert self.driver.find_element_by_class_name('shopping_cart_badge').text == '1'

        self.driver.get('http://www.saucedemo.com/cart.html')
        expected = self.driver.find_elements_by_class_name('inventory_item_name')
        assert len(expected) == 1

    def test_add_and_remove_from_cart(self):
        self.driver.get('http://www.saucedemo.com/inventory.html')
        self.driver.find_element_by_class_name('btn_primary').click()
        self.driver.find_element_by_class_name('btn_primary').click()
        self.driver.find_element_by_class_name('btn_secondary').click()

        assert self.driver.find_element_by_class_name('shopping_cart_badge').text == '1'

        self.driver.get('http://www.saucedemo.com/cart.html')
        
        expected = self.driver.find_elements_by_class_name('inventory_item_name')
        assert len(expected) == 1

if __name__ == '__main__':
    unittest.main()
