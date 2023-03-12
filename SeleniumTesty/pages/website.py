import random
from string import ascii_lowercase

class SignUpPage:
    def __init__(self, driver):
        self.driver = driver
        self.login_input = self.driver.find_element_by_name("login")
        self.email_input = self.driver.find_element_by_name("email")
        self.password1_input = self.driver.find_element_by_name("password1")
        self.password2_input = self.driver.find_element_by_name("password2")
        self.button = self.driver.find_element_by_xpath("//*[@id=\"content\"]/form/button")

    def enter_login(self, login):
        self.login_input.send_keys(login)
        return self

    def enter_email(self, email):
        self.email_input.send_keys(email)
        return self

    def enter_password1(self, password1):
        self.password1_input.send_keys(password1)
        return self

    def enter_password2(self, password2):
        self.password2_input.send_keys(password2)
        return self

    def signup(self):
        self.button.click()
        if "Zalogowano!" in self.get_alerts():
            return HomePage(self.driver)
        else:
            return self

    def get_alerts(self):
        alerts = self.driver.find_elements_by_name("alert")
        return [alert.text for alert in alerts]


class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.login_input = self.driver.find_element_by_name("login")
        self.password1_input = self.driver.find_element_by_name("password")
        self.button = self.driver.find_element_by_xpath("//*[@id=\"content\"]/div/form/button")


    def enter_login(self, login):
        self.login_input.send_keys(login)
        return self

    def enter_password1(self, password1):
        self.password1_input.send_keys(password1)
        return self

    def login(self):
        self.button.click()
        if "Zalogowano!" in self.get_alert():
            return HomePage(self.driver)
        else:
            return self

    def get_alert(self):
        alert = self.driver.find_element_by_name("alert")
        return alert.text


class HomePage:
    def __init__(self, driver):
        self.driver = driver

    def get_alert(self):
        label = self.driver.find_element_by_name("alert")
        return label.text

    def go_to_signup(self):
        home_link = self.driver.find_element_by_css_selector("a[href=\"/signup\"]")
        home_link.click()
        return SignUpPage(self.driver)

    def go_to_login(self):
        login_link = self.driver.find_element_by_css_selector("a[href=\"/login\"]")
        login_link.click()
        return LoginPage(self.driver)
    def go_to_comment(self):
        comment_link = self.driver.find_element_by_xpath('//*[@id="content"]/div/div[1]/div[1]/div/div/a/button')
        comment_link.click()
        return Comment(self.driver)


class RandomPage:
    def __init__(self, driver):
        self.driver = driver
        self.heart = self.driver.find_element_by_id("heart")

    def find_heart(self, heart):
        self.assertIsNotNone(heart)
        return self


class Comment:
    def __init__(self, driver):
        self.driver = driver
        self.comment_input = self.driver.find_element_by_name("comment")
        self.button = self.driver.find_element_by_xpath('//*[@id="content"]/form/button')
