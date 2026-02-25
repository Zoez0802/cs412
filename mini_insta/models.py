from django.db import models
from django.urls import reverse


class Profile(models.Model):
    username = models.TextField(blank=False)
    display_name = models.TextField(blank=False)
    profile_image_url = models.URLField(blank=True)
    bio_text = models.TextField(blank=True)
    join_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.username}'
    

    def get_all_posts(self):
        """Return a QuerySet of all Posts created by this Profile"""
        return Post.objects.filter(profile=self).order_by("-timestamp")


    def get_absolute_url(self):
        '''Return the URL to display this Profile.'''
        return reverse('show_profile', kwargs={'pk': self.pk})


    def get_followers(self):
        """Return a *list* of Profile objects that follow this profile."""
        followers = []
        f_r = Follow.objects.filter(profile=self)

        for f in f_r:
            followers.append(f.follower_profile)

        return followers

    def get_num_followers(self):
        """Return the number of followers (int)."""
        return Follow.objects.filter(profile=self).count()

    def get_following(self):
        """Return a list of Profile objects that this profile is following"""
        following = []
        f_r = Follow.objects.filter(follower_profile=self)

        for f in f_r:
            following.append(f.profile)

        return following

    def get_num_following(self):
        """Return the number of profiles this profile is following (int)."""
        return Follow.objects.filter(follower_profile=self).count()


class Post(models.Model):
    """Encapsulate the data for one Instagram-style post."""

    # 1 Profile to many Posts
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    caption = models.TextField(blank=True)
    
    def __str__(self):
        """Return a string representation of this Post."""
        return f'Post by {self.profile.username} at {self.timestamp}'
    

    def get_all_photos(self):
        """Return a QuerySet of all Photos for this Post"""
        return Photo.objects.filter(post=self).order_by("timestamp")

    # let CreateView to redirect to the Post detail page after successfully creating a new Post.
    def get_absolute_url(self):
        '''Return the URL to display this Post.'''
        return reverse('show_post', kwargs={'pk': self.pk})
    
    #I decided to def this extra to display the first photo of the post
    def get_first_photo(self):
        photos = Photo.objects.filter(post=self).order_by('timestamp')
        if photos:
            return photos[0]
        return None

    def get_all_comments(self):
        """Return a QuerySet of all Comments for this Post."""
        return Comment.objects.filter(post=self).order_by("timestamp")


    def get_likes(self):
        """Return a QuerySet of all Likes for this Post."""
        return Like.objects.filter(post=self).order_by("timestamp")
    
class Photo(models.Model):
    """Encapsulate the data for one image associated with a Post."""

    # 1 Post to many Photos
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image_url = models.URLField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    image_file = models.ImageField(blank=True)

    def get_image_url(self):
        if self.image_url: return self.image_url
        if self.image_file: return self.image_file.url
        return ''

    def __str__(self):
        '''Return a string of this Photo.'''
        if self.image_url: return self.image_url
        if self.image_file: return self.image_file.name
        return 'Photo'

#Task 5.3 -A5
class Follow(models.Model):
    ''' Follow relationship between two Profiles.'''

    # the person being followed (publisher)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="profile")
    # the person doing the following 
    follower_profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="follower_profile")
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        '''Return and view the string representation of this Follow relationship.'''
        return f'{self.follower_profile.username} follows {self.profile.username}'
    


#Task 5.4 -A5
class Comment(models.Model):
    '''Encapsulate the data for one comment on a Post.'''

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    text = models.TextField(blank=False)

    def __str__(self):
        '''Return a string representation of this Comment.'''
        return f'{self.profile.username} on Post {self.post.pk}: {self.text}'


 #Task 5.5 -A5
class Like(models.Model):
    '''Encapsulate a like made by one Profile on one Post.'''

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        '''Return a string representation of this Like.'''
        return f'{self.profile.username} likes Post {self.post.pk}'