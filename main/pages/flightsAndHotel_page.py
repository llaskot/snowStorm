from selenium.webdriver.common.by import By
from main.pages.basePage import BasePage


class FlightsAndHotelPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)

    def get_page_flight_and_hotels(self):
        self.driver.get("https://caesarsuat.mybookingplatform.com/Flight/Search?combined=3")

    def get_page_flight_and_hotels(self, url):
        self.driver.get(url)

    flying_from_input = (By.XPATH, "//input[@placeholder='Enter']")
    airports_drp_items = (By.XPATH, "//div[@class='field_dropdown place_list flight-suggestion-dropdown']/ul/li[1]")
    travelers_field = (By.XPATH, "//div[contains(@class,'room-occupant-box')]/div[1]")
    adults_number = (By.XPATH, "//div[text()='Adults']/..//span")
    children_number = (By.XPATH, "//div[text()='Children']/..//span")
    adults_pl = (By.XPATH, "//a[contains(@data-ng-click,'increaseRoomAdult')]")
    adults_min = (By.XPATH, "//a[contains(@data-ng-click,'decreaseRoomAdult')]")
    children_pl = (By.XPATH, "//a[contains(@data-ng-click,'increaseRoomChild')]")
    children_min = (By.XPATH, "//a[contains(@data-ng-click,'decreaseRoomChild')]")
    from_field = (By.XPATH, "//label[text()='From']/../div")
    datepicker_nextmoth = (By.XPATH, "//div[@class='datepicker-days']//th[@class='next']")
    datepicker_days = (By.XPATH, "//div[@class='datepicker-days']//tbody//td")
    search_btn = (By.CSS_SELECTOR, "div[class='flight-search-btn-holder']")
    continue_as_guest_btn = (By.XPATH, "//button[text()='Continue as guest']")
    sign_in_btn = (By.XPATH, "//button[text()='Sign in / Sign up for free']")
    month = (By.CSS_SELECTOR, "span[class='month focused active']")

    def input_flying_from(self, val):
        self.find_by(self.flying_from_input).send_keys(val)
        return FlightsAndHotelPage(self.driver)

    def click_1st_airports_drp_item(self):
        self.find_elements(self.airports_drp_items)[0].click()
        return FlightsAndHotelPage(self.driver)

    def click_travelers_field(self):
        self.find_by(self.travelers_field).click()
        return FlightsAndHotelPage(self.driver)

    def get_adults_number(self):
        return int(self.find_by(self.adults_number).text)

    def get_children_number(self):
        return int(self.find_by(self.children_number).text)

    def click_adult_plus(self):
        self.find_by(self.adults_pl).click()
        return FlightsAndHotelPage(self.driver)

    def click_adult_minus(self):
        self.find_by(self.adults_min).click()
        return FlightsAndHotelPage(self.driver)

    def click_children_plus(self):
        self.find_by(self.children_pl).click()
        return FlightsAndHotelPage(self.driver)

    def click_children_minus(self):
        self.find_by(self.children_min).click()
        return FlightsAndHotelPage(self.driver)

    def select_adults_number(self, number):
        while self.get_adults_number() > number:
            self.click_adult_minus()
        while self.get_adults_number() < number:
            self.click_adult_plus()
        return FlightsAndHotelPage(self.driver)

    def select_children_number(self, number):
        while self.get_children_number() > number:
            self.click_children_minus()
        while self.get_children_number() < number:
            self.click_children_plus()
        return FlightsAndHotelPage(self.driver)

    def click_from_field(self):
        self.find_by(self.from_field).click()
        return FlightsAndHotelPage(self.driver)

    def click_datepicker_next_month(self):
        self.find_by(self.datepicker_nextmoth).click()
        return FlightsAndHotelPage(self.driver)

    def click_datepicker_day(self, day):
        dates = self.find_elements(self.datepicker_days)
        for i in dates:
            if int(i.text) == day:
                i.click()
                break
        return FlightsAndHotelPage(self.driver)

    def select_date(self, day):
        self.click_datepicker_next_month() \
            .click_datepicker_next_month() \
            .click_datepicker_next_month() \
            .click_datepicker_next_month() \
            .click_datepicker_day(day)
        return FlightsAndHotelPage(self.driver)

    def click_search_btn(self):
        self.find_clickable(self.search_btn).click()
        return FlightsAndHotelPage(self.driver)

    def click_continue_as_guest_btn(self):
        self.find_clickable(self.continue_as_guest_btn).click()
        self.loader_visibility(45)

    def click_continue_as_guest_btn_no_wait(self):
        self.find_by(self.continue_as_guest_btn, 60).click()

    def click_sign_in_btn(self):
        self.find_clickable(self.sign_in_btn).click()

    def get_1_airport_code(self):
        text = self.find_elements(self.airports_drp_items)[0].text
        return text[text.rfind(' ') + 1:len(text)].upper()

    def get_selected_month(self):
        return self.driver.execute_script("return arguments[0].textContent;", self.find_presence(self.month)).upper() \
            .replace(' ', '')
