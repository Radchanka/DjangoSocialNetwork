from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

from gramm.models import Subscription


class SubscriptionTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = get_user_model().objects.create_user(username='testuser1', email='test1@example.com',
                                                          password='12345')
        self.user2 = get_user_model().objects.create_user(username='testuser2', email='test2@example.com',
                                                          password='12345')

    def test_subscribe(self):
        self.client.force_login(self.user1)

        response = self.client.get(
            reverse('gramm:manage_subscription', kwargs={'user_id': self.user2.id, 'action': 'subscribe'}))

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Subscription.objects.filter(follower=self.user1, following=self.user2).exists())

    def test_unsubscribe(self):
        Subscription.objects.create(follower=self.user1, following=self.user2)

        self.client.force_login(self.user1)

        response = self.client.get(
            reverse('gramm:manage_subscription', kwargs={'user_id': self.user2.id, 'action': 'unsubscribe'})
        )

        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            Subscription.objects.filter(follower=self.user1, following=self.user2).exists())  # Подписка удалена

    def test_followers_list(self):
        Subscription.objects.create(follower=self.user1, following=self.user2)

        self.client.force_login(self.user2)

        response = self.client.get(
            reverse('gramm:manage_subscription', kwargs={'user_id': self.user2.id, 'action': 'followers_list'})
        )

        self.assertEqual(response.status_code, 200)

        followers = response.context['followers']

        self.assertTrue(any(subscription.follower == self.user1 for subscription in followers))
