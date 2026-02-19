# mini_insta/admin.py
# Author: Minjie Zuo (minjiez@bu.edu), 2/11/2026
# This file registers the Profile model with the Django admin site,
# allowing profiles to be managed through the admin interface.


from django.contrib import admin
from .models import Profile, Post, Photo

admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Photo)