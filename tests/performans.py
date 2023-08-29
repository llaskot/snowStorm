import json
import random
import time
import pytest_check as check

from main.pages.flightSelectPage import FlightSelectPage
from main.pages.flightsAndHotel_page import FlightsAndHotelPage
from main.pages.hotelSearchPage import HotelSearchPage
from main.pages.myTripPage import MyTripPage
from main.pages.packageDetailsPage import PackageDetailsPage
from main.pages.roomsPage import RoomPage
from tests.baseTest import BaseTest


class Values:
    def __init__(self):
        self.flying_from = 'LAX'
        self.from_date = random.randint(8, 22)
        self.max_wait = 300
        self.avia_company = "United Airlines"
        self.hotels = ["FLAMINGO LAS VEGAS", "RIO ALL-SUITE HOTEL & CASINO"]
        self.your_name = "Alayna Sanudo"
        self.friend_name = "Elena Besedina"
        self.friend_email = "nouwokaunique-1271@yopmail.com"
        self.max_preloader_time = 180


class SavedValues:
    def __init__(self):
        # self.home_url = "https://caesars.cs-uat.mybookingplatform.com/Flight/Search?combined=3"
        # self.home_url = "https://caesarsprod.mybookingplatform.com/Flight/Search?combined=3"
        self.home_url = "https://flights-hotels.caesars.com/Flight/Search?combined=3"
        self.flying_from_code = 0
        self.month = 0
        self.departure_flights_info = {}
        self.return_flights_info = {}
        self.flight_price = {}
        self.hotel_info = {}
        self.room_info = {}
        self.loader_duration = {}


class TestCriticalPath(BaseTest):

    def test_main_path(self):
        fh_page = FlightsAndHotelPage(self.driver)
        flights_page = FlightSelectPage(self.driver)
        hotel_search_page = HotelSearchPage(self.driver)
        room_page = RoomPage(self.driver)
        my_trip_page = MyTripPage(self.driver)
        pack_details_page = PackageDetailsPage(self.driver)
        val = Values()
        saved = SavedValues()
        fh_page.get_page_flight_and_hotels(saved.home_url)
        fh_page.input_flying_from(val.flying_from)
        fh_page.click_1st_airports_drp_item() \
            .click_from_field() \
            .select_date(val.from_date) \
            .click_search_btn() \
            .click_continue_as_guest_btn_no_wait()
        saved.loader_duration["search flights"] = flights_page.loader_visibility_time(val.max_wait)
        # flights_page.click_close_banner_btn() \
        flights_page.scroll_flights() \
            .click_select_flight_btn(val.avia_company)
        saved.loader_duration["select flight"] = hotel_search_page.loader_visibility_time(val.max_wait)
        # hotel_search_page.click_close_banner_btn() \
        hotel_search_page.click_select_room_btn(val.hotels)
        saved.loader_duration["Select hotel"] = room_page.loader_visibility_time(val.max_wait)
        # room_page.click_close_banner_btn() \
        room_page.click_add_to_trip(1)
        time.sleep(30)
        saved.loader_duration["add to my trip"] = room_page.loader_visibility_time(val.max_wait)
        time.sleep(1)
        room_page.click_my_trip()
        saved.loader_duration["get my trip"] = my_trip_page.loader_visibility_time(val.max_wait)
        # my_trip_page.click_close_banner_btn()
        check.equal(my_trip_page.get_package_num(), "1", "ERROR: Incorrect package number")
        my_trip_page.click_terms_cond()
        if my_trip_page.get_t_and_c_display_block():
            info = my_trip_page.package_terms_and_cond_text()
            check.is_in("Fully cancellable and refundable without penalty.", info,
                        "\nPACKAGE TERMS & CONDITIONS popup does not contains text: "
                        "Fully cancellable and refundable without penalty.")
            check.is_in("Room amount will be refunded and airline credit provided (if available).", info,
                        "\nPACKAGE TERMS & CONDITIONS popup does not contains text: "
                        "Room amount will be refunded and airline credit provided (if available).")
            check.is_in("Cancelable, non-changeable and non-refundable.", info,
                        "\nPACKAGE TERMS & CONDITIONS popup does not contains text: "
                        "Cancelable, non-changeable and non-refundable.")
            my_trip_page.click_package_t_c_popup_close()
            print("PACKAGE TERMS & CONDITIONS popup has been reviewed")
        else:
            check.is_true(my_trip_page.t_and_c_popup_is_visible())
            print("PACKAGE TERMS & CONDITIONS popup has NOT been reviewed")

        my_trip_page.click_checked_baggage()
        check.equal(flights_page.depart_info['number_of_flights'] + flights_page.return_info['number_of_flights']
                    , len(my_trip_page.get_baggage_policy_flights()), "Wrong flights number in 'Baggage Policy' popup")
        my_trip_page.click_close_baggage_popup()

        my_trip_page.click_invite_friend() \
            .input_your_name(val.your_name) \
            .click_next() \
            .input_friend_name(val.friend_name) \
            .input_friend_email(val.friend_email) \
            .click_submit_btn()
        time.sleep(30)
        check.is_true(my_trip_page.get_visibility_sent_btn(), "Button 'SENT' is not visible in 5 sec")
        my_trip_page.click_close_invite_popup()

        my_trip_page.click_search_pac_details()
        saved.loader_duration["get Package Details"] = pack_details_page.loader_visibility_time(val.max_wait)
        self.driver.switch_to.window(self.driver.window_handles[1])
        check.is_in(flights_page.depart_info["1th_flight_company"], pack_details_page.get_departure_1th_flight(),
                    "Wrong avia company in package detail DEPARTURE")
        check.is_in(flights_page.depart_info["1th_flight_num"], pack_details_page.get_departure_1th_flight(),
                    "Wrong flight in package detail DEPARTURE")
        check.is_in(flights_page.return_info["1th_flight_company"], pack_details_page.get_return_1th_flight(),
                    "Wrong avia company in package detail RETURN")
        check.is_in(flights_page.return_info["1th_flight_num"], pack_details_page.get_return_1th_flight(),
                    "Wrong flight in package detail RETURN")
        for key in saved.loader_duration:
            print(key, saved.loader_duration[key])
            check.less_equal(saved.loader_duration[key], val.max_preloader_time,
                             "Preloader " + key + " has been worked longer then expected " + str(
                                 val.max_preloader_time) + " sec")
        time.sleep(5)
