from rest_framework.test import APITestCase
from rest_framework import status
from users.models import User
from .models import Tweet


class TweetsAPITestCase(APITestCase):
    USER_INFO = {
        "username": "test",
        "email": "test@test.com",
        "name": "testname",
        "gender": "male",
        "password": "123",
    }
    PAYLOAD = "Test Payload"
    URL = "/api/v1/tweets"
    user = User(**USER_INFO)

    def setUp(self):
        self.user.save()
        Tweet.objects.create(
            user=self.user,
            payload=self.PAYLOAD,
        )

    def test_get_tweets(self):
        response = self.client.get(self.URL)
        data = response.json()
        self.assertEqual(
            response.status_code,
            200,
            "Status code is not 200.",
        )
        self.assertIsInstance(
            data,
            list,
        )
        self.assertEqual(
            len(data),
            1,
        )
        self.assertEqual(
            data[0]["payload"],
            self.PAYLOAD,
        )
        self.assertEqual(
            data[0]["user"]["username"],
            self.USER_DICT["username"],
        )

    def test_post_tweets(self):
        self.client.force_login(
            self.user,
        )
        response = self.client.post(
            self.URL,
            data={
                "user": self.user,
                "payload": self.PAYLOAD,
            },
        )
        data = response.json()
        self.assertEqual(
            response.status_code,
            200,
            "Status code is not 200.",
        )
        self.assertEqual(
            data["payload"],
            self.PAYLOAD,
        )
        response = self.client.post(self.URL)
        data = response.json()
        self.assertEqual(
            response.status_code,
            400,
        )
        self.assertIn(
            "payload",
            data,
        )


class TweetAPITestCase(APITestCase):

    USER_INFO = {
        "username": "test",
        "email": "test@test.com",
        "name": "testname",
        "gender": "male",
        "password": "123",
    }
    PAYLOAD = "Test Payload"
    URL = "/api/v1/tweets"
    user = User(**USER_INFO)

    def setUp(self):
        self.user.save()
        Tweet.objects.create(
            user=self.user,
            payload=self.PAYLOAD,
        )

    def test_get_tweet(self):
        response = self.client.get(self.URL)
        data = response.json()
        self.assertEqual(
            response.status_code,
            200,
            "Status code is not 200.",
        )
        self.assertIsInstance(
            data,
            dict,
        )
        self.assertEqual(
            data["payload"],
            self.PAYLOAD,
        )
        self.assertEqual(
            data["user"]["username"],
            self.USER_DICT["username"],
        )

    def test_put_tweet(self):
        self.client.force_login(
            self.user,
        )
        response = self.client.put(
            self.URL,
            data={
                "user": self.user,
                "payload": self.NEW_PAYLOAD,
            },
        )
        data = response.json()
        self.assertEqual(
            response.status_code,
            200,
            "Status code is not 200.",
        )
        self.assertEqual(
            data["payload"],
            self.NEW_PAYLOAD,
        )

    def test_delete_tweet(self):
        self.client.force_login(
            self.user,
        )
        response = self.client.delete(self.URL)
        self.assertEqual(
            response.status_code,
            200,
            "Status code is not 200.",
        )
