from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

def login(driver):
    driver.find_element(
    By.XPATH, "//*[@id='__layout']/div/div[1]/div[1]/div/ul/li[4]/a").send_keys(Keys.ENTER)

    id = "tldldh1212@naver.com"
    pw = "4uaOV!rg"

    driver.find_element(
        By.XPATH, "//div[@class='login_area']/div[1]/div/input").send_keys(id)
    driver.find_element(
        By.XPATH, "//div[@class='login_area']/div[2]/div/input").send_keys(pw)
    driver.find_element(
        By.XPATH, "//div[@class='login_area']/div[3]/a").send_keys(Keys.ENTER)

    