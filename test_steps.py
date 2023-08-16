import time

from selenium import webdriver
from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.service import Service

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

COOKIES_ACC_BTN_XPATH = f"//*[@id=\"wrapper\"]/div[1]/div/div/div[2]/div/button[1]"
SEARCH_EDITTEXT_XPATH = f"//*[@id=\"header\"]/div[1]/div/div[2]/div/div/form/input"


def get_xpath_for_shelf_element(element):
    return f"//*[@id=\"page-content\"]/div/div[2]/div/div[3]/div/div[{element}]/div/div/div/div/div[3]/div[3]/a/span[" \
           f"2]/span"


def get_xpath_for_price(element, part):
    return f"//*[@id=\"page-content\"]/div/div[2]/div/div[3]/div/div[{element}]/div/div/div/div/div[3]/div[3" \
           f"]/div/div[2]/div/div/span/span[{part}]"


class Driver:
    def __init__(self, browser="chrome"):
        if browser == "chrome":
            self.driver = webdriver.Chrome(service=Service("chromedriver.exe"))
            self.driver.maximize_window()
            self.wait_cookies_banner = WebDriverWait(self.driver, 20)
            self.wait_products_shelf = WebDriverWait(self.driver, 5)

    def setup(self, website="https://www.frisco.pl"):
        self.driver.get(website)
        self.wait_cookies_banner.until(ec.presence_of_element_located((By.XPATH, COOKIES_ACC_BTN_XPATH)))
        self.driver.find_element(By.XPATH, COOKIES_ACC_BTN_XPATH).click()

    def add_to_basket(self, product, amount=0):
        self.driver.find_element(By.XPATH, SEARCH_EDITTEXT_XPATH).send_keys(f"{product}\n")
        iteration = 2
        while iteration < 11:
            try:
                found_product = self.get_product_name(iteration)
                if product.lower() in found_product.lower():
                    price = self.get_product_price(iteration)
                    print(iteration, found_product, price)
            except NoSuchElementException:
                pass
            except TimeoutException:
                pass
            finally:
                iteration += 1

    def get_product_name(self, iteration):
        xpath = get_xpath_for_shelf_element(iteration)
        self.wait_products_shelf.until(ec.presence_of_element_located((By.XPATH, xpath)))
        return self.driver.find_element(By.XPATH, xpath).text

    def get_product_price(self, element):
        part_1 = self.driver.find_element(By.XPATH, get_xpath_for_price(element, 1)).text
        part_2 = self.driver.find_element(By.XPATH, get_xpath_for_price(element, 2)).text
        part_3 = self.driver.find_element(By.XPATH, get_xpath_for_price(element, 3)).text
        return part_1 + part_2 + part_3
