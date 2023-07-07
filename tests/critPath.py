import json
import time
import pytest_check as check

from main.pages.flightSelectPage import FlightSelectPage
from main.pages.flightsAndHotel_page import FlightsAndHotelPage
from main.pages.hotelSearchPage import HotelSearchPage
from main.pages.paymentPage import PaymentPage
from main.pages.roomsPage import RoomPage
from tests.baseTest import BaseTest


class Values:
    def __init__(self):
        self.flying_from = 'VANCOUVER'
        self.adults = 1
        self.children = 0
        self.from_date = 15
        self.to_date = 19
        self.flight_container_num = 7
        self.hotel_container_num = 6
        self.room_container_num = 5


class SavedValues:
    def __init__(self):
        self.flights_url = 'https://caesarsuat.mybookingplatform.com/us/Flight/Search/Results/'
        self.hotels_url = 'https://caesarsuat.mybookingplatform.com/us/Hotel/Search/Result/'
        self.rooms_url = 'https://caesarsuat.mybookingplatform.com/us/Hotel/Search/Details/'
        self.payment_url = 'https://caesarsuat.mybookingplatform.com/us/Flight-Hotel-Car/Cart/Purchase/Combined'

    flying_from_code = 0
    month = 0
    departure_flights_info = {}
    return_flights_info = {}
    flight_price = {}
    hotel_info = {}
    room_info = {}


