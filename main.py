from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time


def main():
    driver = webdriver.Chrome(service=Service("chromedriver.exe"))
    driver.get("https://www.softest.com.pl")
    time.sleep(5)
    print(driver.title)


if __name__ == '__main__':
    main()
