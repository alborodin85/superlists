from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import unittest
from selenium.webdriver.common.by import By


class NewVisitorTest(unittest.TestCase):
    '''Тест нового посетителя'''

    def setUp(self) -> None:
        '''Установка'''
        self.browser = webdriver.Firefox()

    def tearDown(self) -> None:
        '''Демонтаж'''
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        '''тест: можно начать список и получить его позже'''
        # Эдит слышала про крутое онлайн-решение со списком неотложных дел. Она решает оценить домашнюю страницу.
        self.browser.get('http://localhost:8000')

        # Она видит, что заголовок и шапка страницы говорят о списках неотложных дел
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element(By.TAG_NAME, 'h1').text
        self.assertIn('To-Do', header_text)

        # Ей сразу же предлагается ввести элемент списка
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        # Она набирает в текстовом поле "Купить павлиньи перья"
        inputbox.send_keys('Купить павлиньи перья')

        # Когда она нажимает Enter, страница обновляется, и теперь страница содержит "1: Купить павлиньи перья"
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        table = self.browser.find_element(By.ID, 'id_list_table')
        rows = table.find_elements(By.TAG_NAME, 'tr')
        self.assertTrue(
            any(row.text == '1: Купить павлиньи перья' for row in rows),
            "Новый элемент списка не появился в таблице"
        )

        # Текстовое поле по-прежнему приглашает ее добавить еще один элемент. Она вводит "Сделать мушку из павлиньих перьев"
        self.fail('Дописать тест!')

        # Страница снова обновляется. И теперь показывает оба элемента списка.

        # Эдит интересно, запомнит ли сайт ее список. Далее она видит, что сайт сгенерировал для нее уникальный URL-адрес - об этом выводится небольшой текст с разъяснениями

        # Она посещает этот URL-адрес. Ее список по прежнему там

        # Удовлетворенная она снова ложится спать


if __name__ == '__main__':
    unittest.main(warnings='ignore')
