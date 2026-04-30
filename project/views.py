# project/views.py
# Author: Minjie Zuo, 4/14/2026-4/18/2026
# Views for the restaurant review and recommendation app.

from django.views.generic import ListView, DetailView, CreateView, UpdateView, View
from django.urls import reverse
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.db.models import Avg, Count, Q, F
import random #for my random feature
#for my extended feature: trending restaurant
from django.utils import timezone 
from datetime import timedelta
# for my search engine
from difflib import SequenceMatcher

from .models import Restaurant, Profile, Favorite, Review, ReviewPhoto,RestaurantFolder, FolderItem,ReviewLike
from .forms import CreateProfileForm, UpdateProfileForm, CreateReviewForm, CreateFolderForm


class RestaurantListView(ListView):
    '''View for showing the list of all restaurants with optional filters.'''
    model = Restaurant
    template_name = "project/show_all_restaurants.html"
    context_object_name = "restaurants"


    # Override get_queryset to apply filters based on query parameters.
    def get_queryset(self):
        ''' Return the list of restaurants after applying search, filters, and sorting.
        Includes fuzzy search if no direct match is found.'''
        qs = Restaurant.objects.all()

        area = self.request.GET.get("area")
        cuisine = self.request.GET.get("cuisine")
        price = self.request.GET.get("price")
        sort = self.request.GET.get("sort")
        search = self.request.GET.get("q", "").strip() #search engine

        if search:
            # First try normal partial matching.
            direct_matches = qs.filter(name__icontains=search)

            if direct_matches.exists():
                qs = direct_matches
            else:
                # If no exact/partial match, try a simple fuzzy match.
                matched_ids = []

                for restaurant in qs:
                    restaurant_name = restaurant.name.lower()
                    search_text = search.lower()

                    score = SequenceMatcher(None, search_text, restaurant_name).ratio()

                    if score >= 0.55:
                        matched_ids.append(restaurant.id)

                qs = qs.filter(id__in=matched_ids)

        if area:
            qs = qs.filter(area=area)

        if cuisine:
            qs = qs.filter(cuisine=cuisine)

        if price:
            qs = qs.filter(price_level=price)

        # Add summary values so we can sort by them.
        qs = qs.annotate(
            avg_rating=Avg("review__rating"),
            review_count=Count("review")
        )

        # Apply sorting.
        if sort == "rating_high":
            qs = qs.order_by("-avg_rating", "-review_count", "name")
        elif sort == "rating_low":
            qs = qs.order_by("avg_rating", "-review_count", "name")
        elif sort == "reviews_high":
            qs = qs.order_by("-review_count", "-avg_rating", "name")
        elif sort == "reviews_low":
            qs = qs.order_by("review_count", "-avg_rating", "name")
        else:
            # Default order if user does not choose a sort option.
            qs = qs.order_by("name")

        return qs


    # Override get_context_data to pass the choices and selected filters to the template.
    def get_context_data(self, **kwargs):
        '''This method adds the filter choices and the currently selected filters to the context, so that the template can display them properly.'''
        context = super().get_context_data(**kwargs)

        context["area_choices"] = Restaurant.AREA_CHOICES
        context["cuisine_choices"] = Restaurant.CUISINE_CHOICES
        context["price_choices"] = Restaurant.PRICE_CHOICES

        context["selected_area"] = self.request.GET.get("area", "")
        context["selected_cuisine"] = self.request.GET.get("cuisine", "")
        context["selected_price"] = self.request.GET.get("price", "")
        context["selected_sort"] = self.request.GET.get("sort", "")

        # search engine
        context["selected_search"] = self.request.GET.get("q", "")

        # extend feature: random restaurant recommendation
        help_me_decide = self.request.GET.get("help_me_decide", "")
        context["help_me_decide"] = help_me_decide
        # favorite map feature
        context["favorite_ids"] = []

        if self.request.user.is_authenticated:
            profile = Profile.objects.filter(user=self.request.user).first()

            if profile:
                context["favorite_ids"] = list(
                    Favorite.objects.filter(profile=profile).values_list("restaurant_id", flat=True)
                )

        # recommendation: Help Me Decide
        context["recommended_restaurant"] = None

        if help_me_decide == "1":
            seen_ids = self.request.session.get("seen_recommendations", [])

            recommended_qs = self.get_queryset().filter(
                avg_rating__gte=4
            ).exclude(
                id__in=seen_ids
            )

            # If all 4+ restaurants have already been shown, restart the cycle.
            if not recommended_qs.exists():
                seen_ids = []
                recommended_qs = self.get_queryset().filter(avg_rating__gte=4)

            if recommended_qs.exists():
                recommended_restaurant = random.choice(list(recommended_qs))
                context["recommended_restaurant"] = recommended_restaurant

                seen_ids.append(recommended_restaurant.id)
                self.request.session["seen_recommendations"] = seen_ids


        # extended feature: Trending Now
        trending = self.request.GET.get("trending", "")
        context["trending"] = trending
        context["trending_restaurant"] = None
        context["trending_reviews"] = None
        context["trending_days"] = 7

        if trending == "1":
            days = 7
            start_date = timezone.now() - timedelta(days=days)

            trending_qs = Restaurant.objects.annotate(
                avg_rating=Avg("review__rating"),
                recent_review_count=Count(
                    "review",
                    filter=Q(review__created_at__gte=start_date),
                    distinct=True
                ),
                recent_favorite_count=Count(
                    "favorite",
                    filter=Q(favorite__created_at__gte=start_date),
                    distinct=True
                )
            ).annotate(
                recent_activity=F("recent_review_count") + F("recent_favorite_count")
            ).filter(
                recent_activity__gt=0
            ).order_by(
                "-recent_activity",
                "-recent_review_count",
                "-recent_favorite_count",
                "-avg_rating",
                "name"
            )

            if trending_qs.exists():
                trending_restaurant = trending_qs.first()
                context["trending_restaurant"] = trending_restaurant

                context["trending_reviews"] = Review.objects.filter(
                    restaurant=trending_restaurant,
                    created_at__gte=start_date
                ).order_by("-created_at")[:3]


        # favorite map feature
        context["favorite_ids"] = []

        if self.request.user.is_authenticated:
            profile = Profile.objects.filter(user=self.request.user).first()

            if profile:
                context["favorite_ids"] = list(
                    Favorite.objects.filter(profile=profile).values_list("restaurant_id", flat=True)
                )


        #folder feature
        context["saved_restaurant_ids"] = []

        if self.request.user.is_authenticated:
            profile = Profile.objects.filter(user=self.request.user).first()

            if profile:
                context["saved_restaurant_ids"] = list(
                    FolderItem.objects.filter(
                        folder__profile=profile
                    ).values_list("restaurant_id", flat=True).distinct()
                )

        return context


