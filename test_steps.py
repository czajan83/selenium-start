from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


class Driver:
    def __init__(self, browser="opera"):
        self.driver = None
        self.browser = browser
        self.wait_locator = None
        self.website = None

    def setup(self):
        if self.browser == "chrome":
            self.driver = webdriver.Chrome(executable_path="/home/andrzej/Development/selenium-start/chromedriver")
        else:
            self.driver = webdriver.Opera(executable_path="/home/andrzej/Development/selenium-start/operadriver")
        self.wait_locator = WebDriverWait(self.driver, 20)
        self.driver.maximize_window()

    def wait_for_locator(self, locator):
        self.wait_locator.until(ec.presence_of_element_located((By.XPATH, locator)))

    def click_locator(self, locator):
        self.wait_for_locator(locator)
        self.driver.find_element(By.XPATH, locator).click()

    def get_locator_text(self, locator):
        self.wait_for_locator(locator)
        return self.driver.find_element(By.XPATH, locator).text

    def check_locator(self, locator):
        return self.driver.find_element(By.XPATH, locator)

    def type_text_to_locator(self, locator, text):
        self.driver.find_element_by_xpath(locator).send_keys(f"{text}\n")
