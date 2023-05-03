import os

EXECUTABLE_PATH = "chromedriver"
EMAIL = "nvdm.ufw@gmail.com"
PWD = "nvdm.ufw-1"

DATA_PATH = "crawler/data"
URLS_PATH = os.path.join(DATA_PATH, "urls.json")
COOKIES_PATH = os.path.join(DATA_PATH, "cookies.json")
OUTPUT_PATH = os.path.join(DATA_PATH, "data.csv")
OUTPUT_HEADER = ["url", "name", "subscribe_count", "like_count", "general_info", "phone_number"]
