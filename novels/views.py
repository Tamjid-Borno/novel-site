from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
import json
import logging

from .forms import CommentForm, ReplyForm, ProfilePictureForm
from .models import Novel, Comment, Rating, Reply, NovelContent, Bookmark, UserProfile

logger = logging.getLogger(__name__)

# Home view with pagination for ongoing releases and top novels
def home(request):
    ongoing_releases_list = Novel.objects.filter(is_ongoing=True).order_by('-release_date')
    ongoing_paginator = Paginator(ongoing_releases_list, 15)
    ongoing_page_number = request.GET.get('ongoing_page', 1)
    ongoing_page_obj = ongoing_paginator.get_page(ongoing_page_number)

    top_novels_list = Novel.objects.filter(is_top=True, rating__gte=4).order_by('-release_date')
    top_paginator = Paginator(top_novels_list, 15)
    top_page_number = request.GET.get('top_page', 1)
    top_page_obj = top_paginator.get_page(top_page_number)

    context = {
        'ongoing_releases': ongoing_page_obj,
        'top_novels': top_page_obj,
    }

    return render(request, 'home.html', context)

# View for displaying novel details and handling comments
def novel_details(request, novel_id):
    novel = get_object_or_404(Novel, id=novel_id)
    comments = Comment.objects.filter(novel=novel, parent=None).order_by('-created_at')

    if request.method == 'POST':
        comment_text = request.POST.get('comment')
        parent_id = request.POST.get('parent_id')
        parent_comment = Comment.objects.get(id=parent_id) if parent_id else None

        if comment_text:
            Comment.objects.create(
                novel=novel,
                user=request.user,
                text=comment_text,
                parent=parent_comment
            )
            return redirect('novel_details', novel_id=novel_id)

    return render(request, 'novel_details.html', {
        'novel': novel,
        'comments': comments
    })

# View for the filter page
def filter_view(request):
    return render(request, 'filter.html')

from django.shortcuts import render
from .models import Novel

def ranking_view(request):
    # Fetch all novels, sorted by rating in descending order
    novels = Novel.objects.all().order_by('-rating')
    
    # Pass the sorted novels to the template
    return render(request, 'ranking.html', {'novels': novels})


def newest_view(request):
    # Fetch all novels, sorted by release_date in descending order
    novels = Novel.objects.all().order_by('-release_date')
    
    # Pass the sorted novels to the template
    return render(request, 'newest.html', {'novels': novels})


# Signup view
def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Error creating account. Please correct the errors below.")
    else:
        form = UserCreationForm()

    return render(request, 'signup.html', {'form': form})

# Login view
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            logger.info(f"User authenticated: {user.username}")
            auth_login(request, user)
            return redirect('home')
        else:
            logger.error(f"Form errors: {form.errors}")
            messages.error(request, "Invalid login credentials. Please check your email and password.")
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})

import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.db.models import Avg
from .models import Novel, Rating

@login_required
@require_POST
def rate_novel(request, novel_id):
    try:
        # Parse the incoming JSON data
        data = json.loads(request.body)
        rating = data.get('rating')

        # Validate the rating is a number and within range
        if rating is None or not isinstance(rating, int) or rating < 1 or rating > 5:
            return JsonResponse({'success': False, 'error': 'Invalid rating. Rating must be between 1 and 5.'}, status=400)

        # Get the novel instance
        novel = get_object_or_404(Novel, id=novel_id)

        # Update or create the rating for the user and novel
        Rating.objects.update_or_create(
            user=request.user,
            novel=novel,
            defaults={'rating': rating}
        )

        # Recalculate the average rating and the count of ratings
        average_rating = novel.ratings.aggregate(Avg('rating'))['rating__avg'] or 0
        novel.rating = round(average_rating, 1)
        novel.rating_count = novel.ratings.count()
        novel.save()

        # Return the updated rating to the frontend
        return JsonResponse({'success': True, 'new_rating': novel.rating})

    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Invalid JSON'}, status=400)

    except Exception as e:
        # Log the exception (optional but useful in debugging)
        print(f"Error in rating novel: {str(e)}")
        return JsonResponse({'success': False, 'error': 'Something went wrong. Please try again later.'}, status=500)



# Add reply view
@login_required
def add_reply(request, comment_id):
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            comment = get_object_or_404(Comment, id=comment_id)
            Reply.objects.create(
                user=request.user,
                comment=comment,
                content=content
            )
            print("Reply created successfully")
        else:
            print("Content is missing")
    return redirect(request.META.get('HTTP_REFERER', 'home'))

