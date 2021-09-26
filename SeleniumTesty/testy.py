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








    # def wylosuj_login(self, size):
    #     return "".join([random.choice(ascii_lowercase) for i in range(size)])
    #
    #
    # def przejdz_do_zakladania_konta(self):
    #     link = self.driver.find_element_by_css_selector("a[href=\"/signup\"]")
    #     link.click()
    #
    # def przejdz_do_logowania(self):
    #     link = self.driver.find_element_by_css_selector("a[href=\"/login\"]")
    #     link.click()
    #
    #
    #
    # def przejdz_do_losowego_filmu(self):
    #     link = self.driver.find_element_by_css_selector("a[href=\"/random\"]")
    #     link.click()
    #
    # def wyloguj(self):
    #     link = self.driver.find_element_by_css_selector("a[href=\"/logout\"]")
    #     link.click()
    #
    # def wprowadz_login(self, login):
    #     login_input = self.driver.find_element_by_name("login")
    #     login_input.send_keys(login)
    #
    # def test_poprawne_wejscie(self):
    #     footer = self.driver.find_element_by_id("footer")
    #     self.assertEqual(footer.text, "Author: P&M", msg="Niepoprawna stopka strony")
    #
    # def test_stworzenie_legit_konta(self):
    #     self.przejdz_do_zakladania_konta()
    #
    #     time.sleep(1)
    #     login = self.wylosuj_login(size=20)
    #     self.wprowadz_login(login)
    #
    #     email_input = self.driver.find_element_by_name("email")
    #     email_input.send_keys(login+"@mail.com")
    #
    #     password_input = self.driver.find_element_by_name("password1")
    #     password_input.send_keys("Przykladowe_246")
    #
    #     password2_input = self.driver.find_element_by_name("password2")
    #     password2_input.send_keys("Przykladowe_246")
    #
    #     button = self.driver.find_element_by_xpath("//*[@id=\"content\"]/form/button")
    #     button.click()
    #
    #     alert = self.driver.find_element_by_name("alert")
    #     self.assertEqual(alert.text, "Utworzono uzytkownika")
    #
    #
    # def test_stworzenia_konta_taki_sam_login(self):
    #     self.przejdz_do_zakladania_konta()
    #     self.wprowadz_login("Przykladowe")
    #
    #     email_input = self.driver.find_element_by_name("email")
    #     email_input.send_keys("przykladowe@mail.com")
    #
    #     password_input = self.driver.find_element_by_name("password1")
    #     password_input.send_keys("Przykladowe_246")
    #
    #     password2_input = self.driver.find_element_by_name("password2")
    #     password2_input.send_keys("Przykladowe_246")
    #
    #     button = self.driver.find_element_by_xpath("//*[@id=\"content\"]/form/button")
    #     button.click()
    #
    #     alert = self.driver.find_element_by_name("alert")
    #     self.assertEqual(alert.text, "Podany uzytkownik juz istnieje")
    #
    #
    # def test_poprawne_logowanie(self):
    #     self.przejdz_do_logowania()
    #     self.zaloguj_sie("Przykladowe", "Przykladowe_246")
    #
    #     alert = self.driver.find_element_by_name("alert")
    #     self.assertEqual(alert.text, "Zalogowano!")
    #
    # def test_niepoprawne_logowanie(self):
    #     self.przejdz_do_logowania()
    #     self.zaloguj_sie("testXD", "fdjdooekesjsd")
    #
    #     label = self.driver.find_element_by_name("alert")
    #     self.assertEqual(label.text, "Nie znaleziono uzytkownika!")
    #
    # def zaloguj_sie(self, login, haslo):
    #     login_input = self.driver.find_element_by_name("login")
    #     login_input.send_keys(login)
    #
    #     password_input = self.driver.find_element_by_name("password")
    #     password_input.send_keys(haslo)
    #
    #     button = self.driver.find_element_by_xpath("//*[@id=\"content\"]/div/form/button")
    #     button.click()
    #
    # def test_random_film(self):
    #     self.przejdz_do_logowania()
    #     self.zaloguj_sie("Przykladowe","Przykladowe_246")
    #
    #     for i in range(20):
    #         self.przejdz_do_losowego_filmu()
    #         serce = self.driver.find_element_by_id("heart")
    #         self.assertIsNotNone(serce)
    #
    # def test_logout(self):
    #     self.przejdz_do_logowania()
    #     self.zaloguj_sie("Przykladowe", "Przykladowe_246")
    #     self.wyloguj()
    #     label = self.driver.find_element_by_name("alert")
    #     self.assertEqual(label.text, "Wylogowano!")

