from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer
from tweets.serializers import TweetSerializer
from .models import User


class Users(APIView):
    def get(self, request):
        all_users = User.objects.all()
        serializer = UserSerializer(
            all_users,
            many=True,
        )
        return Response(serializer.data)


class UserDetail(APIView):
    def get(self, request, user_id):
        try:
            user = User.objects.get(username=user_id)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response({"ok": False})


class UserTweets(APIView):
    def get(self, request, user_id):
        try:
            user = User.objects.get(username=user_id)
            all_tweets = user.tweets.all()
            serializer = TweetSerializer(all_tweets, many=True)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response({"ok": False})
