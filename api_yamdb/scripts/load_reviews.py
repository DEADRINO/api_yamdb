from core.shortcuts import get_object_or_none

from reviews.models import Review, User
import csv


def run():
    with open('static/data/review.csv') as file:
        reader = csv.reader(file)
        next(reader)  # Advance past the header

        Review.objects.all().delete()

        for row in reader:
            user = get_object_or_none(User, id=row[3])

            review = Review(id=row[0], title_id=row[1], text=row[2],
                            author=user, score=row[4], pub_date=row[5])
            review.save()
