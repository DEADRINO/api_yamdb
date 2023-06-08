from reviews.models import User
import csv


def run():
    with open('static/data/users.csv') as file:
        reader = csv.reader(file)
        next(reader)  # Advance past the header

        User.objects.all().delete()

        for row in reader:
            user = User(id=row[0], username=row[1], email=row[2], role=row[3])
            user.save()
