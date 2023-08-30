from datetime import datetime

import allure
import pytest_html
import pytest
from selenium import webdriver


# driver = None
@pytest.fixture(params=["chrome"])
def initialize_driver(request):
    if request.param == "chrome":
        driver = webdriver.Chrome()
    elif request.param == "firefox":
        driver = webdriver.Firefox()
    elif request.param == "edge":
        driver = webdriver.Edge()
    request.cls.driver = driver
    print("Browser: ", request.param)
    driver.maximize_window()
    yield
    # screenshot_path = f"screenshots/{request.node.name}.png"
    # driver.save_screenshot(screenshot_path)
    # allure.attach(driver.get_screenshot_as_png(), name=request.node.name, attachment_type=allure.attachment_type.PNG)
    print("Close Driver")
    driver.close()




@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, "extra", [])
    print("\nAAAAAAAAAAAAAAAAAAAA"
          "aaaaaaaaaaaaaaaaaaa\n", extra, "\nBBBBBBBBBBBBBBBBBBBBBB\n", report, "\nEEEEEEEEEEEEE")















