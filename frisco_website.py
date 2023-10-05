import re
from selenium.common.exceptions import NoSuchElementException
from test_steps import Driver
from sensitive_data import FriscoSensitiveData as fsd

SEARCH_EDITTEXT_CLEAR_XPATH = f"//*[@id=\"header\"]/div[1]/div/div[2]/div/div/form/div[1]"


def get_xpath_for_add_to_basket(element):
    return f"//*[@id=\"page-content\"]/div/div[2]/div/div[3]/div/div[{element}]/div/div/div/div/div[3]/div[3" \
           f"]/div/div[3]"


def get_xpath_for_order_more(element):
    return f"//*[@id=\"page-content\"]/div/div[2]/div/div[3]/div/div[{element}]/div/div/div/div/div[3]/div[3" \
           f"]/div/div[3]/div[3]"


class FriscoWebsite(Driver):
    COOKIES_ACC_BTN_XPATH = f"//*[@id=\"wrapper\"]/div[1]/div/div/div[2]/div/button[1]"
    SEARCH_EDITTEXT_XPATH = f"//*[@id=\"header\"]/div[1]/div/div[2]/div/div/form/input"
    FIRST_PRODUCT_ON_LIST_XPATH = f"//*[@id=\"page-content\"]/div/div[2]/div/div[3]/div/div[1]/div/div/div/div"
    LOGIN_XPATH = f"//*[@id=\"header\"]/div[1]/div/div[3]/div/button[1]"
    EMAIL_XPATH = f"//*[@id=\"email\"]"
    PASSWORD_XPATH = f"//*[@id=\"password\"]"
    LOGIN_BUTTON_XPATH = f"//*[@id=\"page-content\"]/div/div[2]/div/div[2]/form/div[3]/button"

    def __init__(self, browser):
        super().__init__(browser)
        self.wait = None
        self.iteration = None
        self.the_cheapest = None
        self.the_cheapest_price = None
        self.unit_price = None
        self.product = None
        self.found_product = None
        self.price = None
        self.amount = None

    def get_xpath_for_shelf_element(self):
        return (f"//*[@id=\"page-content\"]/div/div[2]/div/div[3]/div/div[{self.iteration}]/div/div/div/div/div["
                f"3]/div[3]/a/span[2]/span")

    def get_xpath_for_price(self, part):
        return (f"//*[@id=\"page-content\"]/div/div[2]/div/div[3]/div/div[{self.iteration}]/div/div/div/div/div["
                f"3]/div[3]/div/div[2]/div/div/span/span[{part}]")

    def get_xpath_for_amount(self):
        return (f"//*[@id=\"page-content\"]/div/div[2]/div/div[3]/div/div[{self.iteration}]/div/div/div/div/div["
                f"3]/div[3]/a/span[3]/span[2]")

    def get_xpath_for_button_text(self):
        return f"//*[@id=\"page-content\"]/div/div[2]/div/div[3]/div/div[{self.iteration}]/div/div/div/div/a"

    def open_website(self):
        self.driver.get(f"http://www.frisco.pl")
        self.click_locator(self.COOKIES_ACC_BTN_XPATH)

    def login(self):
        self.click_locator(self.LOGIN_XPATH)
        self.type_text_to_locator(self.EMAIL_XPATH, f"aaaa")
        self.type_text_to_locator(self.PASSWORD_XPATH, f"aaaa")
        self.click_locator(self.LOGIN_BUTTON_XPATH)

    def refresh_the_cheapest_product(self):
        if self.unit_price < self.the_cheapest_price:
            self.the_cheapest = self.iteration
            self.the_cheapest_price = self.unit_price

    def scrap_product(self):
        self.found_product = self.get_product_name()
        if self.product.lower() in self.found_product.lower():
            self.price = self.get_product_price()
            self.amount = self.get_product_amount()
            self.unit_price = float(self.price.replace(",", ".")) / self.amount
            self.refresh_the_cheapest_product()

    def check_promotional_product(self):
        try:
            self.check_locator(self.get_xpath_for_button_text())
            self.iteration += 1
            return True
        except NoSuchElementException:
            pass
        return False

    def check_next_product(self):
        try:
            self.scrap_product()
        except NoSuchElementException:
            return False
        self.iteration += 1
        return True

    def add_to_basket(self, product, amount=0):
        self.type_text_to_locator(self.SEARCH_EDITTEXT_XPATH, product)
        self.wait_for_locator(self.FIRST_PRODUCT_ON_LIST_XPATH)
        self.iteration = 1
        self.the_cheapest = 0
        self.the_cheapest_price = 1000000
        self.product = product
        while self.iteration < 11:
            if self.check_promotional_product() is True:
                continue
            if self.check_next_product() is False:
                break
        # self.driver.find_element(By.XPATH, get_xpath_for_add_to_basket(the_cheapest)).click()
        # self.driver.find_element(By.XPATH, get_xpath_for_order_more(the_cheapest)).click()
        # self.driver.find_element(By.XPATH, SEARCH_EDITTEXT_CLEAR_XPATH).click()

    def get_product_name(self):
        return self.get_locator_text(self.get_xpath_for_shelf_element())

    def get_product_price(self):
        part_1 = self.get_locator_text(self.get_xpath_for_price(1))
        part_2 = self.get_locator_text(self.get_xpath_for_price(2))
        part_3 = self.get_locator_text(self.get_xpath_for_price(3))
        return part_1 + part_2 + part_3

    def get_product_amount(self):
        amount = self.get_locator_text(self.get_xpath_for_amount())
        pattern = re.compile(r"[0-9]+")
        num_amount = int(pattern.findall(amount)[0])
        if "g" in amount and "kg" not in amount:
            num_amount /= 1000
        return num_amount
