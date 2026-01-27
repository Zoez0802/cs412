# files: hw/views.py
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
 
 
# Create your views here.
 
import time
import random

#two Python lists in the global scope of the views.py file
# add some quote for the famous person that i chosen, Steve Jobs
# 3 quotes
quotes = [
    "Stay hungry, stay foolish.",
    "Innovation distinguishes between a leader and a follower.",
    "Your time is limited, so don’t waste it living someone else’s life."
]


#3 pics of SJ
images = [
    "https://img-cdn.inc.com/image/upload/f_webp,c_fit,w_1920,q_auto/images/panoramic/steve-jobs_521035_gqjw7g.jpg",
    "https://img-cdn.inc.com/image/upload/f_webp,c_fit,w_1920,q_auto/images/panoramic/GettyImages-115296994_531075_sy6nmm.jpg",
    "https://tse3.mm.bing.net/th/id/OIP.05tMe9Ec7Tyvp0f_jd_LywHaE8?rs=1&pid=ImgDetMain&o=7&rm=3",
] 

def home(request):
    return render(request, "hw/home.html")

#/quote : the same as /, to generate one quote and one image at random.
def quote(request):
    context = {
        "quote": random.choice(quotes),
        "image": random.choice(images),
    }
    return render(request, "hw/quote.html", context)

#/show_all : an ancillary page which will show all quotes and images.
def show_all(request):
    context = {
        "quotes": quotes,
        "images": images,
    }
    return render(request, "hw/show_all.html", context)

#/about : an about page with short biographical information about the person whose quotes
def about(request):
    return render(request, "hw/about.html")