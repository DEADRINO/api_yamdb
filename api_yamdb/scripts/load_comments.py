from core.shortcuts import get_object_or_none

from reviews.models import Comment, User
import csv


def run():
    with open('static/data/comments.csv') as file:
        reader = csv.reader(file)
        next(reader)  # Advance past the header

        Comment.objects.all().delete()

        for row in reader:
            user = get_object_or_none(User, id=row[3])

            comment = Comment(id=row[0], review_id=row[1], text=row[2],
                              author=user, pub_date=row[4])
            comment.save()
