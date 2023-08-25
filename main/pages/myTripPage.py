import time

from selenium.webdriver.common.by import By

from main.pages.basePage import BasePage


class MyTripPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    package = (By.XPATH,
               "//h2[text()='SEARCHED']/..//li[@class='gray-block']//span[text()='Package']/../following-sibling::div")

    package_block = (By.XPATH, "//h2[text()='SEARCHED']/..//li[@class='gray-block']//span[text()='Package']/../../..")

    t_and_c_popup = (By.XPATH, "//div[@id='CombinedpackageTnC']//div[@class='modal-content']")

    baggage_policy_popup = (By.XPATH, "//div[@class='modal fade in']//div[contains(text(), 'Baggage Policy')]/..")
    baggage_policy_popup_flights = \
        (By.XPATH, "//div[@class='modal fade in']//div[contains(text(), 'Baggage Policy')]/..//tbody/tr/td[1]")
    invite_friend = (By.XPATH, "//a[@data-target='#InviteTripModal' and contains(@class,'tooltip-toggle-friend')]")
    invite_popup = (By.XPATH, "//div[@id='InviteTripModal']//div[@class='modal-content']")
    your_name_field = (By.XPATH, ".//input[@name='clientTitle']")
    next_btn = (By.XPATH, ".//button[@id='EditTripButton']")
    recipient_name = (By.XPATH, ".//input[@name='RecipientName[]']")
    recipient_mail = (By.XPATH, ".//input[@name='RecipientEmail[]']")
    submit_btn = (By.XPATH, "//div[@id='InviteTripModal']//div[@class='modal-content']//button[@id='inviteTripSubmit']")
    sent_btn = (By.XPATH, "//div[@id='InviteTripModal']//div[@class='modal-content']//div[@id='sent_btn']")

    def get_package_num(self):
        return self.find_by(self.package).text.strip()[0]

    def click_terms_cond(self):
        time.sleep(1)
        self.scroll_to(self.find_by(self.package_block) \
                       .find_element(By.XPATH,
                                     ".//div[@class='row accordian-head']//a[text()='Terms & Conditions']")).click()
        return self

    def package_terms_and_cond_text(self):
        return self.find_by(self.t_and_c_popup).text.strip()

    def click_package_t_c_popup_close(self):
        self.scroll_to(self.find_by(self.t_and_c_popup).find_element(By.XPATH, ".//button")).click()
        return self

    def click_checked_baggage(self):
        time.sleep(0.5)
        self.find_by(self.package_block).find_element(By.XPATH, ".//a[text()='Checked Baggage']").click()
        return self

    def get_baggage_policy_flights(self):
        return list(map(lambda a: a.text, self.find_elements(self.baggage_policy_popup_flights, 10)))

    def click_close_baggage_popup(self):
        self.find_by(self.baggage_policy_popup).find_element(By.XPATH, ".//button[@class='close']").click()
        time.sleep(0.2)
        return self

    def click_invite_friend(self):
        el = self.find_by(self.invite_friend)
        a = (By.XPATH, "//a[text()='EDocs']")
        self.scroll_to(self.find_by(a))
        time.sleep(5)
        el.click()
        return self

    def input_your_name(self, name):
        self.find_by(self.invite_popup).find_element(*self.your_name_field).send_keys(name)
        return self

    def click_next(self):
        self.find_clickable(self.invite_popup).find_element(*self.next_btn).click()
        return self

    def input_friend_name(self, name):
        self.find_clickable(self.recipient_name).send_keys(name)
        return self

    def input_friend_email(self, mail):
        self.find_clickable(self.invite_popup).find_element(*self.recipient_mail).send_keys(mail)
        return self

    def click_submit_btn(self):
        self.find_clickable(self.submit_btn).click()
        return self

    def get_visibility_sent_btn(self):
        return self.find_presence(self.sent_btn, 3).is_displayed()

    def click_close_invite_popup(self):
        self.find_by(self.invite_popup).find_element(By.XPATH, ".//button[@class='close ng-scope']").click()
        return self

    def click_search_pac_details(self):
        self.scroll_to(self.find_by(self.package_block).find_element(By.XPATH,
                                                                     ".//*[contains(@href,'/us/Itinerary/')]")).click()
