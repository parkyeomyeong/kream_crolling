from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import time
import csv
import re


def get_product_info(PRODUCT_PID, category, driver):
    # product_brand = ''
    # product_name_english = ''
    # product_name_korean = ''
    # product_info_model_number = ''
    # product_info_release_date = ''
    # product_info_color = ''
    # product_info_release_product = ''
    product_img = []
    product_size = []

    time.sleep(0.2)
    product_brand = driver.find_element(
        By.XPATH, "//*[@class='main_title_box']/div/a").text

    
    product_name_english = driver.find_element(
        By.XPATH, "//*[@class='main_title_box']/p[1]").text
    product_name_korean = driver.find_element(
        By.XPATH, "//*[@class='main_title_box']/p[2]").text

    print(product_name_korean, end=" ")

    # 이미지
    img_len = len(driver.find_elements(
        By.XPATH, "//*[@class='slide_item']"))+1

    idx = 0
    for i in range(1, img_len):
        if idx >= 5:
            break
        product_img.append(driver.find_element(
            By.XPATH, f"//*[@class='slick-track'][1]/div[{i}]/div/div/div/div/div/picture/img").get_attribute('src'))
        idx += 1

    # 이미지 백그라운드 RGB 가져오기
    rgb = driver.find_element(
        By.XPATH, "//*[@class='slide_item']").get_attribute('style')
    rgb_list = rgb.split(',')

    r = re.sub(r'[^0-9]', '', rgb_list[0])
    g = re.sub(r'[^0-9]', '', rgb_list[1])
    b = re.sub(r'[^0-9]', '', rgb_list[2])

    # 카테고리가 패션 잡화일경우 ONE SIZE라서 사이즈 안봐도 됨
    if category != 4:
        # 사모든 사이즈 보기 버튼 누르기
        driver.find_element(
            By.XPATH, "//*[@class='btn_size']").send_keys(Keys.ENTER)
        # 사이즈들
        sizes = driver.find_elements(
            By.XPATH, "//*[@class='select_list']/li")

        for size in range(1, len(sizes)+1):
            product_size.append(driver.find_element(
                By.XPATH, f"//*[@class='select_list']/li[{size}]/button/div/span[1]").text)

        # 사이즈보기 닫기버튼 누르기
        driver.find_element(
            By.XPATH, "//*[@class='btn_layer_close']").send_keys(Keys.ENTER)
    # 만약 product_size의 크기가 0 이면 원사이즈지
    if len(product_size) == 0:
        product_size.append("ONE SIZE")

    product_info_model_number = driver.find_element(
        By.XPATH, "//*[@class='detail_product']/div[1]/dd").text
    product_info_release_date = driver.find_element(
        By.XPATH, "//*[@class='detail_product']/div[2]/dd").text
    product_info_color = driver.find_element(
        By.XPATH, "//*[@class='detail_product']/div[3]/dd").text
    product_info_release_product = re.sub(r'[^0-9]', '', driver.find_element(By.XPATH,
                                                                             "//*[@class='detail_product']/div[4]/dd").text.split("(")[-1])

    # 제품 상세 csv
    with open(f'out/product_table.csv', 'a') as f:
        wr = csv.writer(f, lineterminator='\n')
        row = []
        row.append(PRODUCT_PID)
        row.append(category-1)#카테고리는 변호로
        row.append(product_brand)
        row.append(product_name_english)
        row.append(product_name_korean)
        row.append(r)
        row.append(g)
        row.append(b)
        row.append(product_info_model_number)
        row.append(product_info_release_date)
        row.append(product_info_color)
        row.append(product_info_release_product)
        for img in product_img:
            row.append(img)
        wr.writerow(row)
    # 제품 사이즈 csv
    with open(f'out/product_size_table.csv', 'a') as f:
        wr = csv.writer(f, lineterminator='\n')
        for size in product_size:
            row = []
            row.append(PRODUCT_PID)
            row.append(product_info_model_number)
            row.append(size)
            row.append(0)#가격
            wr.writerow(row)
        