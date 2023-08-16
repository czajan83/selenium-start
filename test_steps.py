import time

from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.service import Service

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

COOKIES_ACC_BTN_XPATH = f"//*[@id=\"wrapper\"]/div[1]/div/div/div[2]/div/button[1]"
SEARCH_EDITTEXT_XPATH = f"//*[@id=\"header\"]/div[1]/div/div[2]/div/div/form/input"

class Driver:
    def __init__(self, browser="chrome"):
        if browser == "chrome":
            self.driver = webdriver.Chrome(service=Service("chromedriver.exe"))
            self.driver.maximize_window()
            self.wait = WebDriverWait(self.driver, 20)

    def setup(self, website="https://www.frisco.pl"):
        self.driver.get(website)
        self.wait.until(ec.presence_of_element_located((By.XPATH, COOKIES_ACC_BTN_XPATH)))
        self.driver.find_element(By.XPATH, COOKIES_ACC_BTN_XPATH).click()

    def add_to_basket(self, product, amount):
        self.driver.find_element(By.XPATH, SEARCH_EDITTEXT_XPATH).send_keys(f"{product}\n")
        try:
            print(self.driver.find_element(By.XPATH,
                                           "//*[@id=\"page-content\"]/div/div[2]/div/div[3]/div/div[4]/div/div/div/div/div[3]/div[3]/a/span[2]/span").text)
        except NoSuchElementException:
            print("Unable to find the element on website")
