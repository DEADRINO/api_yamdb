# from core.shortcuts import get_object_or_none

# from api.models import Genre, GenreTitle, Title
from reviews.models import GenreTitle
import csv


def run():
    with open('static/data/genre_title.csv') as file:
        reader = csv.reader(file)
        next(reader)  # Advance past the header

        GenreTitle.objects.all().delete()

        for row in reader:
            genre_title = GenreTitle(id=row[0],
                                     title_id=row[1],
                                     genre_id=row[2])
            genre_title.save()
