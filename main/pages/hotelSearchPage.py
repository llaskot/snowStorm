import re
import time

from selenium.webdriver.common.by import By

from main.pages.basePage import BasePage


class HotelSearchPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)

    date_from = (By.XPATH, "//h3[@class='date-to book-date']/span[1]")
    date_to = (By.XPATH, "//h3[@class='date-to book-date']/span[2]")
    adults_field = (By.XPATH, "//p[text()='Adults']/../span")
    children_field = (By.XPATH, "//p[text()='Children']/../span")
    all_hotels_containers = (By.XPATH, "//ul[@class='hotelListSet']/li//div[@class='pad row']")
    hotel_name = (By.XPATH, ".//div[@class='details hotel-details']/h5/a")
    person_prise_field = (By.XPATH, ".//span[@class='priceFROM']/..")
    total_prise_field = (By.XPATH, ".//div[@class='small-txt-price ng-binding']")
    select_room_btn = (By.CSS_SELECTOR, "div[class='selectbtn']>a")

    def get_from_date(self):
        text = self.find_by(self.date_from).text.strip().split("\n")
        return text[2] + text[1]

    def get_to_date(self):
        text = self.find_by(self.date_to).text.strip().split("\n")
        return text[2] + text[1]

    def get_adults_num(self):
        return int(self.find_by(self.adults_field).text)

    def get_children_num(self):
        return int(self.find_by(self.children_field).text)

    def get_hotel_info(self, hotel_container):
        hotels = self.find_elements(self.all_hotels_containers)
        text = hotels[hotel_container - 1].find_element(*self.person_prise_field).text.strip().split("\n")
        info = {'hotel_name': hotels[hotel_container - 1].find_element(*self.hotel_name).text.strip(),
                'per_person': int(re.sub(r"\D", "", text[0])),
                'total': int(re.sub(r"\D", "", text[2]))}
        return info

    def click_select_room_btn(self, hotel_container):
        web_el = self.find_elements(self.all_hotels_containers)[hotel_container - 1].find_element(*self.select_room_btn)
        self.scroll_to(web_el)
        time.sleep(2)
        web_el.click()
        self.loader_visibility(45)

    def click_select_room_btn(self, hotel_name):
        web_els = self.find_elements(self.all_hotels_containers)
        btn = None
        for el in web_els:
            if el.find_element(*self.hotel_name).text.strip() in hotel_name \
                    and el.find_element(*self.select_room_btn).text.strip() == 'SELECT A ROOM':
                btn = el.find_element(*self.select_room_btn)
                break
        if btn is None:
            for el in web_els:
                if el.find_element(*self.select_room_btn).text.strip() == 'SELECT A ROOM':
                    btn = el.find_element(*self.select_room_btn)
                    break
        self.scroll_to(btn)
        time.sleep(1)
        btn.click()







