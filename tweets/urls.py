from django.urls import path
from . import views

urlpatterns = [
    path("", views.Tweets.as_view()),
    path("<int:pk>/", views.TweetDefail.as_view()),
    path("tweets_board/", views.TweetsBoard.as_view()),
]
