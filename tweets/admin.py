from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from .models import Tweet, Like


# Filter Definition


class WordFilter(admin.SimpleListFilter):
    title = "Words Filter"
    parameter_name = "word"

    def lookups(self, request, model_admin):
        return [
            ("elon musk", "Elon Musk"),
        ]

    def queryset(self, request, tweets):
        word = self.value()
        if word:
            return tweets.filter(payload__contains=word)
        else:
            return tweets


# Tweet Admin Definition


@admin.register(Tweet)
class TweetAdmin(admin.ModelAdmin):
    list_display = (
        "payload",
        "user",
        "total_like",
        "created_at",
        "updated_at",
    )

    search_fields = (
        "payload",
        "user__username",
    )

    list_filter = (
        WordFilter,
        "created_at",
    )


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "tweet",
        "created_at",
        "updated_at",
    )

    search_fields = ("user__username",)

    list_filter = ("created_at",)
