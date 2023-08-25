import time

from selenium.webdriver.common.by import By

from main.pages.basePage import BasePage


class PackageDetailsPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    departure_1th_flight = (By.XPATH, "//div[@class='col-sm-5'][1]//p[1]")
    return_1st_flight = (By.XPATH, "//div[@class='col-sm-5'][2]//p[1]")

    def get_departure_1th_flight(self):
        return self.find_by(self.departure_1th_flight).text

    def get_return_1th_flight(self):
        return self.find_by(self.return_1st_flight).text
