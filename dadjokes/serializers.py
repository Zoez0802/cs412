# dadjokes/serializers.py
# author: Minjie Zuo, 3/28/2026
# Serializers for the dadjokes app.

from rest_framework import serializers
from .models import Joke, Picture


class JokeSerializer(serializers.ModelSerializer):
    """Serializer for the Joke model."""

    class Meta:
        model = Joke
        fields = ['id', 'text', 'contributor', 'created_at']


class PictureSerializer(serializers.ModelSerializer):
    """Serializer for the Picture model."""

    class Meta:
        model = Picture
        fields = ['id', 'image_url', 'contributor', 'created_at']