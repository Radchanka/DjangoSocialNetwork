from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

from gramm.forms import PostForm
from gramm.models import Post


class CreatePostTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        self.client.login(username='testuser', password='testpassword')

    def test_create_post(self):
        post_data = {
            'caption': 'Test Caption',
            'tags': 'tag1, tag2, tag3'
        }

        post_form = PostForm(post_data)

        self.assertTrue(post_form.is_valid())

        response = self.client.post(reverse('gramm:create_post'), post_data, follow=True)

        self.assertIn(response.status_code, [200, 302])

        if response.status_code == 302:
            response = self.client.get(response.url, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Caption')
        self.assertContains(response, 'tag1, tag2, tag3')


class DeletePostTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        self.client.login(username='testuser', password='testpassword')
        self.post = Post.objects.create(
            user=self.user,
            caption='Test Caption'
        )

    def test_delete_post(self):
        response = self.client.post(reverse('gramm:delete_post', kwargs={'post_id': self.post.id}))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('gramm:profile', kwargs={'user_id': self.user.id}))

        self.assertEqual(Post.objects.count(), 0)
