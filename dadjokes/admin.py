# dadjokes/admin.py
# Author: Minjie Zuo, 3/28/2026
# This file registers the data models for the dadjokes app with the Django admin site.


from django.contrib import admin
from .models import Joke, Picture

admin.site.register(Joke)
admin.site.register(Picture)