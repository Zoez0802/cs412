# project/admin.py
# Author: Minjie Zuo
# Register models for the Django admin site.

from django.contrib import admin
from .models import Restaurant, Profile, Review, Favorite, ReviewPhoto

admin.site.register(Restaurant)
admin.site.register(Profile)
admin.site.register(Review)
admin.site.register(Favorite)
admin.site.register(ReviewPhoto)