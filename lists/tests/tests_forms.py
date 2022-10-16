from django.test import TestCase
from lists.forms import ItemForm

class ItemFormTest(TestCase):
    """Тест формы для элемента списка"""
    def test_form_renders_item_test_input(self):
        """Тест: форма отображает текстовое поле ввода"""
        form = ItemForm()
        self.fail(form.as_p())

    def test_form_item_input_has_placeholder_and_css_classes(self):
        """Тест: поле ввода имеет атрибут placeholder и css-классы"""
        form = ItemForm()
        self.assertIn('placeholder="Enter a to-do item"', form.as_p())
        self.assertIn('class="form-control input-lg"', form.as_p())
