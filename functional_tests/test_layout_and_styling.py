from .base import FunctionalTest
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


class LayoutAndStylingTest(FunctionalTest):
    """Тест макета и стилевого оформления"""
    def test_layout_and_styling(self):
        """Тест макета стилевого оформления"""
        # Эдит открывает домашнюю страницу
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        # Она замечает, что поле ввода аккуратно центрировано
        inputBox = self.get_item_input_box()
        self.assertAlmostEqual(inputBox.location['x'] + inputBox.size['width'] / 2, 512, delta=10)

        # Она начинает новый список и видит, что поле ввода там тоже аккуратно центрировано
        inputBox.send_keys('testing')
        inputBox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: testing')
        inputBox = self.get_item_input_box()
        self.assertAlmostEqual(inputBox.location['x'] + inputBox.size['width'] / 2, 512, delta=10)
