# mini_insta/views.py
# Author: Minjie Zuo (minjiez@bu.edu), 2/11/2026 , 2/18/2026
# This file defines the class-based views for the Mini-Insta application.

from urllib import request, response, response

from django.views.generic import DetailView, ListView, CreateView, TemplateView, UpdateView, DeleteView, UpdateView, CreateView
from django.urls import reverse
from .models import Profile, Post, Photo, Follow, Like
from .forms import CreatePostForm, UpdateProfileForm, CreateProfileForm
from django.shortcuts import redirect, render #added for task 3 - a5
from django.contrib.auth.mixins import LoginRequiredMixin  # NEW
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login

#imports for API
from rest_framework import generics
from rest_framework.response import Response
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        other = self.get_object()
        me = None

        if self.request.user.is_authenticated:
            me = Profile.objects.filter(user=self.request.user).first()

        # default: cannot follow
        context["can_follow"] = False
        context["is_following"] = False

        # only allow follow if logged-in user has a profile AND it's not their own page
        if me is not None and me.pk != other.pk:
            context["can_follow"] = True
            context["is_following"] = Follow.objects.filter(profile=other,follower_profile=me).exists()

        return context

class PostDetailView(DetailView):
    """Display a single Post object, including its Photos."""
    model = Post
    template_name = "mini_insta/show_post.html"
    context_object_name = "post"
    

    # Add the Profile to the context so base.html can render the navigation.
    # I want user to be able to cancel their action on update or delete post.
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        post = self.get_object()

        if self.request.user.is_authenticated:
            me = Profile.objects.filter(user=self.request.user).first()

            if me is not None and post.profile.pk != me.pk:
                context["can_like"] = True
                context["is_liked"] = Like.objects.filter(post=post, profile=me).exists()
            else:
                context["can_like"] = False
                context["is_liked"] = False
        else:
            context["can_like"] = False
            context["is_liked"] = False

        return context

class CreatePostView(LoginRequiredMixin, CreateView):
    '''Display and process the form to create a new Post for a given Profile.'''

    model = Post
    form_class = CreatePostForm
    template_name = "mini_insta/create_post_form.html"

    def get_context_data(self, **kwargs):
        '''Add the Profile to the template context so the template can build URLs.'''
        context = super().get_context_data(**kwargs)
        profile = Profile.objects.filter(user=self.request.user).first()
        context['profile'] = profile
        return context

    def form_valid(self, form):
        '''Attach the Profile FK to the new Post, then create exactly one Photo using image_url from the submitted HTML form field.'''
        profile = Profile.objects.filter(user=self.request.user).first()

        if profile.user != self.request.user:
            return super().get(self.request) 
        
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

    def get_success_url(self):
        return reverse('profile')
    
    def get_login_url(self):
        return reverse('login')
        
class UpdateProfileView(LoginRequiredMixin, UpdateView):
    '''Display and process a form to update an existing Profile.'''

    model= Profile
    form_class = UpdateProfileForm
    template_name = "mini_insta/update_profile_form.html"

    def get_object(self):
        return Profile.objects.filter(user=self.request.user).first()

    def get_login_url(self):
        return reverse('login')

class DeletePostView(LoginRequiredMixin, DeleteView):
    '''Display and process a form to delete an Post.'''

    model = Post
    template_name = "mini_insta/delete_post_form.html"

    def get_context_data(self, **kwargs):
        '''Add the Post and the Profile to the template context.'''
        context=super().get_context_data(**kwargs)

        post =self.get_object()
        context['post']= post
        context['profile'] =post.profile

        return context

    def get_success_url(self):
        '''Redirect to the Profile page after successful delete.'''
        post = self.get_object()
        return reverse('show_profile', kwargs={'pk': post.profile.pk})
    
    def dispatch(self, request, *args, **kwargs):
        post = Post.objects.get(pk=kwargs["pk"])

        # if user not owner → redirect to login
        if post.profile.user != request.user:
            return redirect("login")

        return super().dispatch(request, *args, **kwargs)

    def get_login_url(self):
        return reverse('login')

