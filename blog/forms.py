# blog/forms.py
from django import forms
from .models import Comment, Article
 
 

class CreateArticleForm(forms.ModelForm):
    """A form to add an Article to the database."""

    class Meta:
        """Associate this form with the Article model."""
        model = Article
        fields = ["author", "title", "text", "image_file"]

class UpdateArticleForm(forms.ModelForm):
    '''A form to update a quote to the database.'''
 
    class Meta:
        '''associate this form with the Article model.'''
        model = Article
        fields = ['title', 'text', ]  # which fields from model should we use


class CreateCommentForm(forms.ModelForm):
    '''A form to add a Comment to the database.'''
 
    class Meta:
            '''Associate this form with the Article model; select fields to add.'''
            model = Comment
            # fields = ['author', 'title', 'text', 'image_url']
            fields = ['author', 'text']
            
    
 
