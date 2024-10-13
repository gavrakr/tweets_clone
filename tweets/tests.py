from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.response import Response
from users.models import User
from .models import Tweet


class TweetsAPITestCase(APITestCase):
    user_info = {
        "username": "tester10",
        "email": "tester10@test.co.kr",
        "name": "tester",
        "gender": "mail",
    }
    test_user = User(**user_info)
    test_payload = "tweets test"
    test_urls = "/api/v1/tweets/"

    def setUp(self):
        self.test_user.save()
        Tweet.objects.create(
            user=self.test_user,
            payload=self.test_payload,
        )

    def test_all_tweets(self):
        response = self.client.get(self.test_urls)
        data = response.json()
        self.assertEqual(
            response.status_code,
            200,
            "Status code isn't 200.",
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
            self.test_payload,
        )

        self.assertEqual(
            data[0]["user"],
            self.user_info["username"],
        )

    def test_create_tweet(self):
        self.client.force_login(
            self.test_user,
        )
        response = self.client.post(
            self.test_urls,
            data={
                "user": self.test_user,
                "payload": self.test_payload,
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
            self.test_payload,
        )


class TweetDetailAPITestCase(APITestCase):
    user_info = {
        "username": "tester1",
        "email": "tester10@test.co.kr",
        "name": "tester",
        "gender": "mail",
    }
    test_user = User(**user_info)
    test_payload = "tweets test"
    test_new_payload = "new test payload"
    test_url = "/api/v1/tweets/1/"

    def setUp(self):
        self.test_user.save()
        Tweet.objects.create(
            user=self.test_user,
            payload=self.test_payload,
        )

    def test_get_tweet(self):
        response = self.client.get(self.test_url)
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
            self.test_payload,
        )
        self.assertEqual(
            data["user"],
            self.user_info["username"],
        )

    def test_put_tweet(self):
        self.client.force_login(
            self.test_user,
        )
        response = self.client.put(
            self.test_url,
            data={
                "user": self.test_user,
                "payload": self.test_new_payload,
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
            self.test_new_payload,
        )

    def test_delete_tweet(self):
        self.client.force_login(
            self.test_user,
        )

        response = self.client.delete(self.test_url)

        self.assertEqual(
            response.status_code,
            200,
            "Status code is not 200.",
        )
