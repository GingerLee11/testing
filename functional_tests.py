from selenium import webdriver
import unittest


class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()


    def test_can_start_a_list_and_retrieve_it_later(self):

        # User can access online to-do app
        # This accesses the homepage
        self.browser.get('http://localhost:8000')


        # This should be what the user sees in the page title
        self.assertIn('To-Do', self.browser.title)
        self.fail('Finish the test!')

        # User should be able to add a to-do list item into a text box immediately
        # And that item will show up as:
        # "1: Item 1"

        # The text box will then reappear below the first item

        # The site will remember the user's list by generating a unique URL 
        # (there will also be explanatory text as to how this is done)

        # User should be able to revisit the site and see the to-do list


if __name__ == "__main__":
    unittest.main()
