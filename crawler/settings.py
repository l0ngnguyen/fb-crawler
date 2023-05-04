from os.path import dirname, join, realpath

EXECUTABLE_PATH = "chromedriver"
EMAIL = "nvdm.ufw@gmail.com"
PWD = "nvdm.ufw-1"

HOME_PATH = dirname(dirname(realpath(__file__)))
DATA_PATH = join(HOME_PATH, "crawler/data")

URLS_PATH = join(DATA_PATH, "urls.json")
COOKIES_PATH = join(DATA_PATH, "cookies.json")
OUTPUT_PATH = join(DATA_PATH, "data.csv")
OUTPUT_HEADER = [
    "url",
    "name",
    "subscribe_count",
    "like_count",
    "general_info",
    "phone_number",
]

LOG_DIR = join(HOME_PATH, "crawler/log")
LOG_FILENAME = join(LOG_DIR, "crawler.log")
LOG_FORMAT = "%(levelname)s %(name)s %(asctime)s - %(message)s"
