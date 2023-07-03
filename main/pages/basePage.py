import time

import self
from selenium import webdriver
from selenium.common import TimeoutException, StaleElementReferenceException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


class BasePage:
    """
  The Purpose Of A BasePage Is To Contain Methods Common To All Page Objects
  """

    def __init__(self, driver):
        self.driver = driver

    close_banner = (By.CSS_SELECTOR,
                    "button[class='onetrust-close-btn-handler onetrust-close-btn-ui banner-close-button ot-close-icon']")
    loader = (By.XPATH, "//main[contains(@class,'loader-background')]")

    def find_by(self, by, time_w=20):
        wait = WebDriverWait(self.driver, time_w)
        elem = wait.until(expected_conditions.visibility_of_element_located(by))
        return elem

    def find_presence(self, by, time_w=20):
        wait = WebDriverWait(self.driver, time_w)
        elem = wait.until(expected_conditions.presence_of_element_located(by))
        return elem

    def find_clickable(self, by, time_w=20):
        # return self.driver.find_element(*by)
        wait = WebDriverWait(self.driver, time_w)
        elem = wait.until(expected_conditions.element_to_be_clickable(by))
        return elem

    def find_elements(self, locator, time_w=20):
        wait = WebDriverWait(self.driver, time_w)
        elem = wait.until(expected_conditions.visibility_of_all_elements_located(locator))
        return elem

    # def loader_visibility(self, waiting=20):
    #     time.sleep(0.1)
    #     start_time = time.time()
    #     elems = self.driver.find_elements(*self.loader)
    #     # print("preloader ", self.driver.find_element(*self.loader).is_displayed())
    #     wait = WebDriverWait(self.driver, waiting)
    #     for el in elems:
    #         print("\npreloader ", el.is_displayed())
    #         wait.until(expected_conditions.invisibility_of_element(el),
    #                    f'preloader worked longer than expected {waiting} seconds')
    #         self.driver.find_elements(*self.loader)
    #     finish_time = time.time()
    #     print('\npreloader worked for: ', finish_time - start_time)

    def loader_visibility(self, waiting=20):
        time.sleep(0.1)
        start_time = time.time()
        while True:
            if (time.time() - start_time) > waiting:
                raise TimeoutException(f'preloader have been working longer than expected {waiting} seconds')
            time.sleep(0.05)
            try:
                if all(list(map(lambda x: not x.is_displayed(), self.driver.find_elements(*self.loader)))):
                    break
            except StaleElementReferenceException:
                continue
        finish_time = time.time()
        print('\npreloader worked for: ', finish_time - start_time)

    def get_current_url(self):
        return self.driver.current_url

    def scroll_to(self, web_elem):
        ActionChains(self.driver).scroll_to_element(web_elem).perform()

    def click_close_banner_btn(self):
        self.find_by(self.close_banner).click()
        time.sleep(0.2)
        return self
