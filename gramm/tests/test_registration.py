from django.test import TestCase, Client
from django.urls import reverse
from django.core import mail


class RegisterViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse('gramm:register')

    def test_register_view_get(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')

    def test_register_view_post_success(self):
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'full_name': 'Test User',
            'password1': 'testpassword',
            'password2': 'testpassword',
        }
        response = self.client.post(self.register_url, data, follow=True)

        self.assertTemplateUsed(response, 'activation_info.html')

        self.assertRedirects(response, reverse('gramm:activation_info'))

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Activate your account on DjangoGramm')

    def test_register_view_post_failure(self):
        data = {
            'email': 'invalid_email',
            'password1': 'testpassword',
            'password2': 'testpassword',
        }
        response = self.client.post(self.register_url, data, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')
        self.assertContains(response, 'Enter a valid email address.')
