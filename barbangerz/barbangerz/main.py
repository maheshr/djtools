from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import sys


def launch_chrome():
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--test-type')
    return webdriver.Chrome(options=options)


def login(driver, user, passwd):
    driver.get("https://www.barbangerz.com/index.php")
    text_area = driver.find_element(By.XPATH, "//input[@placeholder='Login or Email']")
    text_area.send_keys(user)
    text_area = driver.find_element(By.XPATH, "//input[@placeholder='Password']")
    text_area.send_keys(passwd)
    login_button = driver.find_element(By.ID, "Login")
    login_button.click()


def browse(driver, delay):
    try:
        browse_button = WebDriverWait(driver, delay).until(
            EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Browse")))
        browse_button.click()
    except TimeoutException:
        print("Loading took too much time!")


def select_decade(driver, decade, delay):
    IDS = {'90s': '21', '10s': '23', '80s': '19', '00s': '22', '70s': '18'}

    driver.get(f"https://www.barbangerz.com/browse.php?{IDS[decade]}=1")

    try:
        WebDriverWait(driver, delay).until(
            EC.element_to_be_clickable((By.ID, IDS[decade])))

        url = f"https://www.barbangerz.com/browse.php?{IDS[decade]}=1"
        return url
    except TimeoutException:
        print("Loading took too much time!")
        sys.exit(1)


def download_all(driver, url, page):
    while True:
        driver.get(url + f"&p={page}")

        downloads = driver.find_elements_by_class_name("map_download")

        try:
            clicked = 0
            for d in downloads:
                if d.is_enabled() and d.is_displayed():
                    d.click()
                    clicked += 1

            if not clicked:
                break
        except:
            print(f"Failed on page {page}")

        page += 1


def main(args):
    driver = launch_chrome()
    login(driver, args[0], args[1])
    delay = 5
    browse(driver, delay)
    url = select_decade(driver, "00s", delay)
    print("Ready to download")
    download_all(driver, url, 1)
    time.sleep(10)
