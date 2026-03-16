# File: urls.py
# Author: Minjie Zuo (minjiez@bu.edu), 3/16/2026
# Description: URL patterns for the voter_analytics application.

from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.VotersListView.as_view(), name='voters'),
    path('voter/<int:pk>', views.VoterDetailView.as_view(), name='voter'),
]