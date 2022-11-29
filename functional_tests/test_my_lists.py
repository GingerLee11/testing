from django.conf import settings
from django.contrib.auth import BACKEND_SESSION_KEY, SESSION_KEY, get_user_model
from django.contrib.sessions.backends.db import SessionStore

from selenium.webdriver.common.by import By

from .server_tools import create_session_on_server
from .management.commands.create_session import create_pre_authenticated_session
from .base import FunctionalTest, TEST_EMAIL

User = get_user_model()


class MyListsTest(FunctionalTest):

    def create_pre_authenticated_session(self, email):
        if self.staging_server:
            session_key = create_session_on_server(self.staging_server, email)
        else:
            session_key = create_pre_authenticated_session(email)

        ## to set a cookie we need to first visit the domain
        ## 404 pages load the quickest!
        self.browser.get(self.live_server_url + "/404_no_such_url/")
        self.browser.add_cookie(dict(
            name=settings.SESSION_COOKIE_NAME,
            value=session_key,
            path='/',
        ))

    def test_logged_in_users_lists_are_saved_as_my_lists(self):
        email = TEST_EMAIL
        # self.browser.get(self.live_server_url)
        # self.wait_to_be_logged_out(email)

        # Akane is a logged-in user
        self.create_pre_authenticated_session(email)
        self.browser.get(self.live_server_url)
        # self.wait_to_be_logged_in(email)
        self.add_list_item('Perform olympic level feat of athleticism')
        self.add_list_item('Take a "cat" nap')
        first_list_url = self.browser.current_url

        # She notices a "My Lists" link, for the first time.
        self.browser.find_element(By.LINK_TEXT, 'My lists').click()

        # She sees that her lists is in there, named according to its first list item
        self.wait_for(
            self.browser.find_element(By.LINK_TEXT, 'Perform olympic level feat of athleticism')
        )
        self.browser.find_element(By.LINK_TEXT, 'Perform olympic level feat of athleticism').click()
        self.wait_for(lambda:
            self.assertEqual(self.browser.current_url, first_list_url)
        )

        # She decideds to start another list, just to see
        self.browser.get(self.live_server_url)
        self.add_list_item('Play with a ball of yarn')
        second_list_url = self.browser.current_url

        # Under "My lists", her new list appears
        self.browser.find_element(By.LINK_TEXT, 'My lists').click()
        self.wait_for(
            self.browser.find_element(By.LINK_TEXT, 'Play with a ball of yarn')
        )
        self.browser.find_element(By.LINK_TEXT, 'Play with a ball of yarn').click()
        self.wait_for(lambda:
            self.assertEqual(self.browser.current_url, second_list_url)
        )

        # She logs out. The "My lists" option disappears
        self.browser.find_element(By.LINK_TEXT, 'Log out').click()
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element(By.LINK_TEXT, 'My lists'),
            []
        ))
