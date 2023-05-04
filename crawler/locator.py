from selenium.webdriver.common.by import By


class LoginPageLocator:
    email_input = (By.ID, "email")
    pwd_input = (By.ID, "pass")
    login_button = (By.NAME, "login")
    check_login = (By.CSS_SELECTOR, 'a[aria-label="Trang chủ"]')


class SearchPageLocator:
    location_button = (By.CSS_SELECTOR, "div.x1iyjqo2.xu06os2.x1ok221b.x1wo2wf3")
    location_input = (By.CSS_SELECTOR, 'input[aria-label="Vị trí"]')
    first_location_button = (By.CSS_SELECTOR, "ul.x78zum5.xdt5ytf.x1iyjqo2 > li")
    end_of_page = (By.XPATH, "//span[text()='Đã hết kết quả']")
    urls = (By.CSS_SELECTOR, 'div.x1yztbdb a[role="presentation"]')


class MainPageLocator:
    introduce_element = (By.XPATH, "//span[text()='Giới thiệu']")
    general_info = [
        (By.CSS_SELECTOR, "div.xyamay9.xqmdsaz.x1gan7if.x1swvt13"),
        (By.CSS_SELECTOR, "div.x1jx94hy.x78zum5.xdt5ytf.xw3vkyv"),
    ]
    name = [
        (By.CSS_SELECTOR, "div.x1e56ztr.x1xmf6yo > span > h1.x1heor9g.x1qlqyl8.x1pd3egz.x1a2a7pz"),
        (By.CSS_SELECTOR, "div.x1e56ztr.x1xmf6yo > h2 > span > span"),
    ]
    subscribe_count = (By.PARTIAL_LINK_TEXT, "người theo dõi")
    like_count = (By.PARTIAL_LINK_TEXT, "lượt thích")
