from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.conf import settings
from ckeditor.fields import RichTextField
import os

# Tag model
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

# Novel model
class Novel(models.Model):
    cover_image = models.ImageField(upload_to='covers/')
    description = models.TextField()
    id = models.AutoField(primary_key=True)
    is_ongoing = models.BooleanField(default=False)
    num_chapters = models.IntegerField()
    ranking = models.IntegerField(default=0)
    release_date = models.DateField()
    title = models.CharField(max_length=255)
    is_top = models.BooleanField(default=False)
    status = models.CharField(
        max_length=50,
        choices=[('Ongoing', 'Ongoing'), ('Completed', 'Completed')],
        default='Ongoing'
    )
    created_date = models.DateTimeField(default=timezone.now)
    views = models.PositiveIntegerField(default=0)  # PositiveIntegerField to ensure no negative values
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)
    rating_count = models.PositiveIntegerField(default=0)
    tags = models.ManyToManyField(Tag, blank=True)
    summary = RichTextField(blank=True, null=True)

    def __str__(self):
        return self.title

    # Dynamically calculate the average rating
    @property
    def average_rating(self):
        total_ratings = self.ratings.count()
        if total_ratings > 0:
            return self.ratings.aggregate(models.Avg('rating'))['rating__avg']
        return 0

# Chapter model
class Chapter(models.Model):
    novel = models.ForeignKey(Novel, on_delete=models.CASCADE, related_name='chapters')
    title = models.CharField(max_length=255)
    content = RichTextField()  # Use RichTextField for chapter content
    view_count = models.PositiveIntegerField(default=0)  # Add view count tracking for chapters
    chapter_number = models.IntegerField()

    def __str__(self):
        return f'{self.novel.title} - {self.title}'

# Rating model
class Rating(models.Model):
    novel = models.ForeignKey(Novel, related_name='ratings', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = ('novel', 'user')  

    def __str__(self):
        return f'{self.user.username} - {self.novel.title} - {self.rating}'

# UserProfile model
def get_profile_picture_choices():
    profile_pics_dir = os.path.join(settings.BASE_DIR, 'static/profile_pics')
    if not os.path.exists(profile_pics_dir):
        return []  # return an empty list if directory does not exist
    choices = [(f, f) for f in os.listdir(profile_pics_dir) if os.path.isfile(os.path.join(profile_pics_dir, f))]
    return choices

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    bookmarked_novels = models.ManyToManyField('Novel', related_name='bookmarked_by')

    def __str__(self):
        return self.user.username

# Comment model
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    novel = models.ForeignKey(Novel, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='comment_likes', blank=True)
    dislikes = models.ManyToManyField(User, related_name='comment_dislikes', blank=True)
    parent = models.ForeignKey(
        'self', 
        null=True, 
        blank=True, 
        on_delete=models.CASCADE, 
        related_name='children',  # Unique related_name for self-referencing relationship
        related_query_name='comment_parent'  # Changed related_query_name
    )

    def __str__(self):
        return self.text[:20]

    def like_count(self):
        return self.likes.count()

    def dislike_count(self):
        return self.dislikes.count()

    # Calculate score based on likes and dislikes
    def score(self):
        return self.likes.count() - self.dislikes.count()


# Reply model
class Reply(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(
        Comment, 
        on_delete=models.CASCADE, 
        related_name='replies',  # Unique related_name to avoid clashes
        related_query_name='replies'
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content[:20]

# NovelContent model with RichTextField for content
class NovelContent(models.Model):
    novel = models.ForeignKey(Novel, on_delete=models.CASCADE, related_name='contents')
    chapter_number = models.IntegerField()
    chapter_title = models.CharField(max_length=255)
    content = RichTextField()  # Use CKEditor
    view_count = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('novel', 'chapter_number')

# Bookmark model
class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookmarks')
    novel = models.ForeignKey(Novel, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} bookmarked {self.novel.title}"
