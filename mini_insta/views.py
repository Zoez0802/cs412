# mini_insta/views.py
# Author: Minjie Zuo (minjiez@bu.edu), 2/11/2026 , 2/18/2026
# This file defines the class-based views for the Mini-Insta application.

from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView, UpdateView
from django.urls import reverse
from .models import Profile, Post, Photo
from .forms import CreatePostForm, UpdateProfileForm


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

        # get list of uploaded files
        # image_files = self.request.FILES.get('images')
        #if image_file:
            # Photo.objects.create(post=self.object, image_file=image_file)          

        # read uploaded files (0 to many)
        files = self.request.FILES.getlist('images')

        # create one Photo object per uploaded file
        for file in files:
            Photo.objects.create(post=self.object, image_file=file)

        return response
    
class UpdateProfileView(UpdateView):
    '''Display and process a form to update an existing Profile.'''

    model = Profile
    form_class = UpdateProfileForm
    template_name = "mini_insta/update_profile_form.html"


class DeletePostView(DeleteView):
    '''Display and process a form to delete an Post.'''

    model = Post
    template_name = "mini_insta/delete_post_form.html"

    def get_context_data(self, **kwargs):
        '''Add the Post and the Profile to the template context.'''
        context=super().get_context_data(**kwargs)

        post = self.get_object()
        context['post']= post
        context['profile'] =post.profile

        return context

    def get_success_url(self):
        '''Redirect to the Profile page after successful delete.'''
        post = self.get_object()
        return reverse('show_profile', kwargs={'pk': post.profile.pk})


class UpdatePostView(UpdateView):
    '''Display and process a form to update Post.'''

    model = Post
    fields = ['caption']
    template_name = "mini_insta/update_post_form.html"

    def get_success_url(self):
        '''Redirect back to the Post page after successful update.'''
        return reverse('show_post', kwargs={'pk': self.object.pk})
    
    def get_context_data(self, **kwargs):
        '''Add the Post to the template context.'''
        context = super().get_context_data(**kwargs)
        context['post'] = self.get_object()
        return context
    

class ShowFollowersDetailView(DetailView):
    '''Display the followers for one Profile.'''
    model = Profile
    template_name = "mini_insta/show_followers.html"
    context_object_name = "profile"


class ShowFollowingDetailView(DetailView):
    '''Display the profiles that this Profile is following.'''
    model = Profile
    template_name = "mini_insta/show_following.html"
    context_object_name = "profile"