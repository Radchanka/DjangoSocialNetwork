from selenium import webdriver
from django.test import LiveServerTestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from selenium.webdriver.common.by import By


class ProfileViewTest(LiveServerTestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='test@example.com',
            username='testuser',
            password='testpass',
            full_name='full_name_test',
        )
        self.driver = webdriver.Chrome()

    def tearDown(self):
        self.driver.quit()

    def test_profile_view_with_selenium(self):
        self.client.login(username='testuser', password='testpass')

        self.driver.get(self.live_server_url + reverse('gramm:profile', args=[self.user.id]))

        self.assertEqual(self.driver.title, 'testuser Profile - DjangoGramm')

        self.assertIn('testuser', self.driver.page_source)
        self.assertIn('user', self.driver.page_source)

    def test_edit_profile_view(self):
        self.driver.get(self.live_server_url + reverse('gramm:edit_profile', args=[self.user.id]))

        full_name_input = self.driver.find_element(By.NAME, 'full_name')
        full_name_input.send_keys('New Full Name')

        biography_input = self.driver.find_element(By.NAME, 'biography')
        biography_input.send_keys('New Biography')

        submit_button = self.driver.find_element(By.CSS_SELECTOR, '.btn-primary')
        submit_button.click()

        self.assertEqual(self.driver.current_url,
                         self.live_server_url + reverse('gramm:edit_profile', args=[self.user.id]))
