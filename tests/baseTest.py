import pytest
import softest


@pytest.mark.usefixtures("initialize_driver")
class BaseTest:
    pass
