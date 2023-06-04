import json
import logging
import os

from selenium import webdriver

from . import settings


def get_logger(logger_name, log_file, log_level=logging.INFO):
    if not os.path.isdir(settings.LOG_DIR):
        os.mkdir(settings.LOG_DIR)

    logger = logging.getLogger(logger_name)
    logger.setLevel(log_level)

    format = logging.Formatter(settings.LOG_FORMAT)

    file_handler = logging.FileHandler(os.path.join(settings.LOG_DIR, log_file), encoding="utf-8")
    file_handler.setFormatter(format)
    logger.addHandler(file_handler)

    return logger


def is_phone_number(s):
    s = s.replace(" ", "").replace("+", "")
    if s.isdecimal() and 8 < len(s) < 15:
        return True
    return False


def parse_information(data):
    if not data[-1]:
        data.append("")
        return data

    for s in data[-1].split("\n"):
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


def save_cookie(driver, path):
    with open(path, "w") as f:
        json.dump(driver.get_cookies(), f)


def load_cookie(driver, path):
    with open(path, "r") as f:
        cookies = json.load(f)
    for cookie in cookies:
        driver.add_cookie(cookie)


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
    option.add_experimental_option("excludeSwitches", ["enable-logging"])
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