class UpdatePostView(LoginRequiredMixin, UpdateView):
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
    
    def dispatch(self, request, *args, **kwargs):
        post = Post.objects.get(pk=kwargs["pk"])

        # if user not owner → redirect to login
        if post.profile.user != request.user:
            return redirect("login")

        return super().dispatch(request, *args, **kwargs)
        
    def get_login_url(self):
        return reverse('login')


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


class PostFeedListView(LoginRequiredMixin, ListView):
    '''Display a feed of Posts for one Profile.'''

    template_name = "mini_insta/show_feed.html"
    context_object_name = "posts"

    def get_queryset(self):
        profile = Profile.objects.filter(user=self.request.user).first()
        # Only owner can view feed
        if profile.user != self.request.user:
            return Post.objects.none()

        return profile.get_post_feed()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = Profile.objects.filter(user=self.request.user).first()
        context['profile'] = profile
        return context
    
    def get_login_url(self):
        return reverse("login")

    
#for task 3 -a5
class SearchView(LoginRequiredMixin, ListView):
    template_name = "mini_insta/search_results.html"


    def dispatch(self, request, *args, **kwargs):

        # let LoginRequiredMixin run first
        response = super().dispatch(request, *args, **kwargs)

        # if user was not authenticated, mixin already redirected
        if not request.user.is_authenticated:
            return response

        profile = Profile.objects.filter(user=request.user).first()
        # 如果没有 query，就显示 search 
        # if there is no "query" in the GET parameters, render the search page instead of performing a search
        if "query" not in request.GET:
            return render(request, "mini_insta/search.html", {"profile": profile})

        return response
    
    def get_login_url(self):
        return reverse("login")

    


    def get_queryset(self):
        query = self.request.GET.get("query", "")
        return Post.objects.filter(caption__icontains=query)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = Profile.objects.filter(user=self.request.user).first()
        query = self.request.GET.get("query", "")
        posts = self.get_queryset()

        profiles = []
        all_profiles = Profile.objects.all()
        for p in all_profiles: #for all possiblitiy, if the query is in the username, display name, or bio text, add to the list of profiles to display
            if query.lower() in p.username.lower() or query.lower() in p.display_name.lower() or query.lower() in p.bio_text.lower():
                profiles.append(p)
        
        context["profiles"] = profiles
        context["profile"] = profile
        context["query"] = query
        context["posts"] = posts
        return context
    

class MyProfileView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = "mini_insta/show_profile.html"
    context_object_name = "profile"

    def get_object(self):
        # FK -> could be multiple for admin, testing should use non-admin user
        return Profile.objects.filter(user=self.request.user).first()



class CreateProfileView(CreateView):
    """Create a new User and a Profile together (two forms, one submit)."""

    model = Profile
    form_class = CreateProfileForm
    template_name = "mini_insta/create_profile_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # If we already passed a bound user_form, keep it.
        if "user_form" in kwargs:
            context["user_form"] = kwargs["user_form"]
        else:
            context["user_form"] = UserCreationForm(prefix="user")

        return context

    def form_valid(self, form):
        # Build the bound user form using the same POST data
        user_form = UserCreationForm(self.request.POST, prefix="user")

        # If user form is invalid, re-render page with BOTH forms
        if not user_form.is_valid():
            return self.render_to_response(self.get_context_data(form=form, user_form=user_form))

        new_user = user_form.save()
        login(self.request, new_user) # log in the new user immediately after signing up，use login()to log the user, provided by
        form.instance.user = new_user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("profile")
    

#Follow and Unfollow user's profile
class FollowProfileView(LoginRequiredMixin, TemplateView):
    """Logged-in user's Profile can follows another Profile ."""

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        if not request.user.is_authenticated:
            return response

        # Only allow POST to modify DB
        if request.method == "POST":
            me = Profile.objects.filter(user=request.user).first()
            other = Profile.objects.get(pk=self.kwargs["pk"])

            # cannot follow yourself
            if me and me.pk != other.pk:
                Follow.objects.get_or_create(profile=other, follower_profile=me)
        
        request.method = "GET" # i fixed the bug that after following, it redirects to the profile page but the method is still POST, which causes error because the profile page only accepts GET. By changing the method to GET before calling the detail view, we can fix this issue.
        # return the profile page
        return ProfileDetailView.as_view()(request, pk=self.kwargs["pk"])
    
    def get_login_url(self):
        return reverse('login')
    

