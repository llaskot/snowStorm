import re
import time

from selenium.webdriver.common.by import By
from main.pages.basePage import BasePage


class FlightSelectPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)
        self.depart_info = None
        self.return_info = None

    origin_field = (By.CSS_SELECTOR, "div[class='origin-block']>h3")
    from_field = (By.CSS_SELECTOR, "div[class='date-from-block']>h3")
    to_field = (By.CSS_SELECTOR, "div[class='date-to-block']>h3")
    adults_field = (By.XPATH, "//h5[text()='Adults']/../h3")
    children_field = (By.CSS_SELECTOR, "div[class='child-block']>h3")
    all_flight_result_containers = (By.XPATH, "//ul[@class='flightResultContainer']//div[@class='container-fluid']")
    departures = (By.XPATH, ".//div[@id='outbound']/div/div")
    returns = (By.XPATH, ".//div[@id='return']/div/div")
    flight_number_field = (By.XPATH, ".//div[@class='flight-airlines caesarSearchPackageDivoverflowHid']"
                                     "/p[@class='ng-binding']")
    flight_company_field = (By.XPATH, ".//div[@class='flight-airlines caesarSearchPackageDivoverflowHid']/h5")
    flight_plane_field = (By.XPATH, ".//div[@class='flight-airlines caesarSearchPackageDivoverflowHid']"
                                    "/p[@class='equipment ng-binding ng-scope']")
    flight_date_field = (By.XPATH, ".//div[@class='flight-airlines caesarSearchPackageDivoverflowHid']/p["
                                   "@class='equipment main-departure-date ng-binding ng-scope']")
    person_prise_field = (By.XPATH, ".//span[@class='priceFROM']/../sapn")
    total_prise_field = (By.XPATH, ".//div[@class='small-txt-price ng-binding']")
    select_flight_btn = (By.XPATH, ".//button[text()='Select Flight']")
    page_bottom = (By.CSS_SELECTOR, "div[class='why-book-wrapper']")

    def get_origin(self):
        return self.find_by(self.origin_field).text.upper()

    def get_from(self):
        return self.find_by(self.from_field).text.upper().replace(' ', '')

    def get_to(self):
        return self.find_by(self.to_field).text.upper().replace(' ', '')

    def get_adults(self):
        return self.find_by(self.adults_field).text.upper().replace(' ', '')

    def get_children(self):
        return self.find_by(self.children_field).text.upper().replace(' ', '')

    def all_flight_containers(self):
        return self.find_elements(self.all_flight_result_containers)

    def all_departures_in_container(self, cont_number):
        container = self.all_flight_containers()[cont_number - 1]
        return container.find_elements(*self.departures)

    def all_returns_in_container(self, cont_number):
        container = self.all_flight_containers()[cont_number - 1]
        return container.find_elements(*self.returns)

    def get_departure_info(self, cont_number):
        departures = self.all_departures_in_container(cont_number)
        info = {'number_of_flights': len(departures)}
        for index, item in enumerate(departures):
            info[str(index + 1) + 'th_flight_company'] = item.find_element(*self.flight_company_field).text
            info[str(index + 1) + 'th_flight_num'] = item.find_element(*self.flight_number_field).text
            info[str(index + 1) + 'th_flight_plane'] = item.find_element(*self.flight_plane_field).text
            info[str(index + 1) + 'th_flight_date'] = item.find_element(*self.flight_date_field).text.strip()
        return info

    def get_return_info(self, cont_number):
        returns = self.all_returns_in_container(cont_number)
        info = {'number_of_flights': len(returns)}
        for index, item in enumerate(returns):
            info[str(index + 1) + 'th_flight_company'] = item.find_element(*self.flight_company_field).text
            info[str(index + 1) + 'th_flight_num'] = item.find_element(*self.flight_number_field).text
            info[str(index + 1) + 'th_flight_plane'] = item.find_element(*self.flight_plane_field).text
            info[str(index + 1) + 'th_flight_date'] = item.find_element(*self.flight_date_field).text.strip()
        return info

    def get_prices_info(self, cont_number):
        price = self.all_flight_containers()[cont_number - 1]
        info = {'per_person': int(re.sub(r"\D", "", price.find_element(*self.person_prise_field).text)),
                'total': int(re.sub(r"\D", "", price.find_element(*self.total_prise_field).text))}
        return info

    def click_select_flight_btn(self, cont_number):
        web_el = self.all_flight_containers()[cont_number - 1].find_element(*self.select_flight_btn)
        self.scroll_to(web_el)
        time.sleep(0.4)
        web_el.click()
        self.loader_visibility(45)

    def click_select_flight_btn(self, company_name):
        visible_flights = self.all_flight_containers()
        web_el = visible_flights[0]
        for flight in visible_flights:
            companies = []
            for comp in flight.find_elements(*self.flight_company_field):
                companies.append(comp.text.strip())
            if companies.count(company_name) == len(companies):
                web_el = flight
                break
        self.scroll_to(web_el.find_element(*self.select_flight_btn))
        self.depart_info = self.get_departure_info(visible_flights.index(web_el)+1)
        self.return_info = self.get_return_info(visible_flights.index(web_el)+1)
        time.sleep(0.4)
        web_el.find_element(*self.select_flight_btn).click()

    def scroll_flights(self):
        flights = 0
        visible_flights = self.all_flight_containers()
        if len(visible_flights) == 0:
            print("!!!!!!!!!! NO FLIGHTS THESE DAYS   !!!!!!!!!!!!!!!!!!")
        elif len(visible_flights) == 50:
            while len(visible_flights) > flights:
                # print("\nflights = ", flights)
                # print("real flights = ", len(visible_flights))
                flights = len(visible_flights)
                self.scroll_to(visible_flights[len(visible_flights)-5])
                time.sleep(0.7)
                self.scroll_to(visible_flights[len(visible_flights)-3])
                time.sleep(0.7)
                self.scroll_to(self.find_by(self.page_bottom))
                time.sleep(2.5)
                visible_flights = self.all_flight_containers()
                # print("\nnew flights = ", flights)
                # print("new real flights = ", len(visible_flights))
        return self
