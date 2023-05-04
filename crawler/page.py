import json
import os
import time
import urllib.parse

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC

from . import settings, util
from .locator import LoginPageLocator, MainPageLocator, SearchPageLocator


class BasePage(object):
    def __init__(self, driver, logger=None):
        self.driver = driver
        if logger:
            self.logger = logger
        else:
            self.logger = util.get_logger(self.__class__.__name__, settings.LOG_FILENAME)

    def get_title(self):
        return self.driver.title

    def get_url(self):
        return self.driver.current_url

    def get(self, url):
        self.logger.info(f"Get url: {url}")
        self.driver.get(url)

    def find_element(self, locator):
        if isinstance(locator, tuple):
            locator = [locator]

        for l in locator:
            try:
                element = self.driver.find_element(*l)
                self.logger.info(f"Found element with locator: {l}")
                return element
            except NoSuchElementException as e:
                continue
        self.logger.info(f"Not found element with locator: {locator}")
        return None

    def find_elements(self, locator):
        elements = self.driver.find_elements(*locator)
        self.logger.info(f"Found {len(elements)} elements with locator: {locator}")
        return elements

    def hover(self, locator):
        element = self.find_element(*locator)
        hover = ActionChains(self.driver).move_to_element(element)
        hover.perform()


class LoginPage(BasePage):
    locator = LoginPageLocator()
    login_url = "https://www.facebook.com/"
    cookies_path = settings.COOKIES_PATH

    def login(self, usr=None, pwd=None, use_cookie=True):
        if usr is None and pwd is None and use_cookie is False:
            raise ValueError("Use username, password or cookies")

        self.get(self.login_url)
        if use_cookie:
            if os.path.exists(self.cookies_path):
                self.logger.info(f"Try to login by cookies")
                util.load_cookie(self.driver, self.cookies_path)
                self.driver.refresh()
            else:
                return False
        else:
            self.logger.info(f"Try to login by username={usr}, password={pwd}")
            self.find_element(self.locator.email_input).send_keys(usr)
            self.find_element(self.locator.pwd_input).send_keys(pwd)
            self.find_element(self.locator.login_button).click()

        if self.is_login_success():
            self.logger.info("Login successfully!")
            util.save_cookie(self.driver, self.cookies_path)
            return True

        self.logger.info("Login fail!")
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
        self.get(self._get_info_url_from_page_url(page_url))
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

        self.logger.info(f"Crawled data from {page_url}:\n{data}")
        return util.parse_information(data)


class SearchResultsPage(BasePage):
    locator = SearchPageLocator()
    search_api = "https://www.facebook.com/search/{search_type}?q={query}"

    def search(self, query, location, search_type="pages"):
        url = self.search_api.format(search_type=search_type, query=urllib.parse.quote_plus(query))
        self.get(url)
        time.sleep(5)
        self.find_element(self.locator.location_button).click()
        self.find_element(self.locator.location_input).send_keys(location)
        time.sleep(1)
        self.find_element(self.locator.first_location_button).click()

    def scroll(self, delay=1, limit_delay=5):
        while True:
            util.scroll_down_to_end_page(self.driver, delay)
            self.logger.info("Scroll")
            if util.is_exist_element(self.driver, self.locator.end_of_page):
                self.logger.info("Scroll to the end of page")
                print("Reached the bottom of the page")
                break
            delay = delay * 1.5 if delay * 1.5 < limit_delay else limit_delay

    def get_urls(self, save_path=None):
        urls = []
        for ele in self.find_elements(self.locator.urls):
            urls.append(ele.get_attribute("href"))

        if save_path:
            with open(save_path, "w") as f:
                json.dump(urls, f)
            print("Save crawl urls successfully!")

        return urls
