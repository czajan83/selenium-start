import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


class Driver:
    def __init__(self, browser="chrome"):
        if browser == "chrome":
            self.driver = webdriver.Chrome(service=Service("chromedriver.exe"))
            self.driver.maximize_window()
            self.wait = WebDriverWait(self.driver, 20)

    def setup(self, website="https://www.frisco.pl"):
        self.driver.get(website)
        self.wait.until(ec.presence_of_element_located((By.XPATH, "//*[@id=\"wrapper\"]/div[1]/div/div/div[2]/div/button[1]")))
        self.driver.find_element(By.XPATH, "//*[@id=\"wrapper\"]/div[1]/div/div/div[2]/div/button[1]").click()
        self.driver.find_element(By.XPATH, "//*[@id=\"header\"]/div[1]/div/div[2]/div/div/form/input").\
            send_keys("cytryny\n")
        time.sleep(15)
