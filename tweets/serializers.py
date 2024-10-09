from rest_framework import serializers
from .models import Tweet


# class TweetSerializer(serializers.Serializer):

# payload = serializers.CharField()
# user = serializers.CharField(read_only=True)
# created_at = serializers.DateTimeField(read_only=True)


class TweetSerializer(serializers.ModelSerializer):
    user = serializers.CharField()

    class Meta:
        model = Tweet
        # fields = "__all__"
        exclude = (
            "created_at",
            "updated_at",
        )
