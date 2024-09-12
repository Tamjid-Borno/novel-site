# novels/management/commands/reset_views.py
from django.core.management.base import BaseCommand
from novels.models import Novel

class Command(BaseCommand):
    help = 'Reset view counts for all novels'

    def handle(self, *args, **kwargs):
        novels = Novel.objects.all()
        for novel in novels:
            novel.views = 0
            novel.save()
            self.stdout.write(self.style.SUCCESS(f'Successfully reset views for {novel.title}'))
