import json
import re
import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

from . import settings


def is_phone_number(s):
    s = s.replace(" ", "").replace("+", "")
    if s.isdecimal() and 8 < len(s) < 15:
        return True
    return False


def parse_information(data):
    if data[-1]:
        split_info = data[-1].split("\n")
        for s in split_info:
            subscribe_index = s.find("người theo dõi")
            if subscribe_index != -1:
                data[2] = s[:subscribe_index] + "người theo dõi"

            like_index = s.find("người thích")
            if like_index != -1:
                data[3] = s[:like_index] + "lượt thích"

            if is_phone_number(s):
                data.append(s)

    if len(data) < len(settings.OUTPUT_HEADER):
        data.append("")

    return data


def scroll_down_page(driver, speed=100, delay=2):
    current_scroll_position = driver.execute_script("return document.documentElement.scrollTop")
    new_height = current_scroll_position + 1
    while current_scroll_position <= new_height:
        current_scroll_position += speed
        driver.execute_script("window.scrollTo(0, {});".format(current_scroll_position))
        time.sleep(delay)
        new_height = driver.execute_script("return document.body.scrollHeight")


def scroll_down_to_end_page(driver, delay=2):
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(delay)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


def save_cookie(driver, path):
    with open(path, "w") as f:
        json.dump(driver.get_cookies(), f)


def load_cookie(driver, path):
    with open(path, "r") as f:
        cookies = json.load(f)
    for cookie in cookies:
        driver.add_cookie(cookie)


def is_exist_element(driver, locator):
    try:
        driver.find_element(*locator)
        return True
    except NoSuchElementException:
        return False


def urljoin(*args):
    def preprocess(url):
        while "//" in url:
            url = url.replace("//", "/")
        return url

    if len(args) < 2:
        raise TypeError("Must pass at least two arguments to this function")

    if "://" in args[0]:
        split_ = args[0].split("://")
        full_url = "/".join([split_[-1]] + list(args[1:]))
        return split_[0] + "://" + preprocess(full_url)
    else:
        full_url = "/".join(args)
        return preprocess(full_url)


def create_chrome_driver(executable_path=settings.EXECUTABLE_PATH, headless=False):
    option = webdriver.ChromeOptions()
    if headless:
        option.add_argument("--headless")
    option.add_argument("--window-size=1000,1080")
    # option.add_argument("--start-maximized")
    option.add_argument("--disable-xss-auditor")
    option.add_argument("--disable-web-security")
    option.add_argument("--allow-running-insecure-content")
    option.add_argument("--no-sandbox")
    option.add_argument("--disable-setuid-sandbox")
    option.add_argument("--disable-webgl")
    option.add_argument("--disable-gpu")
    option.add_argument("--disable-popup-blocking")
    option.add_experimental_option(
        "prefs", {"profile.default_content_setting_values.notifications": 2}
    )

    driver = webdriver.Chrome(executable_path=executable_path, chrome_options=option)
    return driver


def progress(message1, message2):
    def decorator(func):
        def wrapper(*args, **kwargs):
            print(message1)
            return_value = func(*args, **kwargs)
            print(message2)
            return return_value

        return wrapper

    return decorator


def multiprocess(max_workers, func, *args):
    process_list = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        process_list.append(executor.submit(func, *args))
    wait(process_list)
