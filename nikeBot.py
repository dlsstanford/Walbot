#!/usr/bin/python3
import requests
import bs4
from splinter import Browser


class FootLockerBot:
    def __init__(self, **info):
        self.base = "https://footlocker.com/"
        self.shop_ext = "category/sport/"
        self.checkout_ext = "category/sport/basketball/mens/shoes"
        self.info = info

    def init_browser(self):
        self.b = Browser('chrome')

    def find_product(self):
        try:
            r = requests.get("{}{}{}".format(
                self.base, self.shop_ext, self.info["category"])).text
            print(r)
            soup = bs4.BeautifulSoup(r, 'lxml')
            temp_tuple = []
            temp_link = []

            for link in soup.find_all("a", href=True):
                temp_tuple.append((link["href"], link.text))
            print(temp_tuple)

            for i in temp_tuple:
                if i[1] == self.info["product"] or i[1] == self.info["color"]:
                    temp_link.append(i[0])
            print(temp_link)
            self.final_link = list(
                set([x for x in temp_link if temp_link.count(x) == 2]))[0]
            print(self.final_link)
        except requests.ConnectionError as e:
            print("  Failed to open url")


if __name__ == "__main__":
    INFO = {
        "driver": "geckodriver",
        "product": "Ancient S/S Top",
        "color": "Black",
        "size": "Medium",
        "category": "shoes",
        "namefield": "example",
        "emailfield": "example@example.com",
        "phonefield": "XXXXXXXXXX",
        "addressfield": "example road",
        "city": "example",
        "zip": "72046",
        "country": "GB",
        "card": "visa",
        "number": "1234123412341234",
        "month": "09",
        "year": "2020",
        "ccv": "123"
    }
    bot = FootLockerBot(**INFO)
    bot.find_product()