class RestaurantDetailView(DetailView):
    '''View for showing the details of a restaurant, including its reviews and favorites.'''
    model = Restaurant
    template_name = "project/show_restaurant.html"
    context_object_name = "restaurant"

    def get_context_data(self, **kwargs):
        '''Add restaurant reviews, favorite status, folder return link, and review likes.'''
        context = super().get_context_data(**kwargs)

        restaurant = self.get_object()
        context["reviews"] = restaurant.get_all_reviews()

        # Default values first, so logged-out users do not break the page.
        context["profile"] = None
        context["is_favorite"] = False
        context["liked_review_ids"] = []
        context["from_folder"] = None

        # Optional back-to-folder button.
        folder_id = self.request.GET.get("from_folder")

        if folder_id:
            folder = RestaurantFolder.objects.filter(pk=folder_id).first()

            if folder:
                context["from_folder"] = folder

        # User-specific information.
        if self.request.user.is_authenticated:
            profile = Profile.objects.filter(user=self.request.user).first()
            context["profile"] = profile

            context["is_favorite"] = Favorite.objects.filter(
                profile=profile,
                restaurant=restaurant
            ).exists()

            context["liked_review_ids"] = list(
                ReviewLike.objects.filter(
                    profile=profile
                ).values_list("review_id", flat=True)
            )

        return context


class MyProfileView(LoginRequiredMixin, DetailView):
    '''View for showing the profile of the currently logged in user, including their reviews and favorites.'''
    model = Profile
    template_name = "project/show_profile.html"
    context_object_name = "profile"

    def get_object(self):
        '''Return the profile of the currently logged in user.'''
        return Profile.objects.filter(user=self.request.user).first()

    def get_context_data(self, **kwargs):
        '''Determine which section to show on the profile page.'''
        context = super().get_context_data(**kwargs)

        show = self.request.GET.get("show", "reviews")
        context["show_section"] = show

        profile = self.get_object()

        context["folders"] = RestaurantFolder.objects.filter(
            profile=profile
        ).order_by("name")

        folder_id = self.request.GET.get("folder_id", "")

        context["selected_folder"] = None
        context["folder_items"] = None

        if show == "folder_detail" and folder_id:
            selected_folder = RestaurantFolder.objects.filter(
                pk=folder_id,
                profile=profile
            ).first()

            context["selected_folder"] = selected_folder

            if selected_folder:
                context["folder_items"] = FolderItem.objects.filter(
                    folder=selected_folder
                ).order_by("-created_at")

        return context

    def get_login_url(self):
        '''Redirect to login page if user is not authenticated.'''
        return reverse("login")

