#!/usr/bin/python3
import requests
import bs4
from splinter import Browser


class SupremeBot:
    def __init__(self, **info):
        self.base_url = "https://supremenewyork.com/"
        self.shop_ext = "shop/all/"
        self.checkout_ext = "checkout/"
        self.info = info

    def init_browser(self):
        self.b = Browser('chrome')

    def find_product(self):
        try:
            r = requests.get("{}{}{}".format(
                self.base_url, self.shop_ext, self.info["category"])).text
            print(r)
            soup = bs4.BeautifulSoup(r, 'lxml')
            temp_tuple = []
            temp_link = []
            print(soup)

            for link in soup.find_all("a", href=True):
                temp_tuple.append((link["href"], link.text))

            for i in temp_tuple:
                if i[1] == self.info["product"] or i[1] == self.info["color"]:
                    temp_link.append(i[0])

            self.final_link = list(
                set([x for x in temp_link if temp_link.count(x) == 2]))[0]
            print(self.final_link)
        except requests.ConnectionError as e:
            print("Failed to open url")

    def visit_site(self):
        self.b.visit("{}{}".format(self.base_url, str(self.final_link)))
        self.b.find_option_by_text(self.info["size"]).click()
        self.b.find_by_value('add to basket').click()

    def checkout_func(self):
        self.b.visit("{}{}".format(self.base_url, self.checkout_ext))
        self.b.fill("order[billing_name]", self.info["infofield"])
        self.b.select("order[billing_country]", self.info["country"])
        self.b.fill("order[email]", self.info["emailfield"])
        self.b.fill("order[tel]", self.info["phonefield"])

        self.b.fill("order[billing_address]", self.info["addressfield"])
        self.b.fill("order[billing_city]", self.info["city"])
        self.b.fill("order[billing_zip]", self.info["zip"])

        self.b.select("credit_card[type]", self.info["card"])
        self.b.fill("credit_card[cnb]", self.info["number"])
        self.b.select("credit_card[month]", self.info["month"])
        self.b.select("credit_card[year]", self.info["year"])
        self.b.fill("credit_card[ovv]", self.info["ccv"])
        self.b.find_by_css('.terms').click()
        self.b.find_by_value("process payment").click()

    def main(self):
        self.init_browser()
        self.find_product()
        self.visit_site()
        self.checkout_func()


if __name__ == "__main__":
    INFO = {
        "driver": "geckodriver",
        "product": "Ancient S/S Top",
        "color": "Black",
        "size": "Medium",
        "category": "tops_sweaters",
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
    bot = SupremeBot(**INFO)
    bot.main()
