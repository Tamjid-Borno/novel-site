from django.contrib import admin
from .models import Novel, Tag, NovelContent

class NovelAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_date', 'num_chapters', 'rating', 'is_ongoing')  # Ensure only valid fields
    search_fields = ('title',)
    list_filter = ('is_ongoing',)
    fieldsets = (
        (None, {'fields': ('title', 'cover_image', 'release_date', 'num_chapters', 'views', 'rating', 'is_ongoing', 'tags', 'summary')}),
    )

admin.site.register(Novel, NovelAdmin)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)

from django.contrib import admin
from ckeditor.widgets import CKEditorWidget
from ckeditor.fields import RichTextField
from .models import NovelContent

class NovelContentAdmin(admin.ModelAdmin):
    formfield_overrides = {
        RichTextField: {'widget': CKEditorWidget()},
    }
    list_display = ['chapter_title', 'novel', 'chapter_number']
    fields = ('novel', 'chapter_number', 'chapter_title', 'content', 'view_count')

admin.site.register(NovelContent, NovelContentAdmin)

from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'profile_picture')
