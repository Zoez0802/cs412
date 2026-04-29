# project/forms.py
# Author: Minjie Zuo, 4/16/2026
# This file defines the forms for the restaurant review and recommendation app.

from django import forms
from .models import Profile, Review, RestaurantFolder

RATING_CHOICES = [
    (1, "1"),
    (2, "2"),
    (3, "3"),
    (4, "4"),
    (5, "5"),
]


class CreateProfileForm(forms.ModelForm):
    '''Form for creating a user profile.'''
    class Meta:
        model = Profile
        fields = ["display_name", "bio_text", "profile_image"]


class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["display_name", "bio_text", "profile_image"]


class CreateReviewForm(forms.ModelForm):
    '''Form for creating a restaurant review.'''
    rating = forms.ChoiceField(choices=RATING_CHOICES)

    class Meta:
        model = Review
        fields = ["rating", "comment_text"]
        # Customize the comment_text field to use a textarea with more rows and a placeholder.
        widgets = {
            "comment_text": forms.Textarea(attrs={
                "rows": 5,
                "placeholder": "Share your experience at this restaurant..."
            }),
        }

    def clean_rating(self):
        return int(self.cleaned_data["rating"])
    

#form for creating and updating restaurant folders
class CreateFolderForm(forms.ModelForm):
    '''Form for creating a restaurant folder.'''
    name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            "placeholder": "Example: Date night, Cheap eats, Study spots..."
        })
    )

    class Meta:
        model = RestaurantFolder
        fields = ["name"]