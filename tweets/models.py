from django.db import models
from users.models import User
from common.models import CommonModel

# Tweet Model Definition


class Tweet(CommonModel):
    payload = models.TextField(max_length=180)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="tweets",
    )

    def total_like(self):
        return self.likes.count()

    def __str__(self):
        return self.payload


class Like(CommonModel):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="likes",
    )
    tweet = models.ForeignKey(
        Tweet,
        on_delete=models.SET_NULL,
        related_name="likes",
        null=True,
    )

    def __str__(self):
        return str(self.tweet)
