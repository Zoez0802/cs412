# mini_insta/urls.py
# This file defines the URL patterns for the Mini-Insta application.

from django.urls import path
from .views import ProfileDetailView, ProfileListView

urlpatterns = [
    path("", ProfileListView.as_view(), name="show_all_profiles"),
    path("profile/<int:pk>", ProfileDetailView.as_view(), name="show_profile"),
]