class ProfileDetailView(DetailView):
    '''View for showing any user's public profile.'''
    model = Profile
    template_name = "project/show_profile.html"
    context_object_name = "profile"

    def get_context_data(self, **kwargs):
        '''Determine which section to show when viewing another user's profile.'''
        context = super().get_context_data(**kwargs)

        show = self.request.GET.get("show", "reviews")
        context["show_section"] = show

        profile = self.get_object()

        context["folders"] = RestaurantFolder.objects.filter(
            profile=profile
        ).order_by("name")

        folder_id = self.request.GET.get("folder_id", "")

        context["selected_folder"] = None
        context["folder_items"] = None

        if show == "folder_detail" and folder_id:
            selected_folder = RestaurantFolder.objects.filter(
                pk=folder_id,
                profile=profile
            ).first()

            context["selected_folder"] = selected_folder

            if selected_folder:
                context["folder_items"] = FolderItem.objects.filter(
                    folder=selected_folder
                ).order_by("-created_at")

        return context
    

class CreateProfileView(CreateView):
    '''View for creating a new profile for a user.'''
    model = Profile
    form_class = CreateProfileForm
    template_name = "project/create_profile_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if "user_form" in kwargs:
            context["user_form"] = kwargs["user_form"]
        else:
            context["user_form"] = UserCreationForm(prefix="user")

        return context

    def form_valid(self, form):
        '''Create a new user account, log the user in,and link the profile to that user.'''
        user_form = UserCreationForm(self.request.POST, prefix="user")

        if not user_form.is_valid():
            return self.render_to_response(self.get_context_data(form=form, user_form=user_form))

        new_user = user_form.save()
        login(self.request, new_user)

        form.instance.user = new_user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("show_profile")


class UpdateProfileView(LoginRequiredMixin, UpdateView):
    '''View for updating the profile of the currently logged in user.'''
    model = Profile
    form_class = UpdateProfileForm
    template_name = "project/update_profile_form.html"

    def get_object(self):
        return Profile.objects.filter(user=self.request.user).first()

    def get_success_url(self):
        return reverse("show_profile")

    def get_login_url(self):
        return reverse("login")


class CreateReviewView(LoginRequiredMixin, CreateView):
    '''View for creating a new review for a restaurant.'''
    form_class = CreateReviewForm
    template_name = "project/create_review_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        restaurant = Restaurant.objects.get(pk=self.kwargs["pk"])
        context["restaurant"] = restaurant
        return context

    def form_valid(self, form):
        restaurant = Restaurant.objects.get(pk=self.kwargs["pk"])
        profile = Profile.objects.filter(user=self.request.user).first()
        images = self.request.FILES.getlist("images")

        if len(images) > 4:
            form.add_error(None, "You may upload up to 4 photos for one review.")
            return self.form_invalid(form)

        form.instance.restaurant = restaurant
        form.instance.profile = profile
        response = super().form_valid(form)

        for image in images:
            ReviewPhoto.objects.create(review=self.object, image_file=image)

        return response

    def get_success_url(self):
        return reverse("show_restaurant", kwargs={"pk": self.kwargs["pk"]})

    def get_login_url(self):
        return reverse("login")


class AddFavoriteView(LoginRequiredMixin, View):
    '''Add a restaurant to the current user's favorites.'''

    def post(self, request, pk):
        restaurant = Restaurant.objects.get(pk=pk)
        profile = Profile.objects.filter(user=request.user).first()

        # Prevent duplicate favorite rows for the same user and restaurant.
        if not Favorite.objects.filter(profile=profile, restaurant=restaurant).exists():
            Favorite.objects.create(profile=profile, restaurant=restaurant)

        return redirect("show_restaurant", pk=pk)


