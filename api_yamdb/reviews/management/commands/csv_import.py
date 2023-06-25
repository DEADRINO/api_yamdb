import csv
from django.conf import settings
from django.core.management.base import BaseCommand
from core.shortcuts import get_object_or_none
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

    def load_data(self):
        for data in MODELS_FILES.items():
            with open(data[1]['path']) as file:
                reader = csv.reader(file)
                next(reader)  # Advance past the header

                data[1]['model'].objects.all().delete()

                for row in reader:
                    if data[0] in ['category', 'genre']:
                        item = data[1]['model'](id=row[0],
                                                name=row[1],
                                                slug=row[2])
                        item.save()

                    elif data[0] == 'genre_title':
                        genre_title = GenreTitle(id=row[0],
                                                 title_id=row[1],
                                                 genre_id=row[2])
                        genre_title.save()

                    elif data[0] == 'comment':
                        user = get_object_or_none(User, id=row[3])
                        comment = Comment(id=row[0], review_id=row[1],
                                          text=row[2], author=user,
                                          pub_date=row[4])
                        comment.save()

                    elif data[0] == 'review':
                        user = get_object_or_none(User, id=row[3])
                        review = Review(id=row[0], title_id=row[1],
                                        text=row[2], author=user, score=row[4],
                                        pub_date=row[5])
                        review.save()

                    elif data[0] == 'title':
                        category = get_object_or_none(Category, id=row[3])
                        title = Title(id=row[0], name=row[1], year=row[2],
                                      category=category)
                        title.save()
                    elif data[0] == 'user':
                        user = User(id=row[0], username=row[1], email=row[2],
                                    role=row[3])
                        user.save()

    def handle(self, *args, **kwargs):
        self.load_data()
