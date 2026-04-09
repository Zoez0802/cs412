# mini_insta/serializers.py
# Author: Minjie Zuo (minjiez@bu.edu), 4/6/2026
# Serializers for the mini_insta REST API. These serializers convert model instances to JSON format and validate incoming data for creating new posts.

from rest_framework import serializers
from .models import Profile, Post, Photo

# Serializers for the REST API endpoints. These are used to convert model instances to JSON format and to validate incoming data for creating new posts.
class ProfileSerializer(serializers.ModelSerializer):
    """serializer for Profile"""

    class Meta:
        model = Profile
        fields = ['id', 'username', 'display_name', 'profile_image_url', 'bio_text']


class PhotoSerializer(serializers.ModelSerializer):
    """Serialize one photo"""

    image = serializers.SerializerMethodField()

    class Meta:
        model = Photo
        fields = ['id', 'image']

    def get_image(self, obj):
        # use helper function
        return obj.get_image_url()


class PostSerializer(serializers.ModelSerializer):
    """Serialize post and its photos"""

    photos = serializers.SerializerMethodField() #get all photos for this post and serialize them
    profile = ProfileSerializer(read_only=True)#nested serializer to show profile info in post
    class Meta:
        model = Post
        fields = ['id', 'profile', 'caption', 'timestamp', 'photos']

    def get_photos(self, obj):
        photos = obj.get_all_photos()
        return PhotoSerializer(photos, many=True).data


class CreatePostSerializer(serializers.ModelSerializer):
    """Serializer for creating a new post. It accepts an optional image_url field for convenience, which will create a Photo if provided."""

    image_url = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = Post
        fields = ['caption', 'image_url']

    def create(self, validated_data):
        image_url = validated_data.pop('image_url', '')

        post = Post.objects.create(**validated_data)

        # if user provided an image_url, create a Photo
        if image_url:
            Photo.objects.create(post=post, image_url=image_url)

        return post