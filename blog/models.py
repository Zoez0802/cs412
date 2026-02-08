## Create a Model 
#
# blog/models.py
# Define the data objects for our application
#
from django.db import models
 
 
class Article(models.Model):
    '''Encapsulate the idea of an Article by some author.'''
 
 
    # data attributes of a Article object:
    title = models.TextField(blank=True)
    author = models.TextField(blank=True)
    text = models.TextField(blank=True)
    published = models.DateTimeField(auto_now=True)
    image_url = models.URLField(blank=True) ## new
    
    def __str__(self):
        '''Return a string representation of this Article object.'''
        return f'{self.title} by {self.author}'
 