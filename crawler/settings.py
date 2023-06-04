import os
import tempfile

EXECUTABLE_PATH = "chromedriver.exe"
EMAIL = "nvdm.ufw@gmail.com"
PWD = "nvdm.ufw-1"


def mkdir(*args):
    path = os.path.join(*args)
    if not os.path.exists(path):
        os.mkdir(path)
    return path


HOME_DIR = mkdir(tempfile.gettempdir(), "fbcrawler")
DATA_DIR = mkdir(HOME_DIR, "data")

URLS_PATH = os.path.join(DATA_DIR, "urls.json")
COOKIES_PATH = os.path.join(DATA_DIR, "cookies.json")
OUTPUT_PATH = os.path.join(DATA_DIR, "data.csv")
OUTPUT_HEADER = [
    "url",
    "name",
    "subscribe_count",
    "like_count",
    "general_info",
    "phone_number",
]

LOG_DIR = mkdir(HOME_DIR, "log")
LOG_FILENAME = os.path.join(LOG_DIR, "crawler.log")
LOG_FORMAT = "%(levelname)s %(name)s %(asctime)s - %(message)s"
