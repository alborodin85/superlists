from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import unittest
from selenium.webdriver.common.by import By
from django.test import LiveServerTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.common.exceptions import WebDriverException

MAX_WAIT = 2


class NewVisitorTest(StaticLiveServerTestCase):
    """Тест нового посетителя"""

    def test_layout_and_styling(self):
        """Тест макета стилевого оформления"""
        # Эдит открывает домашнюю страницу
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        # Она замечает, что поле ввода аккуратно центрировано
        inputBox = self.browser.find_element(By.ID, 'id_new_item')
        self.assertAlmostEqual(inputBox.location['x'] + inputBox.size['width']/2, 512, delta=10)

        # Она начинает новый список и видит, что поле ввода там тоже аккуратно центрировано
        inputBox.send_keys('testing')
        inputBox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: testing')
        inputBox = self.browser.find_element(By.ID, 'id_new_item')
        self.assertAlmostEqual(inputBox.location['x'] + inputBox.size['width']/2, 512, delta=10)
    def setUp(self) -> None:
        """Установка"""
        self.browser = webdriver.Firefox()

    def tearDown(self) -> None:
        """Демонтаж"""
        self.browser.refresh()
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        """Подтверждение строки в таблице списка"""
        table = self.browser.find_element(By.ID, 'id_list_table')
        rows = table.find_elements(By.TAG_NAME, 'tr')
        self.assertIn(row_text, [row.text for row in rows])

    def wait_for_row_in_list_table(self, row_text):
        """Ожидать строку в таблице списка"""
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element(By.ID, 'id_list_table')
                rows = table.find_elements(By.TAG_NAME, 'tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.1)

    def test_can_start_a_list_for_one_user(self):
        """Тест: можно начать список для одного пользователя"""
        # Эдит слышала про крутое онлайн-решение со списком неотложных дел. Она решает оценить домашнюю страницу.
        self.browser.get(self.live_server_url)

        # Она видит, что заголовок и шапка страницы говорят о списках неотложных дел
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element(By.TAG_NAME, 'h1').text
        self.assertIn('To-Do', header_text)

        # Ей сразу же предлагается ввести элемент списка
        inputBox = self.browser.find_element(By.ID, 'id_new_item')
        self.assertEqual(
            inputBox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        # Она набирает в текстовом поле "Купить павлиньи перья"
        inputBox.send_keys('Купить павлиньи перья')

        # Когда она нажимает Enter, страница обновляется, и теперь страница содержит "1: Купить павлиньи перья"
        inputBox.send_keys(Keys.ENTER)
        time.sleep(1)
        self.wait_for_row_in_list_table('1: Купить павлиньи перья')

        # Текстовое поле по-прежнему приглашает ее добавить еще один элемент. Она вводит "Сделать мушку из павлиньих перьев"
        inputBox = self.browser.find_element(By.ID, 'id_new_item')
        inputBox.send_keys('Сделать мушку из павлиньих перьев')
        inputBox.send_keys(Keys.ENTER)
        time.sleep(1)

        # Страница снова обновляется. И теперь показывает оба элемента списка.
        self.wait_for_row_in_list_table('1: Купить павлиньи перья')
        self.wait_for_row_in_list_table('2: Сделать мушку из павлиньих перьев')

        # Удовлетворенная она снова ложится спать

    def test_multiple_users_can_start_lists_at_different_urls(self):
        """Тест: многочисленные пользователи могут начать списки по разным url"""
        # Эдит начинает новый список
        self.browser.get(self.live_server_url)
        inputBox = self.browser.find_element(By.ID, 'id_new_item')
        inputBox.send_keys('Купить павлиньи перья')
        inputBox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Купить павлиньи перья')

        # Она замечает, что ее список имеет уникальный URL-адрес
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/lists/.+')

        # Теперь новый пользователь Френсис приходит на сайт
        ## Мы используем новый сеанс браузера, тем самым обеспечивая, чтобы никакая информация от Эдит не прошла через данные cookie и пр.
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Френсис посещает домашнюю страницу. Нет никаких признаков списка Эдит
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertNotIn('Купить павлиньи перья', page_text)
        self.assertNotIn('Сделать мушку', page_text)

        # Френсис начинает новый список, вводя новый элемент. Он менее интересен, чем список Эдит
        inputBox = self.browser.find_element(By.ID, 'id_new_item')
        inputBox.send_keys('Купить молоко')
        inputBox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Купить молоко')

        # Френсис получает уникальный URL-адрес
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, '/lists/.+')
        self.assertNotEqual(francis_list_url, edith_list_url)

        # Опять-таки нет следа от списка Эдит
        page_text = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertNotIn('Купить павлиньи перья', page_text)
        self.assertIn('Купить молоко', page_text)

        # Удовлетворенные они оба ложатся
