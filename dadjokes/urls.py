# dadjokes/urls.py
# author: Minjie Zuo, 3/28/2026
# URL patterns for the dadjokes app.

from django.urls import path
from .views import *

urlpatterns = [
    path("", home, name="home"),
    path("random", random_page, name="random"),
    path("jokes", show_all_jokes, name="show_all_jokes"),
    path("joke/<int:pk>", show_joke, name="show_joke"),
    path("pictures", show_all_pictures, name="show_all_pictures"),
    path("picture/<int:pk>", show_picture, name="show_picture"),
#api
    path('api/', RandomJokeAPIView.as_view()),
    path('api/random', RandomJokeAPIView.as_view()),
    path('api/random_picture', RandomPictureAPIView.as_view()),
    path('api/jokes', JokeListAPIView.as_view()),
    path('api/joke/<int:pk>', JokeDetailAPIView.as_view()),
    path('api/pictures', PictureListAPIView.as_view()),
    path('api/picture/<int:pk>', PictureDetailAPIView.as_view()),
]


