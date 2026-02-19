from django.db import models

class Profile(models.Model):
    username = models.TextField(blank=False)
    display_name = models.TextField(blank=False)
    profile_image_url = models.URLField(blank=True)
    bio_text = models.TextField(blank=True)
    join_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.username}'
    
    #task 1.4
    def get_all_posts(self):
        """Return a QuerySet of all Posts created by this Profile"""
        return Post.objects.filter(profile=self).order_by("-timestamp")

# task 1.1, new model called Post
class Post(models.Model):
    """Encapsulate the data for one Instagram-style post."""

    # 1 Profile to many Posts
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    caption = models.TextField(blank=True)

    def __str__(self):
        """Return a string representation of this Post."""
        return f'Post by {self.profile.username} at {self.timestamp}'
    
    # task 1.4
    def get_all_photos(self):
        """Return a QuerySet of all Photos for this Post"""
        return Photo.objects.filter(post=self).order_by("timestamp")

# task 1.2
class Photo(models.Model):
    """Encapsulate the data for one image associated with a Post."""

    # 1 Post to many Photos
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image_url = models.URLField(blank=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return a string representation of this Photo."""
        return f'Photo for Post {self.post.id} at {self.timestamp}'
