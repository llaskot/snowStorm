from selenium.webdriver.common.by import By
from main.pages.basePage import BasePage


class SignInPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)

    login_field = (By.NAME, "userID")
    password_field = (By.NAME, "userPassword")
    sign_in_btn = (By.XPATH, "//button[text()='SIGN IN']")

    def input_login(self, login):
        self.find_clickable(self.login_field).send_keys(login)
        return self

    def input_password(self, pas):
        self.find_clickable(self.password_field).send_keys(pas)
        return self

    def click_sign_in(self):
        self.find_clickable(self.sign_in_btn).click()
