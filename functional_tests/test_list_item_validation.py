from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException

from unittest import skip

from .base import FunctionalTest


class ItemValidationTest(FunctionalTest):

    def get_error_element(self):
        return self.browser.find_element(By.CSS_SELECTOR, '.has-error')

    def test_cannot_add_empty_list_items(self):
        # Akane goes to the home page and accidentally tries to submit an empty list item.
        
        # She hits Enter on the empty input box.
        self.browser.get(self.live_server_url)

        self.get_item_input_box().send_keys(Keys.ENTER)

        # The home page refreshes, and there is an error message saying that list items 
        # cannot be blank
        ## The browser may intercept the request, and does not load the list page
        self.wait_for(lambda:
            self.browser.find_element(By.CSS_SELECTOR, '#id_text:invalid'))
        # She tries again with some text for the item, which now works
        self.get_item_input_box().send_keys('Look for fish')
        self.wait_for(lambda:
            self.browser.find_element(By.CSS_SELECTOR, '#id_text:valid'))

        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Look for fish')
        # Perversely, she now decided to submit a second blank list item
        self.get_item_input_box().send_keys(Keys.ENTER)
                
        # She receives a similar warning on the list page
        self.wait_for(lambda:
            self.browser.find_element(By.CSS_SELECTOR, '#id_text:invalid')
        )

        # And she can correct it by filling some text in
        self.get_item_input_box().send_keys('Try to catch fish without getting wet')
        self.wait_for(lambda:
            self.browser.find_element(By.CSS_SELECTOR, '#id_text:valid'))
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Look for fish')
        self.wait_for_row_in_list_table('2: Try to catch fish without getting wet')

    def test_cannot_add_duplicate_items(self):
        # Akane goes to the home page and starts a new list
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys('Eat Fish')
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Eat Fish')

        # She accidentally tries to enter a duplicate item
        self.get_item_input_box().send_keys('Eat Fish')
        self.get_item_input_box().send_keys(Keys.ENTER)

        # She sees a helpul error message
        self.wait_for(lambda: self.assertEqual(
            self.get_error_element().text,
            "You've already got this in your list"
        ))

    def test_error_messages_are_cleared_on_input(self):
        # Akane starts a list and causes a validation error:
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys('Lands on her feet')
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Lands on her feet')
        self.get_item_input_box().send_keys('Lands on her feet')
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for(lambda: self.assertTrue(
            self.get_error_element().is_displayed()
        ))
        # She starts typing in the input box to clear the error
        self.get_item_input_box().send_keys('a')
        
        # She is pleased to see that the error message disappears
        self.wait_for(lambda: self.assertFalse(
            self.get_error_element().is_displayed()
        ))