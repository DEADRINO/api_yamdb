from core.shortcuts import get_object_or_none

from api.models import Category, Title
import csv


def run():
    with open('static/data/titles.csv') as file:
        reader = csv.reader(file)
        next(reader)  # Advance past the header

        Title.objects.all().delete()

        for row in reader:
            category = get_object_or_none(Category, id=row[3])

            title = Title(id=row[0],
                          name=row[1],
                          year=row[2],
                          category=category)
            title.save()
