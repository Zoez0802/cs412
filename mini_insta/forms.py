"""
Author: Minjie Zuo (minjiez@bu.edu), 2/19/2026
This file defines ModelForms for the Mini-Insta app.
"""
from django import forms
from .models import *


class CreatePostForm(forms.ModelForm):
    """Form used to create a new Post object.This form is connected to the Post model."""
    class Meta:
        model = Post
        fields = ['caption']


class UpdateProfileForm(forms.ModelForm):
    '''Form to update an existing Profile.'''

    class Meta:
        model = Profile
        fields = ['display_name', 'profile_image_url', 'bio_text']