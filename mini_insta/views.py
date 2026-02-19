# mini_insta/views.py
# Author: Minjie Zuo (minjiez@bu.edu), 2/11/2026 , 2/18/2026
# This file defines the class-based views for the Mini-Insta application.

from django.views.generic import DetailView, ListView, CreateView
from django.urls import reverse
from .models import Profile, Post, Photo
from .forms import CreatePostForm


class ProfileListView(ListView):
    """Display a page that lists all Profile objects."""
    model = Profile
    template_name = "mini_insta/show_all_profiles.html"
    context_object_name = "profiles"

class ProfileDetailView(DetailView):
    """Display a page for one Profile selected by its primary key."""
    model = Profile
    template_name = "mini_insta/show_profile.html"
    context_object_name = "profile"

class PostDetailView(DetailView):
    """Display a single Post object, including its Photos."""
    model = Post
    template_name = "mini_insta/show_post.html"
    context_object_name = "post"


class CreatePostView(CreateView):
    '''Display and process the form to create a new Post for a given Profile.'''

    model = Post
    form_class = CreatePostForm
    template_name = "mini_insta/create_post_form.html"

    def get_context_data(self, **kwargs):
        '''Add the Profile to the template context so the template can build URLs.'''
        context = super().get_context_data(**kwargs)

        profile_pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=profile_pk)

        context['profile'] = profile
        return context

    def form_valid(self, form):
        '''Attach the Profile FK to the new Post, then create exactly one Photo using image_url from the submitted HTML form field.'''
        profile_pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=profile_pk)
        form.instance.profile = profile # attach FK before saving

        response = super().form_valid(form)

        #create the Photo for that Post (if user provided an image URL)
        image_url = self.request.POST.get('image_url', '').strip()
        if image_url != "":
            Photo.objects.create(post=self.object, image_url=image_url)

        return response
