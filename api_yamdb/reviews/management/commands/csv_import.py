import csv
from django.core.management.base import BaseCommand
from reviews.models import (Category, Comment, Genre, GenreTitle,
                            Review, Title, User)


MODELS_FILES = {
    'user': {
        'model': User,
        'path': 'static/data/users.csv'
    },
    'category': {
        'model': Category,
        'path': 'static/data/category.csv'
    },
    'genre': {
        'model': Genre,
        'path': 'static/data/genre.csv'
    },
    'title': {
        'model': Title,
        'path': 'static/data/titles.csv'
    },
    'genre_title': {
        'model': GenreTitle,
        'path': 'static/data/genre_title.csv'
    },
    'review': {
        'model': Review,
        'path': 'static/data/review.csv'
    },
    'comment': {
        'model': Comment,
        'path': 'static/data/comments.csv'
    }
}


class Command(BaseCommand):
    help = 'For loading data from .csv files'

    def _create_correct_row_fields(self, row):
        if row.get('author'):
            row['author'] = User.objects.get(pk=row['author'])
        if row.get('review_id'):
            row['review'] = Review.objects.get(pk=row['review_id'])
        if row.get('title_id'):
            row['title'] = Title.objects.get(pk=row['title_id'])
        if row.get('category'):
            row['category'] = Category.objects.get(pk=row['category'])
        if row.get('genre'):
            row['genre'] = Genre.objects.get(pk=row['genre'])
        return row

    def load_data(self):
        for key, data in MODELS_FILES.items():
            path = data['path']
            model = data['model']

            model.objects.all().delete()

            with open(path) as file:
                csv_read = csv.DictReader(file)
                for row in csv_read:
                    row = self._create_correct_row_fields(row)
                    model.objects.get_or_create(**row)

    def handle(self, *args, **kwargs):
        self.load_data()
