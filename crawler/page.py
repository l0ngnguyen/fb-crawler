import json
import os
import time
import urllib.parse

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

from . import settings, util
from .locator import LoginPageLocator, MainPageLocator, SearchPageLocator


class BasePage(object):
    def __init__(self, driver):
        self.driver = driver

    def find_element(self, locator):
        if isinstance(locator, tuple):
            locator = [locator]

        for l in locator:
            try:
                return self.driver.find_element(*l)
            except NoSuchElementException as e:
                continue
        return None


class LoginPage(BasePage):
    locator = LoginPageLocator()
    login_url = "https://www.facebook.com/"
    cookies_path = settings.COOKIES_PATH

    def login(self, usr=None, pwd=None, use_cookie=True):
        if usr is None and pwd is None and use_cookie is False:
            raise ValueError("Use username, password or cookies")

        self.driver.get(self.login_url)
        if use_cookie:
            if os.path.exists(self.cookies_path):
                util.load_cookie(self.driver, self.cookies_path)
                self.driver.refresh()
            else:
                return False
        else:
            self.find_element(self.locator.email_input).send_keys(usr)
            self.find_element(self.locator.pwd_input).send_keys(pwd)
            self.find_element(self.locator.login_button).click()

        if self.is_login_success():
            util.save_cookie(self.driver, self.cookies_path)
            return True
        return False

    def is_login_success(self):
        if util.is_exist_element(self.driver, self.locator.check_login):
            return True
        return False


class InformationPage(BasePage):
    locator = MainPageLocator()

    @staticmethod
    def _get_info_url_from_page_url(page_url):
        if "profile.php" in page_url:
            return page_url + "&sk=about"
        return util.urljoin(page_url, "/about")

    def get_information(self, page_url, delay=4):
        self.driver.get(self._get_info_url_from_page_url(page_url))
        time.sleep(delay)

        data = [page_url]
        for locator in [
            self.locator.name,
            self.locator.subscribe_count,
            self.locator.like_count,
            self.locator.general_info,
        ]:
            element = self.find_element(locator)
            data.append(element.text if element else "")

        return util.parse_information(data)


class SearchResultsPage(BasePage):
    locator = SearchPageLocator()
    search_api = "https://www.facebook.com/search/{search_type}?q={query}"

    def search(self, query, location, search_type="pages"):
        url = self.search_api.format(search_type=search_type, query=urllib.parse.quote_plus(query))
        self.driver.get(url)
        time.sleep(5)
        self.find_element(self.locator.location_button).click()
        self.find_element(self.locator.location_input).send_keys(location)
        time.sleep(1)
        self.find_element(self.locator.first_location_button).click()

    def scroll(self, delay=1, limit_delay=5):
        while True:
            util.scroll_down_to_end_page(self.driver, delay)
            if util.is_exist_element(self.driver, self.locator.end_of_page):
                print("Đã tới cuối trang")
                break
            delay = delay * 1.5 if delay * 1.5 < limit_delay else limit_delay

    def get_urls(self, save_path=None):
        urls = []
        for ele in self.driver.find_elements(*self.locator.urls):
            urls.append(ele.get_attribute("href"))

        if save_path:
            with open(save_path, "w") as f:
                json.dump(urls, f)
            print("Save crawl urls successfully!")

        return urls
