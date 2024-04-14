from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

from gramm.models import Post, Tag


class TagPostsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        self.tag = Tag.objects.create(name='testtag')
        self.post = Post.objects.create(
            user=self.user,
            caption='Test Caption'
        )
        self.post.tags.add(self.tag)

    def test_tag_posts(self):
        response = self.client.get(reverse('gramm:tag_posts', kwargs={'tag_name': self.tag.name}))

        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.context['tag'], self.tag)
        self.assertIn(self.post, response.context['posts'])

        self.assertContains(response, self.post.caption)
