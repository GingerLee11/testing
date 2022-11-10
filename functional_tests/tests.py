from django.test import LiveServerTestCase

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException

import time
import unittest

MAX_WAIT = 10


class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def wait_for_row_in_list_table(self, row_text):
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
                time.sleep(0.5)

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
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
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

        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        inputbox.send_keys("Stat monster for Stonetop")
        inputbox.send_keys(Keys.ENTER)

        # The user will then enter in "Stat monster for Stonetop"
        self.wait_for_row_in_list_table('2: Stat monster for Stonetop')
        self.wait_for_row_in_list_table('1: Prep for Stonetop campaign')

        # The site will remember the user's list by generating a unique URL 
        # (there will also be explanatory text as to how this is done)

        # User should be able to revisit the site and see the to-do list

        self.fail('Finish the test!')