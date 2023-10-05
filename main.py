from frisco_website import FriscoWebsite


def main():
    task = FriscoWebsite("chrome")
    task.setup()
    task.open_website()
    task.login()
    task.add_to_basket("cytryny")
    print("done")


if __name__ == '__main__':
    main()
