from string import ascii_lowercase
import time
from tqdm import tqdm
from math import sin, cos, tan 
from random import random
from datetime import datetime
import json

def func(x):
    x /= 500
    return (sin(1.5 * x) ** 2 + 0.5 * cos(x * 0.5) - sin(x) * tan(x * 0.1) + random() / 10 - 0.05 + 11) * 1000

a = open("data2.tsv", mode="w")
cur_dict = json.load(open("currencies.json"))
t = int(time.time())
t = int(datetime.fromisoformat(datetime.fromtimestamp(t).isoformat()[:13]).timestamp())


regions = [ ("Turkey", "TRY"),
            ("France", "EUR"),
            ("Germany", "EUR"),
            ("USA", "USD"),
            ("Pakistan", "PKR"),
            ("Israel", "ILS"),
            ("China", "CNY"),
            ("Japan", "JPY"),
            ("India", "INR"),
            ("Russian Federation", "RUB"),
            ("Poland", "PLN"),
            ("United Kingdom", "GBP"),
            ("Australia", "AUD"),
            ("Georgia", "GEL"),
            ("Hungary", "HUF")]

categories = ["Home & Kitchen",
              "Beauty & Personal Car",
              "Clothing, Shoes & Jewelry",
              "Toys & games",
              "Health, Household & Baby Care",
              "Baby",
              "Electronics",
              "Sports & outdoors",
              "Pet Supplies",
              "Office Supplies"]

K = 1036800 // 24
for e in tqdm(range(K // 6), ascii=True):
    for j, (region, currency) in enumerate(regions):
        for i, category in enumerate(categories):
            print(t + e, region, currency, category, func(t * ((e + 1) * (e + j + 2)) + e) * cur_dict[currency], file=a, sep="\t")
