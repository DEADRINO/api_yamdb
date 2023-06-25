from django.core.management.base import BaseCommand
from reviews.models import (Category, Comment, Genre, GenreTitle,
                            Review, Title, User)

MODELS = [Category, Comment, Genre, Title, Review, GenreTitle, User]


class Command(BaseCommand):
    help = 'Clear all data from database'

    def handle(self, *args, **kwargs):
        for model in MODELS:
            model.objects.all().delete()
