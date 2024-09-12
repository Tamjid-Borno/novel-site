# novel_site/urls.py
from django.contrib import admin
from django.urls import path, include
import tinymce.urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('novels.urls')),  # This points to the novels app's urls.py
    path('tinymce/', include(tinymce.urls)),
]
