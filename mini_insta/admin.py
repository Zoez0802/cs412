# mini_insta/admin.py
# This file registers the Profile model with the Django admin site,
# allowing profiles to be managed through the admin interface.


from django.contrib import admin
from .models import Profile

admin.site.register(Profile)
