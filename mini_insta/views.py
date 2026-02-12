# mini_insta/views.py
# Author: Minjie Zuo (minjiez@bu.edu), 2/11/2026
# This file defines the class-based views for the Mini-Insta application.

from django.views.generic import ListView, DetailView
from .models import Profile

class ProfileListView(ListView):
    """Display a page that lists all Profile objects."""
    model = Profile
    template_name = "mini_insta/show_all_profiles.html"
    context_object_name = "profiles"

class ProfileDetailView(DetailView):
    """Display a page for one Profile selected by its primary key."""
    model = Profile
    template_name = "mini_insta/show_profile.html"
    context_object_name = "profile"