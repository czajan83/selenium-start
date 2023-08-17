from test_steps import Driver


def main():
    driver = Driver()
    driver.setup()
    driver.add_to_basket("cytryny")
    driver.add_to_basket("pomarańcze")
    driver.add_to_basket("sok 100% NFC z pomarańczy wyciskanych")
    print("done")


if __name__ == '__main__':
    main()
