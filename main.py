from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from lib import scroll_down, login, crolling_product, make_csv

import re
import time
import datetime


def app():

    program_start = time.time()
    TOTAL = 0
    FAIL = 0
    driver = webdriver.Chrome("C:\Dev\chromedriver_win32\chromedriver.exe")

    # 우선 SHOP으로 이동
    driver.get("https://kream.co.kr/search")
    driver.implicitly_wait(3)

    # product detail 볼 새창 하나 더 띄우기
    driver.execute_script("window.open()")

    # 로그인
    login.login(driver)
    time.sleep(1)

    PRODUCT_PID = 1

    # 신발, 의류, 패션 잡화 순서대로 3개 카테고리 크롤링
    for i in range(2, 5):
        driver.find_element(
            By.XPATH, f"//*[@class='quick_filter_items']/a[{i}]").send_keys(Keys.ENTER)

        time.sleep(1)

        s = time.time()
        # 끝까지 스크롤 내리기
        # scroll_down.infinite_loop(driver)
        e = time.time()
        print(f"스크롤하는데 시간 : {datetime.timedelta(seconds=(e-s))}")
        # 물건들 목록 가져오기
        products_len = len(driver.find_elements(
            By.XPATH, "//div[@class='search_result_list']/div"))

        product_list = [
            link.find_element(By.XPATH, "./a[@class='item_inner']").get_attribute('href') for link in driver.find_elements(By.XPATH, "//div[@class='product_card']")
        ]
        print(product_list)
        driver.switch_to.window(driver.window_handles[1])
        for next_product in product_list:

            # driver.find_element(
            #     By.XPATH, f"//div[@class='search_result_list']/div[{i}]/a").send_keys(Keys.ENTER)

            driver.get(next_product)
            driver.implicitly_wait(1)
            time.sleep(0.1)
            try:
                TOTAL += 1
                crolling_product.get_product_info(PRODUCT_PID, i, driver)
                PRODUCT_PID += 1
                print("\t성공 ")
            except:
                FAIL += 1
                print("\t----------이 제품은 크롤링 실패-----------")
        driver.switch_to.window(driver.window_handles[0])

        # break
    driver.close()
    program_end = time.time()
    print(
        f"프로그램 러닝타임 : {datetime.timedelta(seconds=(program_end-program_start))}")
    print(
        f"총 물건 : {TOTAL},성공 : {TOTAL-FAIL}/{TOTAL},실패 : {FAIL}/{TOTAL},확률 : {(TOTAL-FAIL)/TOTAL * 100}")


if __name__ == "__main__":
    app()
