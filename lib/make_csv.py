import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import re
import time


def SaveProductDetail():
    with open(f'out/product_table.csv', 'a') as f:
        wr = csv.writer(f, lineterminator='\n')
        row = []
        wr.writerow(row)

