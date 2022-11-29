from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from .base import FunctionalTest


class NewVisitorTest(FunctionalTest):

    def test_can_start_a_list_and_retrieve_it_later(self):

        # User can access online to-do app
        # This accesses the homepage
        self.browser.get(self.live_server_url)

        # This should be what the user sees in the page title
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element(By.TAG_NAME, 'h1').text
        self.assertIn('To-Do', header_text)

        # User should be able to add a to-do list item into a text box immediately
        # The placeholder for the box should be 'Enter a to-do list'
        inputbox = self.get_item_input_box()
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )
        # User will type in "Prep for Stonetop campaign"
        inputbox.send_keys("Prep for Stonetop campaign")

        # After hitting enter, the page updates, and now the page list
        # "1: Prep for Stonetop campaign" as an item in a to-do list table
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Prep for Stonetop campaign')

        # The text box will then reappear below the first item
        self.add_list_item("Stat monster for Stonetop")

        # The user will then enter in "Stat monster for Stonetop"
        self.wait_for_row_in_list_table('2: Stat monster for Stonetop')
        self.wait_for_row_in_list_table('1: Prep for Stonetop campaign')
        # The site will remember the user's list by generating a unique URL 
        # (there will also be explanatory text as to how this is done)
        # User should be able to revisit the site and see the to-do list

    def test_multiple_users_can_start_lists_at_different_urls(self):
        # Scott starts a new to-do list
        self.browser.get(self.live_server_url)
        inputbox = self.get_item_input_box()
        # User will type in "Prep for Stonetop campaign"
        inputbox.send_keys("Prep for Stonetop campaign")

        # After hitting enter, the page updates, and now the page list
        # "1: Prep for Stonetop campaign" as an item in a to-do list table
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Prep for Stonetop campaign')

        # Scott notices that his list has a unique URL
        scott_list_url = self.browser.current_url
        self.assertRegex(scott_list_url, '/lists/.+')

        # A new user, Kay, comes along to the site
        ## We use a new browser session to make sure that no information
        ## of Edith's is coming through from cookies
        self.browser.quit()
        self.browser = webdriver.Firefox()

        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertNotIn('1: Prep for Stonetop campaign', page_text)
        self.assertNotIn('2: Stat monster for Stonetop', page_text)

        # Kay starts a new list by entering a new item.
        inputbox = self.get_item_input_box()
        self.add_list_item('Pick new move for Isra')

        # Kay gets their own URL
        kay_list_url = self.browser.current_url
        self.assertRegex(kay_list_url, '/lists/.+')
        self.assertNotEqual(kay_list_url, scott_list_url)

        # Again there is no trace of Scott's list
        page_text = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertNotIn('Prep for Stonetop campaign', page_text)
        self.assertIn('Pick new move for Isra', page_text)
