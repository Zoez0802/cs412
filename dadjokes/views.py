# dadjokes/views.py
# Author: Minjie Zuo, 3/28/2026
# Views for the dadjokes app.


import random
from django.shortcuts import render
from .models import *

#API imports
from rest_framework import generics
from rest_framework.response import Response
from .serializers import *


def home(request):
    """Show one random joke and one random picture."""
    jokes = Joke.objects.all()
    pictures = Picture.objects.all()

    random_joke = random.choice(jokes) if jokes else None
    random_picture = random.choice(pictures) if pictures else None

    context = {
        "joke": random_joke,
        "picture": random_picture,
    }
    return render(request, "dadjokes/home.html", context)


def random_page(request):
    """Show one random joke and one random picture."""
    jokes = Joke.objects.all()
    pictures = Picture.objects.all()

    random_joke = random.choice(jokes) if jokes else None
    random_picture = random.choice(pictures) if pictures else None

    context = {
        "joke": random_joke,
        "picture": random_picture,
    }
    return render(request, "dadjokes/home.html", context)


def show_all_jokes(request):
    """Show all jokes."""
    jokes = Joke.objects.all().order_by("-created_at")

    context = {
        "jokes": jokes,
    }
    return render(request, "dadjokes/show_all_jokes.html", context)


def show_joke(request, pk):
    """Show one joke by primary key."""
    joke = get_object_or_404(Joke, pk=pk)

    context = {
        "joke": joke,
    }
    return render(request, "dadjokes/show_joke.html", context)


def show_all_pictures(request):
    """Show all pictures."""
    pictures = Picture.objects.all().order_by("-created_at")

    context = {
        "pictures": pictures,
    }
    return render(request, "dadjokes/show_all_pictures.html", context)


def show_picture(request, pk):
    """Show one picture by primary key."""
    picture = get_object_or_404(Picture, pk=pk)

    context = {
        "picture": picture,
    }
    return render(request, "dadjokes/show_picture.html", context)

#API views
class JokeListAPIView(generics.ListCreateAPIView):
    '''
    An API view to return a listing of Jokes
    and to create a Joke.
    '''
    queryset = Joke.objects.all()
    serializer_class = JokeSerializer


class JokeDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Joke.objects.all()
    serializer_class = JokeSerializer


class PictureListAPIView(generics.ListCreateAPIView):
    '''
    An API view to return a listing of Pictures.
    '''
    queryset = Picture.objects.all()
    serializer_class = PictureSerializer


class PictureDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Picture.objects.all()
    serializer_class = PictureSerializer


class RandomJokeAPIView(generics.ListCreateAPIView):
    '''
    Return one Joke selected at random.
    '''
    queryset = Joke.objects.all()
    serializer_class = JokeSerializer

    def get(self, request):
        jokes = Joke.objects.all()
        joke = random.choice(jokes)
        serializer = JokeSerializer(joke)
        return Response(serializer.data)


class RandomPictureAPIView(generics.ListCreateAPIView):
    '''
    Return one Picture selected at random.
    '''
    queryset = Picture.objects.all()
    serializer_class = PictureSerializer

    def get(self, request):
        pictures = Picture.objects.all()
        picture = random.choice(pictures)
        serializer = PictureSerializer(picture)
        return Response(serializer.data)
