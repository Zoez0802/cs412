# mini_insta/views.py
# This file defines the class-based views for the Mini-Insta application.

from django.views.generic import ListView, DetailView
from .models import Profile

class ProfileListView(ListView):
    #Display all Profiles
    model = Profile
    template_name = "mini_insta/show_all_profiles.html"
    context_object_name = "profiles"

class ProfileDetailView(DetailView):
    model = Profile
    template_name = "mini_insta/show_profile.html"
    context_object_name = "profile"