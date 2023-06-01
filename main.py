import csv
import json
import multiprocessing
import os
import time

from tqdm import tqdm

from crawler import page, settings, util


def get_title(s, char, len_title=50):
    len_char = len_title - len(s) - 2
    if len_char < 2:
        return s
    elif len_char % 2 == 0:
        head = tail = char * (len_char // 2)
    else:
        head = char * (len_char // 2)
        tail = head + char
    return head + " " + s + " " + tail


OK = "[DONE]"
def print_title1(s):
    print(get_title(s.upper(), char="#", len_title=60))
def print_title2(s):
    print(get_title(s, char="=", len_title=60))


def login_facebook(driver, logobj=None, usr=None, pwd=None):
    page_obj = page.LoginPage(driver, logobj)
    if os.path.exists(settings.COOKIES_PATH):
        if page_obj.login(use_cookie=True):
            return True

    if usr is None and pwd is None:
        return False

    return page_obj.login(usr=usr, pwd=pwd, use_cookie=False)


def search_and_crawl_page_urls(
    driver,
    query,
    location,
    search_type="pages",
    scroll_delay=1,
    limit_scroll_delay=5,
):
    page_obj = page.SearchPage(driver)

    print_title2("Searching")
    page_obj.search(query, location, search_type=search_type)
    print(OK)

    print_title2("Auto scroll to the end of page")
    page_obj.scroll(scroll_delay, limit_scroll_delay)
    print(OK)

    print_title2("Extract urls from page")
    urls = page_obj.get_urls(save_path=settings.URLS_PATH)
    print(OK)

    print(f"Get {len(urls)} pages for query='{query}' and location='{location}'")
    print(OK)


def create_output_file(output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(settings.OUTPUT_HEADER)


def crawl_page_information(urls, output_path, logobj, delay=4, usr=None, pwd=None, headless=False):
    driver = util.create_chrome_driver(headless=headless)
    if not login_facebook(driver, logobj, usr, pwd):
        driver.quit()
        return

    page_obj = page.InformationPage(driver, logobj)
    with open(output_path, "a+", encoding="utf-8") as f:
        writer = csv.writer(f)
        for i in tqdm(range(len(urls)), desc="processing...."):
            writer.writerow(page_obj.get_information(urls[i], delay=delay))
            if i % 10:
                f.flush()

    driver.quit()


def crawl_page_information_multiprocess(
    n_threads,
    output_path,
    delay=4,
    usr=None,
    pwd=None,
    headless=False
):
    create_output_file(output_path)
    with open(settings.URLS_PATH, "r", encoding="utf-8") as f:
        urls = json.load(f)

    n = len(urls) // n_threads
    chunks = [urls[i: i + n] for i in range(0, len(urls), n)]
    process_list = []
    for i, chunk in enumerate(chunks):
        logobj = util.get_logger(f"thread_{i+1}", settings.LOG_FILENAME)
        process = multiprocessing.Process(
            target=crawl_page_information,
            args=(chunk, output_path, logobj, delay, usr, pwd, headless,),
        )
        process.start()
        process_list.append(process)
        time.sleep(2)

    for p in process_list:
        p.join()


if __name__ == "__main__":
    headless = bool(input("Show browser (input 0 or 1): "))
    driver = util.create_chrome_driver(headless=headless)

    # login facebook
    print_title1("Facebook login")

    usr = pwd = None
    if login_facebook(driver):
        print("Login success!")
        print(OK)
    else:
        while True:
            print_title2("Input facebook username and password")
            usr = input("Input your username: ")
            pwd = input("Input your password: ")
            print_title2("Start logging in facebook")
            if login_facebook(driver, logobj=None, usr=usr, pwd=pwd):
                print("Login success!")
                print(OK)
                break
            request = input("Login fail :((, press q to escape!: ")
            if request == "q":
                break

    # Crawl data
    print_title1("Crawling data")

    print_title2("Input query")
    query = input("Input search text: ")
    location = input("Input search location: ")

    print_title2("Input config")
    download_delay = float(input("Input download delay: "))
    n_threads = int(input("Input Number of threads: "))
    output_path = input("Input output file path: ")

    # Search and crawl urls
    search_and_crawl_page_urls(driver, query, location)
    driver.quit()

    # Crawl information
    print_title2("Start Crawling page info")
    crawl_page_information_multiprocess(
        n_threads,
        output_path,
        delay=download_delay,
        usr=usr,
        pwd=pwd,
        headless=headless
    )
    print(OK)
