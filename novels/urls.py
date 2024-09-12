from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from novels import views
from .views import update_profile_picture
from django.contrib.auth import views as auth_views
from .views import login_view,add_reply,rate_novel
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    # Home and other views
    path('', views.home, name='home'),
    path('filter/', views.filter_view, name='filter'),
    path('ranking/', views.ranking_view, name='ranking'),
    path('newest/', views.newest_view, name='newest'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('update-profile-picture/', update_profile_picture, name='update_profile_picture'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
     path('novel_list/', views.novel_list, name='novel_list'),

    # Novel-related paths

    path('novel/<int:novel_id>/', views.novel_details, name='novel_details'),
    path('novel/<int:novel_id>/comment/', views.add_comment, name='add_comment'),
    path('novel/<int:novel_id>/content/<int:chapter_number>/', views.novel_content_view, name='novel_content'),
    path('bookmark/<int:novel_id>/', views.bookmark_novel, name='bookmark_novel'),
    path('novel/<int:novel_id>/rate/', rate_novel, name='rate_novel'),

    # Comment actions
    path('like-comment/<int:comment_id>/', views.like_comment, name='like_comment'),
    path('dislike-comment/<int:comment_id>/', views.dislike_comment, name='dislike_comment'),
    path('reply/<int:comment_id>/', add_reply, name='add_reply'),
    path('delete_comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),

    path('ckeditor/', include('ckeditor_uploader.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
