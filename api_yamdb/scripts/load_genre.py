from api.models import Genre
import csv


def run():
    with open('static/data/genre.csv') as file:
        reader = csv.reader(file)
        next(reader)  # Advance past the header

        Genre.objects.all().delete()

        for row in reader:
            genre = Genre(id=row[0], name=row[1], slug=row[2])
            genre.save()
