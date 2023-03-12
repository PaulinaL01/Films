import random
import unittest
from selenium import webdriver
from pages.website import HomePage, LoginPage, SignUpPage
from selenium.webdriver.chrome.options import Options
import time
from string import ascii_lowercase
from random import choice


class StrUtils:
    @staticmethod
    def generate_random_name(count):
        return "".join([random.choice(ascii_lowercase) for i in range(9)])

    @staticmethod
    def generate_random_email(name_count):
        domains = ["gmail.com", "vp.pl", "poczta.onet.pl", "protonmain.com", "poczta.interia.pl"]
        return StrUtils.generate_random_name(name_count) + "@" + choice(domains)


class Test_Portalu(unittest.TestCase):
    def setUp(self): #ta metoda wykonuje sie przed kazdym testem
        # options = Options()
        # options.headless = True
        self.driver = webdriver.Chrome("C:\\Users\\lesni\\OneDrive\\Pulpit\\chromedriver.exe")
        self.driver.get("http://127.0.0.1:5000/")

    def tearDown(self): #metoda ktora wykonuje sie po kazdym tescie
        self.driver.close()

    def test_correct_signup(self):
        alerts = HomePage(self.driver) \
            .go_to_signup()\
            .enter_login(StrUtils.generate_random_name(9))\
            .enter_email(StrUtils.generate_random_email(9))\
            .enter_password1("Przykladowe123") \
            .enter_password2("Przykladowe123") \
            .signup() \
            .get_alerts()
        self.assertIn("Utworzono uzytkownika", alerts)

    def test_unique_email(self):
        for a in range(1):
            alerts = HomePage(self.driver)\
                .go_to_signup()\
                .enter_login(StrUtils.generate_random_name(9))\
                .enter_email("przykladowe@mail.com")\
                .enter_password1("Przykladowe123")\
                .enter_password2("Przykladowe123")\
                .signup()\
                .get_alerts()
        self.assertEqual(alerts, ["Użytkownik o podanym adresie email już istnieje!"])
    #     dziala

    def test_incorrect_signup_password_not_equal(self):
        alerts = HomePage(self.driver)\
            .go_to_signup()\
            .enter_login(StrUtils.generate_random_name(9))\
            .enter_email(StrUtils.generate_random_email(9))\
            .enter_password1("Przykladowe123")\
            .enter_password2("Przykladowe1234")\
            .signup()\
            .get_alerts()
        self.assertIn("Passwords must match", alerts)
    #     dziala

    def test_incorrect_signup_password_short(self):
        alerts = HomePage(self.driver)\
            .go_to_signup()\
            .enter_login(StrUtils.generate_random_name(9))\
            .enter_email(StrUtils.generate_random_email(9))\
            .enter_password1("Przyk1")\
            .enter_password2("Przyk1")\
            .signup()\
            .get_alerts()
        self.assertEqual(alerts, ["Field must be between 8 and 30 characters long."])
    #    dziala

    def test_incorrect_signup_password_no_number(self):
        alerts = HomePage(self.driver) \
            .go_to_signup() \
            .enter_login(StrUtils.generate_random_name(9))\
            .enter_email(StrUtils.generate_random_email(9))\
            .enter_password1("Przykladowe") \
            .enter_password2("Przykladowe") \
            .signup() \
            .get_alerts()
        self.assertEqual(alerts, ["Hasło powinno mieć przynajmniej jedną cyfrę"])
    #     dziala

    def test_correct_login(self):
        alert = HomePage(self.driver)\
            .go_to_login()\
            .enter_login("paulina")\
            .enter_password1("Paulina123")\
            .login()\
            .get_alert()
        self.assertEqual(alert, "Zalogowano!")

