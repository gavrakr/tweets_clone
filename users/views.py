from django.contrib.auth import authenticate, login, logout
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ParseError, NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import User
from . import serializers
from tweets.serializers import TweetSerializer


class Me(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = serializers.UserSerializer(user)
        return Response(serializer.data)

    def put(self, request):
        user = request.user
        serializer = serializers.UserSerializer(
            user,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            user = serializer.save()
            serializer = serializers.UserSerializer(user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class Users(APIView):
    def get(self, request):
        all_users = User.objects.all()
        serializer = serializers.UserSerializer(
            all_users,
            many=True,
        )
        return Response(serializer.data)

    def post(self, request):
        password = request.data.get("password")
        if not password:
            raise ParseError
        serializer = serializers.UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(password)
            user.save()
            serializer = serializers.UserSerializer(user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class UserDetail(APIView):
    def get(self, request, user_id):
        try:
            user = User.objects.get(username=user_id)
            serializer = serializers.UserSerializer(user)
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


class ChangePassword(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")
        if not old_password or not new_password:
            raise ParseError
        if user.check_password(old_password):
            user.set_password(new_password)
            user.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class LogIn(APIView):

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if not username or not password:
            raise ParseError
        user = authenticate(
            request,
            username=username,
            password=password,
        )
        if user:
            login(request, user)
            return Response({"ok": "Welcome to Tweets!"})
        else:
            return Response({"error": "wrong password"})


class LogOut(APIView):

    def post(self, request):
        logout(request)
        return Response({"ok": "Your logout now! Bye!"})
