import pytest
from selenium import webdriver
import softest


@pytest.fixture(scope="class")
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


@pytest.mark.usefixtures("initialize_driver")
class MyTestClass(softest.TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Здесь можно выполнять дополнительные настройки перед всем классом

    @classmethod
    def tearDownClass(cls):
        # Здесь можно выполнять дополнительные действия после всего класса
        super().tearDownClass()

    def test_example(self):
        # Ваш тестовый метод
        self.soft_assert.assertEqual(2 + 2, 4)
        self.soft_assert.assertAll()

    def test_another_example(self):
        # Ваш тестовый метод
        self.soft_assert.assertEqual(3 * 3, 9)
        self.soft_assert.assertAll()