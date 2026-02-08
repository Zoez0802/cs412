## Create View
# blog/views.py
# Define the views for the blog app:
 
 
from django.shortcuts import render
from .models import Article
from django.views.generic import ListView, DetailView
import random
 
 
class ShowAllView(ListView):
    '''Create a subclass of ListView to display all blog articles.'''
 
 
    model = Article # retrieve objects of type Article from the database
    template_name = 'blog/show_all.html'
    context_object_name = 'articles' # how to find the data in the template file
 
class ArticleView(DetailView):
    '''Show the details for one article.'''
    model = Article
    template_name = 'blog/article.html' ## reusing same template!!
    context_object_name = 'article'


class RandomArticleView(DetailView):
    '''Show the details for one random article.'''
    model = Article
    template_name = 'blog/article.html' ## reusing same template!!
    context_object_name = 'article'

    def get_object(self):
        '''Override the default get_object() method to return a random article.'''
        all_articles = Article.objects.all()
        return random.choice(all_articles)