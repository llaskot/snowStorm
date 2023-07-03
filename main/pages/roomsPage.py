import re
import time

from selenium.webdriver.common.by import By

from main.pages.basePage import BasePage


class RoomPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    all_rooms_container = (By.XPATH, "//ul/li//div[@class='pkgRow']")
    payment_info = (By.XPATH, ".//div[@class='text-center price']/div[@class='p2']")
    details = (By.XPATH, ".//div[contains(@class, 'hotel_details_block_new')]/h4")
    proceed_to_checkout_btn = (
        By.XPATH, ".//div[@class='row detailsPagePriceBlock']//button[text()='PROCEED TO CHECKOUT']")

    def get_room_info(self, room_container):
        room = self.find_elements(self.all_rooms_container)[room_container - 1]
        price = room.find_element(*self.payment_info).text.strip().split("\n")
        info = {'details': room.find_element(*self.details).text.strip(),
                'per_person': int(re.sub(r"\D", "", price[0])),
                'total': int(re.sub(r"\D", "", price[2]))
                }
        return info

    def click_proceed_to_checkout_btn(self, room_container):
        web_el = self.find_elements(self.all_rooms_container)[room_container - 1] \
            .find_element(*self.proceed_to_checkout_btn)
        self.scroll_to(web_el)
        time.sleep(1)
        web_el.click()
        self.loader_visibility(45)