class TestCriticalPath(BaseTest):

    def test_check_flights_values(self):
        fh_page = FlightsAndHotelPage(self.driver)
        flights_page = FlightSelectPage(self.driver)
        hotel_search_page = HotelSearchPage(self.driver)
        room_page = RoomPage(self.driver)
        payment_page = PaymentPage(self.driver)
        val = Values()
        saved = SavedValues()
        fh_page.get_page_flight_and_hotels()
        fh_page.input_flying_from(val.flying_from)
        saved.flying_from_code = fh_page.get_1_airport_code()
        fh_page.click_1st_airports_drp_item() \
            .click_travelers_field() \
            .select_adults_number(val.adults) \
            .select_children_number(val.children) \
            .click_from_field() \
            .select_date(val.from_date)
        saved.month = fh_page.get_selected_month()
        fh_page.click_datepicker_day(val.to_date) \
            .click_search_btn() \
            .click_continue_as_guest_btn()
        check.is_in(saved.flights_url, flights_page.get_current_url(), "wrong URL")
        check.is_in(saved.flying_from_code, flights_page.get_origin(),
                    "Origin field doesn't contain airport code: " + saved.flying_from_code)
        check.equal(flights_page.get_from(), saved.month + str(val.from_date), "Wrong from date")
        check.equal(flights_page.get_to(), saved.month + str(val.to_date), "Wrong to date")
        check.equal(flights_page.get_adults(), str(val.adults), "Wrong adults number")
        check.equal(flights_page.get_children(), str(val.children), "Wrong children number")
        saved.departure_flights_info = flights_page.get_departure_info(val.flight_container_num)
        saved.return_flights_info = flights_page.get_return_info(val.flight_container_num)
        saved.flight_price = flights_page.get_prices_info(val.flight_container_num)
        flights_page.click_close_banner_btn() \
            .click_select_flight_btn(val.flight_container_num)
        hotel_search_page.click_close_banner_btn()
        check.is_in(saved.hotels_url, hotel_search_page.get_current_url(), "wrong URL")
        check.equal(hotel_search_page.get_from_date(), saved.month + str(val.from_date), "Wrong from date")
        check.equal(hotel_search_page.get_adults_num(), val.adults, "Wrong adults number")
        check.equal(hotel_search_page.get_children_num(), val.children, "Wrong children number")
        saved.hotel_info = hotel_search_page.get_hotel_info(val.hotel_container_num)
        hotel_search_page.click_select_room_btn(val.hotel_container_num)
        check.is_in(saved.rooms_url, room_page.get_current_url(), "wrong URL")
        room_page.click_close_banner_btn()
        check.equal(room_page.get_room_info(1).get('per_person'), saved.hotel_info.get('per_person'),
                    "wrong per person price of the cheapest room")
        check.equal(room_page.get_room_info(1).get('total'), saved.hotel_info.get('total'),
                    "wrong total price of the cheapest room")
        saved.room_info = room_page.get_room_info(val.room_container_num)
        room_page.click_proceed_to_checkout_btn(val.room_container_num)
        print('\n\n------INPUTTED and SELECTED values--------------\n', json.dumps(val.__dict__, indent=4))
        print('\n\n------SAVED values------------------------------\n', json.dumps(saved.__dict__, indent=4))
        check.is_in(saved.payment_url, payment_page.get_current_url(), "wrong URL")
        payment_page.click_close_banner_btn()
        package_inf = payment_page.get_summary_info()
        print("\n\n---------------PAYMENT package-------------------\n", json.dumps(package_inf, indent=4))
        hotel_inf = payment_page.get_hotel_info()
        print("\n\n---------------PAYMENT HOTEL-------------------\n", json.dumps(hotel_inf, indent=4))
        flights_inf = payment_page.get_flight_info()
        print("\n\n---------------PAYMENT FLIGHTS-------------------\n",
              json.dumps(flights_inf, indent=4))
        check.equal(package_inf["airport_code"], saved.flying_from_code, "Wrong departure airport code in package info")
        check.equal(package_inf['hotel_name'], saved.hotel_info['hotel_name'], "Wrong hotel name in package info")
        check.equal(package_inf["date_from"], saved.month + str(val.from_date), "Wrong from date in package info")
        check.equal(package_inf["date_to"], saved.month + str(val.to_date), "Wrong to date in package info")
        check.equal(hotel_inf['hotel_name'], saved.hotel_info['hotel_name'], "Wrong hotel name in hotel info")
        check.equal(hotel_inf["details"], saved.room_info['details'], "Wrong room details in hotel info")
        check.equal(hotel_inf['date_from'], saved.month + str(val.from_date), "Wrong from date in hotel info")
        check.equal(hotel_inf['date_to'], saved.month + str(val.to_date), "Wrong to date in hotel info")
        check.equal(hotel_inf['adults'], val.adults, "Wrong number of adults in hotel info")
        check.equal(hotel_inf['children'], val.children, "Wrong number of children in hotel info")
        check.equal(flights_inf['departure_code'], saved.flying_from_code,
                    "Wrong departure airport code in flights info")
        check.equal(flights_inf['adults'], val.adults, "Wrong number of adults in flights info")
        check.equal(flights_inf['children'], val.children, "Wrong number of children in flights info")
        for key in saved.departure_flights_info.keys():
            check.equal(flights_inf['departure_flights_info'][key], saved.departure_flights_info[key],
                        "Wrong " + key + " value in departure in flights info ")
        for key in saved.return_flights_info.keys():
            check.equal(flights_inf['return_flights_info'][key], saved.return_flights_info[key],
                        "Wrong " + key + " value in departure in flights info ")

        time.sleep(4)

    def test_soft_check_flights_values(self):
        fh_page = FlightsAndHotelPage(self.driver)
        flights_page = FlightSelectPage(self.driver)
        hotel_search_page = HotelSearchPage(self.driver)
        room_page = RoomPage(self.driver)
        payment_page = PaymentPage(self.driver)
        val = Values()
        saved = SavedValues()
        fh_page.get_page_flight_and_hotels()
        fh_page.input_flying_from(val.flying_from)
        saved.flying_from_code = fh_page.get_1_airport_code()
        fh_page.click_1st_airports_drp_item() \
            .click_travelers_field() \
            .select_adults_number(val.adults) \
            .select_children_number(val.children) \
            .click_from_field() \
            .select_date(val.from_date)
        saved.month = fh_page.get_selected_month()
        fh_page.click_datepicker_day(val.to_date) \
            .click_search_btn() \
            .click_continue_as_guest_btn()
        check.is_in(saved.flights_url, flights_page.get_current_url(), "wrong URL")
        check.is_in(saved.flying_from_code, flights_page.get_origin(),
                    "Origin field doesn't contain airport code: " + saved.flying_from_code)
        check.equal(flights_page.get_from(), saved.month + str(val.from_date), "Wrong from date")
        check.equal(flights_page.get_to(), saved.month + str(val.to_date), "Wrong to date")
        check.equal(flights_page.get_adults(), str(val.adults+1), "Wrong adults number")
        check.equal(flights_page.get_children(), str(val.children), "Wrong children number")
