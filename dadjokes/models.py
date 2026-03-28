# dadjokes/models.py
# Author: Minjie Zuo, 3/28/2026
# This file defines the data models for the dadjokes app.

from django.db import models

# This app will have 2 data models:
#Joke, which will store a joke, contributor, and the timestamp of when it was created.
#Picture, which will store the image_url, contributor name and timesamp

class Joke(models.Model):
    text = models.TextField()
    contributor = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text[:50]


class Picture(models.Model):
    image_url = models.URLField()
    contributor = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.image_url