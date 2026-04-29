# project/urls.py
# Author: Minjie Zuo , 4/16/2026
# This file defines the URL patterns for the restaurant review and recommendation app.
# Final project for CS 412, Spring 2026.
from django.urls import path
from django.contrib.auth import views as auth_views

from formdata import views

from .views import (
    AddToFolderView,
    DeleteReviewView,
    RestaurantListView,
    RestaurantDetailView,
    MyProfileView,
    CreateProfileView,
    ToggleReviewLikeView,
    UpdateProfileView,
    CreateReviewView,
    AddFavoriteView,
    RemoveFavoriteView,
    ProfileDetailView,
)

urlpatterns = [
    path("", RestaurantListView.as_view(), name="show_all_restaurants"),
    path("restaurant/<int:pk>", RestaurantDetailView.as_view(), name="show_restaurant"),
    path("restaurant/<int:pk>/review", CreateReviewView.as_view(), name="create_review"),
    path("restaurant/<int:pk>/favorite", AddFavoriteView.as_view(), name="add_favorite"),
    path("restaurant/<int:pk>/unfavorite", RemoveFavoriteView.as_view(), name="remove_favorite"),

    #for profile related
    path("profile", MyProfileView.as_view(), name="show_profile"),
    path("profile/<int:pk>/", ProfileDetailView.as_view(), name="show_other_profile"),
    path("profile/create", CreateProfileView.as_view(), name="create_profile"),
    path("profile/update", UpdateProfileView.as_view(), name="update_profile"),

    #login and logout
    path("login/", auth_views.LoginView.as_view(template_name="project/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(template_name="project/logged_out.html"), name="logout"),

    # when user creating a restaurant folder, the form will be submitted to this url
    path("restaurant/<int:pk>/folder/", AddToFolderView.as_view(), name="add_to_folder"),
    # this url is for when user clicks the like button for a review, it will send a POST request to this url to toggle the like status
    path("review/<int:pk>/like/", ToggleReviewLikeView.as_view(), name="toggle_review_like"),
    #user delete review
    path("review/<int:pk>/delete/", DeleteReviewView.as_view(), name="delete_review"),
]
