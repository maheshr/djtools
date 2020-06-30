from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import sys

BASE_URL = r"http://remixmaza.in/filelist/3/single_latest_remix/new2old/"


def launch_chrome():
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--test-type')
    return webdriver.Chrome(options=options)


def nav_to_singles_page(driver, page_num):
    driver.get(BASE_URL + str(page_num))


def get_all_file_links(driver):
    files = driver.find_elements(By.CLASS_NAME, 'fileName')
    index = 0
    while index < len(files):
        f = files[index]
        f.click()
        time.sleep(1)
        d = driver.find_element(By.CLASS_NAME, 'dwnLink')
        d.click()
        time.sleep(1)
        driver.execute_script("window.history.go(-1)")
        time.sleep(1)
        files = driver.find_elements(By.CLASS_NAME, 'fileName')
        index += 1


GO_BACK = [80]

if __name__ == '__main__':
    chrome = launch_chrome()
    try:
        start = 81
        for page in range(start, 269):
            print(f"Page {page}")
            nav_to_singles_page(chrome, page)
            get_all_file_links(chrome)
        time.sleep(10)
    except:
        chrome.quit()
