from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import sys
import get_single_urls as g

BASE_URL = r"http://remixmaza.in/categorylist/4/album_latest_remix/default/"


def nav_to_albums_page(driver, page_num):
    driver.get(BASE_URL + str(page_num))


def get_all_songs(driver):
    g.get_all_file_links(driver)

def get_all_album_links(driver):
    albums = driver.find_elements(By.CLASS_NAME, "catRow")
    index = 0
    while index < len(albums):
        print(f"album = {index}")
        album= albums[index]
        album.click()
        time.sleep(1)
        get_all_songs(driver)
        driver.execute_script("window.history.go(-1)")
        time.sleep(1)
        albums = driver.find_elements(By.CLASS_NAME, 'catRow')
        index += 1


MISSED = [5, 10, 12, 14]
if __name__ == '__main__':
    chrome = g.launch_chrome()
    #try:
    start = 15
    for page in range(start, 21+1):
        print(f"Album Page {page}")
        nav_to_albums_page(chrome, page)
        get_all_album_links(chrome)
    time.sleep(10)
    #except:
    #    chrome.quit()
