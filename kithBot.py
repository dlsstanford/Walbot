#!/usr/bin/python3
from splinter import Browser
import bs4
import requests
import json

class KithBot:
    def __init__(self, **info):
        self.base_url = "https://kith.com/"
        self.shop_ext = "collections/"
        self.checkout_ext = "checkout/"
        self.info = info

    def init_browser(self):
        self.b = Browser('chrome')

    def find_product(self):
        try:
            r = requests.get("{}{}{}".format(
                self.base_url, self.shop_ext, self.info["category"])).text
            soup = bs4.BeautifulSoup(r, 'lxml')
            temp_tuple = []
            temp_link = []

            for link in soup.find_all("a", class_="product-card__link"):
                temp_tuple.append((link["href"], link.contents[1].text, link.contents[3].text))

            for i in temp_tuple:
                if i[1] == self.info["product"] and i[2] == self.info["color"]:
                    temp_link.append(i[0])

            self.final_link = list(
                set([x for x in temp_link if temp_link.count(x) == 1]))[0]
            print(self.final_link)
        except requests.ConnectionError as e:
            print("Failed to open url")

    def visit_site(self):
        size = '//div[@data-value='+ self.info["size"] + ']'
        self.b.visit("{}{}".format(self.base_url, str(self.final_link)))
        self.b.find_by_xpath(size).click()
        self.b.find_by_name('add').click()
        self.b.find_by_name('checkout').click()

    def shipping_func(self):
        self.b.fill("checkout[email]", self.info["emailfield"])

        self.b.fill("checkout[shipping_address][first_name]", self.info["firstName"])
        self.b.fill("checkout[shipping_address][last_name]", self.info["lastName"])
        self.b.fill("checkout[shipping_address][address1]", self.info["addressfield"])

        self.b.fill("checkout[shipping_address][city]", self.info["city"])
        self.b.fill("checkout[shipping_address][zip]", self.info["zip"])
        self.b.fill("checkout[shipping_address][phone]", self.info["phonefield"])

        self.b.find_by_id('continue_button').click()

        self.b.find_by_id('continue_button').click()

    def checkout_func(self):
        self.b.fill("number", self.info["number"])
        # self.b.fill("name", self.info["nameField"])
        # self.b.fill("expiry", self.info["expiry"])
        # self.b.fill("verification_value", self.info["ccv"])

        self.b.find_by_id('continue_button').click()

    def main(self):
        self.init_browser()
        self.find_product()
        self.visit_site()
        self.shipping_func()
        self.checkout_func()

if __name__ == "__main__":
    INFO = {
        "driver": "geckodriver",
        "product": "Puma Suede",
        "color": "Vintage Peacoat",
        "size": "12",
        "category": "mens-footwear",
        "firstName": "John",
        "lastName": "Smith",
        "nameField": "John Smith",
        "emailfield": "example@example.com",
        "phonefield": "6780870522",
        "addressfield": "example road",
        "city": "example",
        "zip": "30106",
        "country": "GB",
        "card": "visa",
        "number": "1234123412341234",
        "month": "09",
        "year": "2020",
        "expiry": "0920",
        "ccv": "123"
    }
    bot = KithBot(**INFO)
    bot.main()
