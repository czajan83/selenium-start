import re
import time

from selenium import webdriver
from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from webdriver_manager.chrome import ChromeDriverManager

COOKIES_ACC_BTN_XPATH = f"//*[@id=\"wrapper\"]/div[1]/div/div/div[2]/div/button[1]"
SEARCH_EDITTEXT_XPATH = f"//*[@id=\"header\"]/div[1]/div/div[2]/div/div/form/input"
SEARCH_EDITTEXT_CLEAR_XPATH = f"//*[@id=\"header\"]/div[1]/div/div[2]/div/div/form/div[1]"


def get_xpath_for_shelf_element(element):
    return f"//*[@id=\"page-content\"]/div/div[2]/div/div[3]/div/div[{element}]/div/div/div/div/div[3]/div[3]/a/span[" \
           f"2]/span"


def get_xpath_for_price(element, part):
    return f"//*[@id=\"page-content\"]/div/div[2]/div/div[3]/div/div[{element}]/div/div/div/div/div[3]/div[3" \
           f"]/div/div[2]/div/div/span/span[{part}]"


def get_xpath_for_amount(element):
    return f"//*[@id=\"page-content\"]/div/div[2]/div/div[3]/div/div[{element}]/div/div/div/div/div[3]/div[3" \
           f"]/a/span[3]/span[2]"


def get_xpath_for_add_to_basket(element):
    return f"//*[@id=\"page-content\"]/div/div[2]/div/div[3]/div/div[{element}]/div/div/div/div/div[3]/div[3" \
           f"]/div/div[3]"


def get_xpath_for_order_more(element):
    return f"//*[@id=\"page-content\"]/div/div[2]/div/div[3]/div/div[{element}]/div/div/div/div/div[3]/div[3" \
           f"]/div/div[3]/div[3]"


def get_xpath_for_button_text(element):
    return f"//*[@id=\"page-content\"]/div/div[2]/div/div[3]/div/div[{element}]/div/div/div/div/a"


def get_xpath_for_first_product():
    return f"//*[@id=\"page-content\"]/div/div[2]/div/div[3]/div/div[1]/div/div/div/div"


class Driver:
    def __init__(self, browser="chrome"):
        if browser == "chrome":
            options_2 = Options()
            self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options_2)
            self.driver.maximize_window()
            self.wait_cookies_banner = WebDriverWait(self.driver, 20)
            self.wait_products_shelf = WebDriverWait(self.driver, 10)

    def setup(self, website="https://www.frisco.pl"):
        self.driver.get(website)
        self.wait_cookies_banner.until(ec.presence_of_element_located((By.XPATH, COOKIES_ACC_BTN_XPATH)))
        self.driver.find_element(By.XPATH, COOKIES_ACC_BTN_XPATH).click()

    def add_to_basket(self, product, amount=0):
        self.driver.find_element(By.XPATH, SEARCH_EDITTEXT_XPATH).send_keys(f"{product}\n")
        self.wait_products_shelf.until(ec.presence_of_element_located((By.XPATH, get_xpath_for_first_product())))
        iteration = 1
        the_cheapest = 0
        the_cheapest_price = 1000000
        while iteration < 11:
            try:
                if self.driver.find_element(By.XPATH, get_xpath_for_button_text(iteration)).text == f"Zobacz promocję":
                    iteration += 1
                    continue
            except NoSuchElementException:
                pass
            try:
                found_product = self.get_product_name(iteration)
                if product.lower() in found_product.lower():
                    price = self.get_product_price(iteration)
                    amount = self.get_product_amount(iteration)
                    unit_price = float(price.replace(",", ".")) / amount
                    if unit_price < the_cheapest_price:
                        the_cheapest = iteration
                        the_cheapest_price = unit_price
            except NoSuchElementException:
                pass
            except TimeoutException:
                print("a")
                break
            finally:
                iteration += 1
        self.driver.find_element(By.XPATH, get_xpath_for_add_to_basket(the_cheapest)).click()
        # self.driver.find_element(By.XPATH, get_xpath_for_order_more(the_cheapest)).click()
        self.driver.find_element(By.XPATH, SEARCH_EDITTEXT_CLEAR_XPATH).click()
        time.sleep(1)

    def get_product_name(self, iteration):
        xpath = get_xpath_for_shelf_element(iteration)
        self.wait_products_shelf.until(ec.presence_of_element_located((By.XPATH, xpath)))
        return self.driver.find_element(By.XPATH, xpath).text

    def get_product_price(self, element):
        part_1 = self.driver.find_element(By.XPATH, get_xpath_for_price(element, 1)).text
        part_2 = self.driver.find_element(By.XPATH, get_xpath_for_price(element, 2)).text
        part_3 = self.driver.find_element(By.XPATH, get_xpath_for_price(element, 3)).text
        return part_1 + part_2 + part_3

    def get_product_amount(self, element):
        amount = self.driver.find_element(By.XPATH, get_xpath_for_amount(element)).text
        pattern = re.compile(r"[0-9]+")
        num_amount = int(pattern.findall(amount)[0])
        if "g" in amount and "kg" not in amount:
            num_amount /= 1000
        return num_amount