@login_required
def like_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    
    # Check if user already liked the comment
    if comment.likes.filter(id=request.user.id).exists():
        # If already liked, remove the like
        comment.likes.remove(request.user)
    else:
        # If not liked yet, add the like
        comment.likes.add(request.user)
        # Ensure the user can't both like and dislike
        comment.dislikes.remove(request.user)  

    # Return updated like/dislike counts
    return JsonResponse({
        'like_count': comment.likes.count(),
        'dislike_count': comment.dislikes.count()
    })


@login_required
def dislike_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    
    # Check if user already disliked the comment
    if comment.dislikes.filter(id=request.user.id).exists():
        # If already disliked, remove the dislike
        comment.dislikes.remove(request.user)
    else:
        # If not disliked yet, add the dislike
        comment.dislikes.add(request.user)
        # Ensure the user can't both like and dislike
        comment.likes.remove(request.user)

    # Return updated like/dislike counts
    return JsonResponse({
        'like_count': comment.likes.count(),
        'dislike_count': comment.dislikes.count()
    })


# Add comment view
@login_required
def add_comment(request, novel_id):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.novel = get_object_or_404(Novel, id=novel_id)
            comment.save()
            return JsonResponse({'success': True, 'comment_id': comment.id})
        return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)

# Delete comment view
@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user == comment.user:
        comment.delete()
    return redirect('novel_details', novel_id=comment.novel.id)

# Novel content view
def novel_content_view(request, novel_id, chapter_number):
    novel = get_object_or_404(Novel, id=novel_id)
    novel_content = get_object_or_404(NovelContent, novel=novel, chapter_number=chapter_number)
    
    # Increment view count
    novel.views += 1
    novel.save()

    return render(request, 'novel_content.html', {
        'novel': novel,
        'novel_content': novel_content
    })

# Bookmark novel view
@login_required
def bookmark_novel(request, novel_id):
    novel = get_object_or_404(Novel, id=novel_id)
    
    if Bookmark.objects.filter(user=request.user, novel=novel).exists():
        return JsonResponse({'status': 'already_bookmarked'}, status=400)
    
    Bookmark.objects.create(user=request.user, novel=novel)
    
    return JsonResponse({'status': 'success', 'message': 'Bookmark added successfully'})

# User dashboard view
@login_required
def dashboard(request):
    bookmarks = Bookmark.objects.filter(user=request.user).select_related('novel')
    comments = request.user.comments.all()

    return render(request, 'dashboard.html', {
        'bookmarks': bookmarks,
        'comments': comments
    })

# Update profile picture view
@login_required
def update_profile_picture(request):
    if not hasattr(request.user, 'userprofile'):
        UserProfile.objects.create(user=request.user)

    user_profile = request.user.userprofile

    if request.method == 'POST':
        form = ProfilePictureForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = ProfilePictureForm(instance=user_profile)

    return render(request, 'dashboard.html', {'form': form})

# Custom login view
from django.contrib.auth.views import LoginView

class CustomLoginView(LoginView):
    template_name = 'login.html'

    def form_valid(self, form):
        user = form.get_user()
        logger.info(f"User logged in: {user.username}")
        return super().form_valid(form)

    def form_invalid(self, form):
        logger.error(f"Login failed: {form.errors}")
        return super().form_invalid(form)


from django.shortcuts import render
from .models import Novel, Tag

def filter_view(request):
    tags = Tag.objects.all()
    selected_tags = request.GET.getlist('tags')
    
    if selected_tags:
        filtered_novels = Novel.objects.filter(tags__in=selected_tags).distinct()
    else:
        filtered_novels = Novel.objects.all()
    
    context = {
        'tags': tags,
        'filtered_novels': filtered_novels,
        'ongoing_releases': filtered_novels.filter(is_ongoing=True),  # For the "New Ongoing Series" section
    }
    return render(request, 'filter.html', context)

# views.py
from django.shortcuts import render
from .models import Novel  # Assuming Novel is the model for novels

def novel_list(request):
    query = request.GET.get('q')  # Get the search term from the URL parameter
    if query:
        novels = Novel.objects.filter(title__icontains=query)  # Filter novels by title
    else:
        novels = Novel.objects.all()  # Show all novels if no search term
    return render(request, 'novel_list.html', {'novels': novels})