class RemoveFavoriteView(LoginRequiredMixin, View):
    '''Remove a restaurant from the current user's favorites.'''

    def post(self, request, pk):
        restaurant = Restaurant.objects.get(pk=pk)
        profile = Profile.objects.filter(user=request.user).first()

        Favorite.objects.filter(profile=profile, restaurant=restaurant).delete()

        return redirect("show_restaurant", pk=pk)
    


# Views for the extended feature: restaurant folders
class AddToFolderView(LoginRequiredMixin, View):
    '''Let a logged-in user add one restaurant to an existing or new folder.'''

    template_name = "project/add_to_folder.html"

    def get(self, request, pk):
        '''Show the form for adding a restaurant to a folder, including the user's existing folders.'''
        restaurant = Restaurant.objects.get(pk=pk)
        profile = Profile.objects.filter(user=request.user).first()

        folders = RestaurantFolder.objects.filter(profile=profile).order_by("name")
        form = CreateFolderForm()

        saved_folder_ids = list(
            FolderItem.objects.filter(
                restaurant=restaurant,
                folder__profile=profile
            ).values_list("folder_id", flat=True)
        )

        return render(request, self.template_name, {
            "restaurant": restaurant,
            "folders": folders,
            "form": form,
            "saved_folder_ids": saved_folder_ids,
        })

    def post(self, request, pk):
        restaurant = Restaurant.objects.get(pk=pk)
        profile = Profile.objects.filter(user=request.user).first()

        folder_id = request.POST.get("folder_id", "")
        new_folder_name = request.POST.get("name", "").strip()

        # User cannot select an existing folder AND create a new folder at the same time.
        if folder_id and new_folder_name:
            folders = RestaurantFolder.objects.filter(profile=profile).order_by("name")
            form = CreateFolderForm()

            saved_folder_ids = list(
                FolderItem.objects.filter(
                    restaurant=restaurant,
                    folder__profile=profile
                ).values_list("folder_id", flat=True)
            )

            return render(request, self.template_name, {
                "restaurant": restaurant,
                "folders": folders,
                "form": form,
                "saved_folder_ids": saved_folder_ids,
                "error_message": "Please either choose an existing folder or create a new folder, not both.",
            })

        # User selected an existing folder.
        if folder_id:
            folder = RestaurantFolder.objects.filter(
                pk=folder_id,
                profile=profile
            ).first()

        # User created a new folder.
        elif new_folder_name:
            folder, created = RestaurantFolder.objects.get_or_create(
                profile=profile,
                name=new_folder_name
            )

        # User did neither.
        else:
            folders = RestaurantFolder.objects.filter(profile=profile).order_by("name")
            form = CreateFolderForm()

            saved_folder_ids = list(
                FolderItem.objects.filter(
                    restaurant=restaurant,
                    folder__profile=profile
                ).values_list("folder_id", flat=True)
            )

            return render(request, self.template_name, {
                "restaurant": restaurant,
                "folders": folders,
                "form": form,
                "saved_folder_ids": saved_folder_ids,
                "error_message": "Please choose a folder or create a new one.",
            })

        if folder:
            FolderItem.objects.get_or_create(
                folder=folder,
                restaurant=restaurant
            )

        return redirect("show_all_restaurants")

    def get_login_url(self):
        '''Redirect to login page if user is not authenticated.'''
        return reverse("login")
    

class ToggleReviewLikeView(LoginRequiredMixin, View):
    """Let a logged-in user like or unlike a review."""

    def post(self, request, pk):
        ''''Handle the form submission for liking or unliking a review.'''
        review = Review.objects.get(pk=pk)
        profile = Profile.objects.filter(user=request.user).first()

        like = ReviewLike.objects.filter(
            review=review,
            profile=profile
        ).first()

        if like:
            like.delete()
        else:
            ReviewLike.objects.create(
                review=review,
                profile=profile
            )

        return redirect("show_restaurant", pk=review.restaurant.pk)

    def get_login_url(self):
        return reverse("login")
    

#Allow user to delete their own review, and only their own review. This is a POST request to prevent accidental deletions from a wrong click.
class DeleteReviewView(LoginRequiredMixin, View):
    ''''Let a logged-in user delete one of their reviews. Only the owner of the review can delete it.'''
    def post(self, request, pk):
        review = get_object_or_404(Review, pk=pk)

        # Only allow the owner to delete
        if review.profile.user != request.user:
            return redirect("show_restaurant", pk=review.restaurant.pk)

        restaurant_pk = review.restaurant.pk
        review.delete()

        # redirect back to restaurant page
        return redirect("show_restaurant", pk=restaurant_pk)