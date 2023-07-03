import re

from selenium.webdriver.common.by import By

from main.pages.basePage import BasePage


def flights_info(fl_name, fl_plane, fl_date):
    inf = {'number_of_flights': len(fl_name)}
    for index, item in enumerate(fl_name):
        com_fl = item.text.strip().replace('\n', '').split("-")
        pl = fl_plane[index].text.strip()
        dt = fl_date[index].text.strip()
        inf[str(index + 1) + 'th_flight_company'] = com_fl[0].strip()
        inf[str(index + 1) + 'th_flight_num'] = com_fl[1].strip()
        inf[str(index + 1) + 'th_flight_plane'] = pl[pl.find(":") + 1:].strip()
        inf[str(index + 1) + 'th_flight_date'] = dt[dt.find(":") + 1:].strip()
    # print(inf)
    return inf


class PaymentPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    package = (By.XPATH, "//div[@class='payment-flight-booking-details']")
    pac_dates = (By.XPATH, ".//div[@class='payment-flight-booking-date']")
    paragraph = (By.XPATH, ".//p[@class='ng-binding']")
    hotel = (By.XPATH, "//div[@class='payment-round-trip'][1]")
    flight = (By.XPATH, "//div[@class='payment-round-trip'][2]")
    name = (By.XPATH, ".//h3[@class='ng-binding']")
    room_inf = (By.XPATH, ".//b[@class='ng-binding']")
    items = (By.XPATH, "./div/p[@class='ng-binding']")
    flight_passengers = (By.XPATH, "./p[@class='ng-binding']")
    depart_flight_num = (By.XPATH, "//h4[text()='Departure ']/following-sibling::p[1]")
    return_flight_num = (By.XPATH, "//h4[text()='Return ']/following-sibling::p[1]")
    depart_plane = (By.XPATH, "//h4[text()='Departure ']/following-sibling::p[contains(text(), 'Equipment:')]")
    return_plane = (By.XPATH, "//h4[text()='Return ']/following-sibling::p[contains(text(), 'Equipment:')]")
    depart_date = (By.XPATH, "//h4[text()='Departure ']/following-sibling::p[contains(text(), 'Departure Date:')]")
    return_date = (By.XPATH, "//h4[text()='Return ']/following-sibling::p[contains(text(), 'Departure Date:')]")

    def get_summary_info(self):
        pack = self.find_by(self.package)
        hotel_airports = pack.find_element(*self.paragraph).text.strip().split("\n")
        dates = pack.find_element(*self.pac_dates).text.strip().split("\n")
        summ = {'airport_code': hotel_airports[0][hotel_airports[0].find("(") + 1:hotel_airports[0].find(")")],
                'hotel_name': hotel_airports[1].upper(),
                'date_from': dates[0].replace(" ", ""),
                'date_to': dates[3].replace(" ", "")
                }
        return summ

    def get_hotel_info(self):
        pack = self.find_by(self.hotel)
        hotel_items = pack.find_elements(*self.items)
        items_text = list(map(lambda a: a.text.strip(), hotel_items))
        occupants = list(map(lambda a: int(re.sub(r"\D", "", a)), items_text[1].split(",")))
        summ = {'hotel_name': pack.find_element(*self.name).text.strip().upper(),
                'details': pack.find_element(*self.room_inf).text.strip().upper(),
                'adults': occupants[0],
                'children': occupants[1],
                'date_from': items_text[2][items_text[2].find(":") + 1: items_text[2].find(",")].replace(" ",
                                                                                                         "").upper(),
                'date_to': items_text[3][items_text[3].find(":") + 1: items_text[3].find(",")].replace(" ", "").upper(),
                }
        return summ

    def get_flight_info(self):
        pack = self.find_by(self.flight)
        code = pack.find_element(*self.name).text.strip().upper()
        passengers_list = pack.find_element(*self.flight_passengers).text.strip().split(",")
        passengers = list(map(lambda a: int(re.sub(r"\D", "", a)), passengers_list))
        summ = {'departure_code': code[code.find(":") + 1:code.find(" TO ")].replace(" ", ""),
                'adults': passengers[0],
                'children': passengers[1],
                "departure_flights_info": flights_info(pack.find_elements(*self.depart_flight_num),
                                                       pack.find_elements(*self.depart_plane),
                                                       pack.find_elements(*self.depart_date)),
                "return_flights_info": flights_info(pack.find_elements(*self.return_flight_num),
                                                    pack.find_elements(*self.return_plane),
                                                    pack.find_elements(*self.return_date)),
                }
        return summ
