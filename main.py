from test_steps import Driver
import time


def main():
    driver = Driver("opera")
    driver.setup()
    driver.add_to_basket("cytryny")
    print("done")


if __name__ == '__main__':
    main()
