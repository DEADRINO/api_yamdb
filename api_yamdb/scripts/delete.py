from api.models import Category, Genre, GenreTitle, Title

MODELS = {
    'genre_title': GenreTitle,
    'title': Title,
    'category': Category,
    'genre': Genre
}


def run(*script_args):
    if (len(script_args) == 0):
        for model in MODELS:
            MODELS[model].objects.all().delete()
    else:
        for model in script_args:
            MODELS[model.lower()].objects.all().delete()