class UnfollowProfileView(LoginRequiredMixin, TemplateView):
    """Logged-in user's Profile unfollows another Profile."""

    def dispatch(self, request, *args, **kwargs):
        r= super().dispatch(request, *args, **kwargs)
        if not request.user.is_authenticated:
            return r

        if request.method == "POST":
            me = Profile.objects.filter(user=request.user).first()
            other = Profile.objects.get(pk=self.kwargs["pk"])

            if me and me.pk != other.pk:
                Follow.objects.filter(profile=other, follower_profile=me).delete()
        request.method = "GET"
        return ProfileDetailView.as_view()(request, pk=self.kwargs["pk"])
    
    def get_login_url(self):
        return reverse('login')
    

#Like and Unlike a post
class LikePostView(LoginRequiredMixin, TemplateView):
    """Logged-in user's Profile likes a Post"""

    def post(self, request, *args, **kwargs):
        me = Profile.objects.filter(user=request.user).first()
        p_obj = Post.objects.get(pk=self.kwargs["pk"])

        if me and p_obj.profile.pk != me.pk:
            Like.objects.get_or_create(post=p_obj, profile=me)

        request.method = "GET" #IMPORTANT: call the detail view as GET
        return PostDetailView.as_view()(request, pk=p_obj.pk)
    
    def get_login_url(self):
        return reverse('login')
    
class UnlikePostView(LoginRequiredMixin, TemplateView):
    """Logged-in user's Profile removes like from a Post"""

    def post(self, request, *args, **kwargs):
        me = Profile.objects.filter(user=request.user).first()
        p_obj = Post.objects.get(pk=self.kwargs["pk"])

        if me and p_obj.profile.pk != me.pk:
            Like.objects.filter(post=p_obj, profile=me).delete()

        request.method = "GET"
        return PostDetailView.as_view()(request, pk=p_obj.pk)
    
    def get_login_url(self):
        return reverse('login')
    

# views for API endpoints
class ProfileListAPIView(generics.ListAPIView):
    """Return all profiles."""
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    #update for authentication and permission
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]


class ProfileDetailAPIView(generics.RetrieveAPIView):
    """Return one profile by id."""
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    #update for authentication and permission
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]


class ProfilePostsAPIView(generics.ListAPIView):
    """Return all posts for one profile."""
    serializer_class = PostSerializer
    #update for authentication and permission
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        profile = Profile.objects.get(pk=self.kwargs["pk"])
        return profile.get_all_posts()   # already exists 


class ProfileFeedAPIView(generics.ListAPIView):
    """Return feed for one profile."""
    serializer_class = PostSerializer
    #update for authentication and permission
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        profile = Profile.objects.get(pk=self.kwargs["pk"])
        return profile.get_post_feed()  


class PostListCreateAPIView(generics.ListCreateAPIView):
    """Return all posts, or create a new post. For creating a new post, the request body should include the profile id and caption, and optionally an image url."""

    queryset = Post.objects.all()
    serializer_class = CreatePostSerializer
    #update for authentication and permission
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def perform_create(self, serializer):
        """Override perform_create to handle the creation of a new post with an optional image url. If image_url is provided in the request data, create a Photo object for the new post using that image url."""
        serializer.save()

#check user password
class UserLoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            profile = Profile.objects.filter(user=user).first()
            # if the authenticated user doesn't have a profile, return an error response
            if profile is None:
                return Response(
                    {'error': 'This user does not have a MiniInsta profile.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            token, created = Token.objects.get_or_create(user=user)

            # return the token and profile id in the response
            return Response({'token': token.key,'profile_id': profile.pk,},status=status.HTTP_200_OK)

        return Response({'error': 'Invalid Credentials'},status=status.HTTP_400_BAD_REQUEST)
