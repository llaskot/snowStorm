from datetime import datetime

import pytest
from selenium import webdriver



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
    print("Close Driver")
    driver.close()


# /test/

















