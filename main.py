import argparse
import csv
import json
import os
from concurrent.futures import ThreadPoolExecutor, wait

from tqdm import tqdm

from crawler import page, settings, util

parser = argparse.ArgumentParser(description="Simple facebook crawler tool")
parser.add_argument("--headless", dest="headless", action="store_true")
parser.add_argument("--no-headless", dest="headless", action="store_false")
parser.set_defaults(headless=True)
args = parser.parse_args()


TITLE1 = "\n=============== {} ==============="
TITLE2 = "\n--------------- {} ---------------"
DONE_MESSAGE = "[DONE]"


def login_facebook(driver, usr=None, pwd=None):
    page_obj = page.LoginPage(driver)
    if os.path.exists(settings.COOKIES_PATH):
        success = page_obj.login(use_cookie=True)
        if success:
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
    page_obj = page.SearchResultsPage(driver)

    print(TITLE2.format("Searching"))
    page_obj.search(query, location, search_type=search_type)
    print(DONE_MESSAGE)

    print(TITLE2.format("Auto scroll to the end of page"))
    page_obj.scroll(scroll_delay, limit_scroll_delay)
    print(DONE_MESSAGE)

    print(TITLE2.format(f"Extract urls from page"))
    urls = page_obj.get_urls(save_path=settings.URLS_PATH)
    print(DONE_MESSAGE)

    print(f"Get {len(urls)} pages for query='{query}' and location='{location}'")
    print(DONE_MESSAGE)


def crawl_page_information(urls, output_path, delay=4, usr=None, pwd=None):
    driver = util.create_chrome_driver(headless=args.headless)
    if not login_facebook(driver, usr, pwd):
        driver.quit()
        return

    page_obj = page.InformationPage(driver)
    with open(output_path, "a+") as f:
        writer = csv.writer(f)
        for i in tqdm(range(len(urls)), desc="processing...."):
            writer.writerow(page_obj.get_information(urls[i], delay=delay))
            if i % 10:
                f.flush()

    driver.quit()


def create_output_file(output_path):
    with open(output_path, "w") as f:
        writer = csv.writer(f)
        writer.writerow(settings.OUTPUT_HEADER)


def crawl_page_information_multiprocess(n_threads, output_path, delay=4, usr=None, pwd=None):
    create_output_file(output_path)
    process_list = []
    with ThreadPoolExecutor(max_workers=n_threads) as executor:
        with open(settings.URLS_PATH, "r") as f:
            urls = json.load(f)

        n = len(urls) // n_threads
        chunks = [urls[i : i + n] for i in range(0, len(urls), n)]
        for chunk in chunks:
            process_list.append(
                executor.submit(crawl_page_information, chunk, output_path, delay, usr, pwd)
            )
    wait(process_list)


if __name__ == "__main__":
    driver = util.create_chrome_driver(headless=args.headless)

    # login facebook
    print(TITLE1.format("Facebook login"))

    success = login_facebook(driver)
    email = pwd = None
    if success:
        print("Login success!")
        print(DONE_MESSAGE)
    else:
        while True:
            print(TITLE2.format("Nhập email đăng nhập và password"))
            email = input("Input your email: ")
            pwd = input("Input your password: ")
            success = login_facebook(driver, email, pwd)
            if success:
                print("Login success!")
                print(DONE_MESSAGE)
                break
            request = input("Login fail :((, bấm q để thoát!: ")
            if request == "q":
                break

    # Crawl data
    print(TITLE1.format("Crawling data"))

    print(TITLE2.format("Input query"))
    query = input("Input search text: ")
    location = input("Input search location: ")

    print(TITLE2.format("Input config:"))
    download_delay = float(input("Input download delay: "))
    n_threads = int(input("Input Number of threads: "))
    output_path = input("Input output file path: ")

    # Search and crawl urls
    search_and_crawl_page_urls(driver, query, location)
    driver.quit()

    # Crawl information
    print(TITLE2.format("Start Crawling page information from urls"))
    crawl_page_information_multiprocess(
        n_threads, output_path, delay=download_delay, usr=email, pwd=pwd
    )
    print(DONE_MESSAGE)
