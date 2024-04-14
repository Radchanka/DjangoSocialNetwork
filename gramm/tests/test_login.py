from django.test import TestCase, Client
from django.urls import reverse

from gramm.models import CustomUser


class LoginViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.login_url = reverse('gramm:login')
        self.user = CustomUser.objects.create_user(username='testuser', email='test@example.com',
                                                   password='testpassword')

    def test_login_view_get(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_login_view_post_failure(self):
        response = self.client.post(self.login_url, {'username': 'testuser', 'password': 'wrongpassword'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')
        self.assertContains(response, 'Please enter a correct username and password.', status_code=200)

    def test_login_view_post_success(self):
        response = self.client.post(self.login_url, {'username': 'testuser', 'password': 'testpassword'})
        self.assertRedirects(response, expected_url=reverse('gramm:profile', args=[self.user.id]),
                             fetch_redirect_response=False)
