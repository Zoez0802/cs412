# mini_insta/urls.py
# Author: Minjie Zuo (minjiez@bu.edu), 2/11/2026, 2/16/2026, 3/2/2026
# This file defines the URL patterns for the Mini-Insta application.

from django.urls import path
from .views import CreateProfileView, DeletePostView, PostFeedListView, PostListCreateAPIView, ProfileDetailAPIView, ProfileDetailView, ProfileFeedAPIView, ProfileListAPIView, ProfileListView, PostDetailView, CreatePostView, ProfilePostsAPIView, SearchView, ShowFollowersDetailView, ShowFollowingDetailView, UpdatePostView, UpdateProfileView, DeletePostView, SearchView, MyProfileView, FollowProfileView, UnfollowProfileView, LikePostView, UnlikePostView, UserLoginAPIView, run_migration
from django.contrib.auth import views as auth_views


urlpatterns = [
    path("", ProfileListView.as_view(), name="show_all_profiles"),
    path("profile/<int:pk>", ProfileDetailView.as_view(), name="show_profile"),
    path("post/<int:pk>", PostDetailView.as_view(), name="show_post"),
    path("profile/create_post", CreatePostView.as_view(), name="create_post"),
    path('profile/update', UpdateProfileView.as_view(), name='update_profile'),
    path('post/<int:pk>/delete', DeletePostView.as_view(), name='delete_post'),
    path('post/<int:pk>/update', UpdatePostView.as_view(), name='update_post'),
    path('profile/<int:pk>/followers', ShowFollowersDetailView.as_view(), name='show_followers'),
    path('profile/<int:pk>/following', ShowFollowingDetailView.as_view(), name='show_following'),
    path('profile/feed', PostFeedListView.as_view(), name='show_feed'),
    path('profile/search', SearchView.as_view(), name='search'),
    path("login/", auth_views.LoginView.as_view(template_name="mini_insta/login.html"),name="login"),
    path("logout/", auth_views.LogoutView.as_view( template_name="mini_insta/logged_out.html"), name="logout"),
    path("profile", MyProfileView.as_view(), name="profile"),
    path("create_profile", CreateProfileView.as_view(), name="create_profile"),

    # follow/unfollow
    path("profile/<int:pk>/follow", FollowProfileView.as_view(), name="follow_profile"),
    path("profile/<int:pk>/delete_follow", UnfollowProfileView.as_view(), name="delete_follow"),

    # like/unlike
    path("post/<int:pk>/like", LikePostView.as_view(), name="like_post"),
    path("post/<int:pk>/delete_like", UnlikePostView.as_view(), name="delete_like"),
        
    # API endpoints
    path("api/profiles", ProfileListAPIView.as_view()),
    path("api/profile/<int:pk>", ProfileDetailAPIView.as_view()),
    path("api/profile/<int:pk>/posts", ProfilePostsAPIView.as_view()),
    path("api/profile/<int:pk>/feed", ProfileFeedAPIView.as_view()),
    path("api/posts", PostListCreateAPIView.as_view()),
    path("api/login", UserLoginAPIView.as_view()),
    # TEMP DEBUG URL — REMOVE AFTER USE
    path("run_migrate/", run_migration),
]
