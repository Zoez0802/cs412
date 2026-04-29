# project/models.py
# Author: Minjie Zuo , 4/16/2026-4/18/2026
# This file defines the database models for the restaurant review and recommendation app.
# Final project for CS 412, Spring 2026.

from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

class Restaurant(models.Model):

    # Define choices for area, cuisine, and price level fields
    # use option so later i can develop the filter function based on these fields
    AREA_CHOICES = [
        ("Allston", "Allston"),
        ("Fenway", "Fenway"),
        ("Kenmore", "Kenmore"),
        ("Brookline", "Brookline"),
    ]

    CUISINE_CHOICES = [
        ("American", "American"),
        ("Chinese", "Chinese"),
        ("Japanese", "Japanese"),
        ("Korean", "Korean"),
        ("Thai", "Thai"),
        ("Vietnamese", "Vietnamese"),
        ("Italian", "Italian"),
        ("Mexican", "Mexican"),
        ("Other", "Other"),
    ]

    PRICE_CHOICES = [
        ("$", "$"),
        ("$$", "$$"),
        ("$$$", "$$$"),
    ]

    #basic resturant information
    name = models.TextField(blank=False)
    street_address = models.TextField(blank=False)
    area = models.CharField(max_length=20, choices=AREA_CHOICES)
    cuisine = models.CharField(max_length=20, choices=CUISINE_CHOICES)
    price_level = models.CharField(max_length=10, choices=PRICE_CHOICES)
    description = models.TextField(blank=True)
    image_file = models.ImageField(blank=True)

    #Used for map visualization (stretch feature)
    # These are optional because we may not always find coordinates
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

    def __str__(self):
        """Return restaurant name for admin display."""
        return self.name


    def get_all_reviews(self):
        '''Return all reviews for this restaurant.'''
        return Review.objects.filter(restaurant=self).order_by("-created_at")

    def get_all_favorites(self):
        '''Return all favorites for this restaurant.'''
        return Favorite.objects.filter(restaurant=self).order_by("-created_at")


    def get_average_rating(self):
        '''Return the average rating for this restaurant, or None if there are no reviews.'''
        reviews = self.get_all_reviews()

        if reviews.count() == 0:
            return None

        total = 0
        for review in reviews:
            total += review.rating

        return total / reviews.count()

    def get_num_reviews(self):
        '''Return the number of reviews for this restaurant.'''
        return Review.objects.filter(restaurant=self).count()

    def get_num_favorites(self):
        '''Return the number of favorites for this restaurant.'''
        return Favorite.objects.filter(restaurant=self).count()


    def get_absolute_url(self):
        """Return the URL to display this restaurant."""
        return  reverse("show_restaurant", kwargs={"pk": self.pk})


class Profile(models.Model):
    """store user profile information, including the user account, display name, and bio text."""

    #Link each profile to a Django user account
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="project_profiles")
    #infos
    display_name = models.TextField(blank=False)
    bio_text = models.TextField(blank=True)
    profile_image = models.ImageField(blank=True)

    def __str__(self):
        """Return a string representation of this profile."""
        return self.display_name

    def get_all_reviews(self):
        '''Return all reviews written by this profile.'''
        return Review.objects.filter(profile=self).order_by("-created_at")


    def get_num_reviews(self):
        '''Return the number of reviews written by this profile.'''
        return Review.objects.filter(profile=self).count()
    
    def get_all_favorites(self):
        """Return all favorites restaurants created by this profile."""
        return Favorite.objects.filter(profile=self).order_by("-created_at")


    def get_absolute_url(self):
        """Return the URL to display this profile."""
        return reverse("show_profile", kwargs={"pk": self.pk})
    
    def get_num_favorites(self):
        '''Return the number of favorite restaurants saved by this profile.'''
        return Favorite.objects.filter(profile=self).count()


class Review(models.Model):
    """Store one review for a restaurant by a single user."""
    # Relationships
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    # let users write reviews with a rating and optional comment text
    rating = models.IntegerField()
    comment_text = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return a string representation of this review."""
        return f'{self.profile.display_name} review for {self.restaurant.name}'

    def get_all_photos(self):
        """Return all uploaded photos for this review."""
        return ReviewPhoto.objects.filter(review=self)
    
    def get_num_likes(self):
        """Return the number of likes for this review."""
        return ReviewLike.objects.filter(review=self).count()

# This model is used to store photos uploaded by users for their reviews. 
# Each photo is linked to a specific review, and we can have multiple photos for one review. 
# The image_file field is used to store the actual image file, and it is required (blank=False). 
class ReviewPhoto(models.Model):
    """Store one uploaded image that belongs to a review."""

    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    image_file = models.ImageField(blank=False)

    def __str__(self):
        """Return a string representation of this review photo."""
        return f'Photo for review {self.review.pk}'


class Favorite(models.Model):
    """Store one favorite relationship between a profile and a restaurant."""

    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)#timestamps

    def __str__(self):
        """Return a string representation of this favorite."""
        return f'{self.profile.display_name} favorites {self.restaurant.name}'


#create a new feature to allow user add resturant to custom folders, and each folder can have multiple restaurants.
class RestaurantFolder(models.Model):
    """Store one custom restaurant folder created by a user."""

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    name = models.CharField(max_length=80)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.profile.display_name} folder: {self.name}'

    def get_all_items(self):
        """Return all restaurants saved inside this folder."""
        return FolderItem.objects.filter(folder=self).order_by("-created_at")


class FolderItem(models.Model):
    """Store one restaurant inside one custom folder."""

    folder = models.ForeignKey(RestaurantFolder, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.restaurant.name} in {self.folder.name}'
    


class ReviewLike(models.Model):
    """Store one like from one profile on one review."""

    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.profile.display_name} likes review {self.review.pk}'
    