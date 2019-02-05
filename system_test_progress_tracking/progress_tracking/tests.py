from django.test import TestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import urljoin
from time import sleep


HOME_PAGE = "http://localhost:8000"


class BasePage(object):
    url = None

    def __init__(self, driver):
        self.driver = driver

    def fill_form(self, elem, value):
        elem.send_keys(value)

    def fill_form_by_id(self, form_element_id, value):
        elem = self.driver.find_element_by_id(form_element_id)
        return self.fill_form(elem, value)

    def navigate(self):
        self.driver.get(self.url)


class Homepage(BasePage):
    url = HOME_PAGE

    def getLoginform(self):
        return LogInPage(self.driver)


class LogInPage(BasePage):
    url = urljoin(HOME_PAGE, "login")

    def setUsername(self, username):
        self.fill_form_by_id("id_username", username)

    def setPassword(self, password):
        self.fill_form_by_id("id_password", password)

    def submit(self):
        self.driver.find_element_by_css_selector(".btn[type='submit']").click()


class LogInTest(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--incognito")
        cls.browser = webdriver.Chrome(chrome_options=chrome_options, executable_path=ChromeDriverManager().install())

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super().tearDownClass()

    def test_someone_can_login(self):
        homepage = Homepage(self.browser)
        homepage.navigate()
        signup_form = homepage.getLoginform()
        signup_form.navigate()
        signup_form.setUsername("Justin")
        signup_form.setPassword("asdf")
        signup_form.submit()
        elem = self.browser.find_element_by_css_selector('.alert')
        self.assertIsNotNone(elem)
