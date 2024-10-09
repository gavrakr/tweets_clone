from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.status import HTTP_204_NO_CONTENT
from .models import Tweet
from .models import User
from .serializers import TweetSerializer


class Tweets(APIView):

    def get(self, request):
        all_tweets = Tweet.objects.all()
        serializer = TweetSerializer(
            all_tweets,
            many=True,
        )
        return Response(serializer.data)

    def post(self, request):
        pass


class TweetDefail(APIView):
    def get_object(self, pk):
        return Tweet.objects.get(pk=pk)

    def get(self, request, pk):
        serializer = TweetSerializer(self.get_object(pk))
        return Response(serializer.data)

    def put(self, request, pk):
        serializer = TweetSerializer(
            self.get_object(pk),
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            updated_category = serializer.save()
            return Response(TweetSerializer(updated_category).data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        self.get_object(pk).delete()
        return Response(status=HTTP_204_NO_CONTENT)


class TweetsBoard(APIView):

    def get(self, request):
        tweets = Tweet.objects.all()
        return render(
            request,
            "tweet.html",
            {
                "title": "Tweet Main Page",
                "tweets": tweets,
            },
        )
