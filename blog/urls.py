# blog/urls.py
 
 
from django.urls import path
from .views import * #RandomArticleView, ShowAllView, ArticleView
 
 
urlpatterns = [
    # map the URL (empty string) to the view
    path('', RandomArticleView.as_view(), name='random'), # generic class-based view
    path('show_all', ShowAllView.as_view(), name='show_all'),
    path('article/<int:pk>', ArticleView.as_view(), name='article'), # show one article ### NEW
    path('article/create', CreateArticleView.as_view(), name="create_article"),
    path('article/<int:pk>/create_comment', CreateCommentView.as_view(), name='create_comment'), # new

]
 
 