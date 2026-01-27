from django.urls import path
from django.conf import settings
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    path("", views.quote, name="home"),          #/home
    path("quote/", views.quote, name="quote"),         #/quote
    path("show_all/", views.show_all, name="show_all"),#/show_all
    path("about/", views.about, name="about"),         #/about
]+static (settings.STATIC_URL, document_root=settings.STATIC_ROOT)