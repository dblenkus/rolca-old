from unittest import skipIf
from selenium import webdriver

from django.test import LiveServerTestCase
from django.conf import settings

from login.models import Profile


class FrontendSeleniumTest(LiveServerTestCase):
    def setUp(self):
        Profile.objects.create_superuser(email='test@blenkus.com',
                                             password='test_pwd')

        self.client = webdriver.Chrome('/Applications/chromedriver')
        super(FrontendSeleniumTest, self).setUp()

    def tearDown(self):
        self.client.quit()
        super(FrontendSeleniumTest, self).tearDown()

    def open(self, url):
        self.client.get("%s%s" % (self.live_server_url, url))

    @skipIf(settings.TEST_SELENIUM is False, "Can't test in production.")
    def test_login(self):
        self.open('/')
        email_input = self.client.find_element_by_name("email")
        email_input.send_keys('test@blenkus.com')
        password_input = self.client.find_element_by_name("password")
        password_input.send_keys('test_pwd')
        self.client.find_element_by_xpath('//input[@value="Sign in"]').click()
