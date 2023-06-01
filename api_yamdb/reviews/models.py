from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from api_yamdb.settings import TEXT_LIMIT


User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)


class Genre(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)


class Title(models.Model):
    name = models.CharField(max_length=200)
    year = models.IntegerField()
    description = models.CharField(max_length=200, blank=True, null=True)
    category = models.ForeignKey(
        Category, on_delete=models.DO_NOTHING,
        related_name='title'
    )
    genre = models.ManyToManyField(Genre, through='GenreTitle')


class GenreTitle(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.DO_NOTHING)
    title = models.ForeignKey(Title, on_delete=models.DO_NOTHING)


class Review(models.Model):
    """Отзыв."""
    text = models.TextField(
        verbose_name='Текст',
        help_text='Тект отзыва'
    )
    score = models.IntegerField(
        verbose_name='Oценка',
        help_text='Оценка произведения',
        validators=(
            MinValueValidator(
                1,
                message='Оценка не может быть меньше 1'
            ),
            MaxValueValidator(
                10,
                message='Оценка не может быть больше 10'
            ),
        )
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Название произведения',
        help_text='Название произведения'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Aвтор',
        help_text='Автор произведения'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации',
        help_text='Дата публикации'
    )

    class Meta:
        verbose_name = 'Отзыв'
        help_text = 'Отзыв о произведении'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text[:TEXT_LIMIT]


class Comment(models.Model):
    """Комментарий."""
    text = models.TextField(
        verbose_name='Текст',
        help_text='Текст комментария'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Aвтор',
        help_text='Автор произведения'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации',
        help_text='Дата публикации',
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв',
        help_text='Отзыв о произведении'
    )

    class Meta:
        verbose_name = 'Комментарий',
        help_text = 'Комментарий к отзыву'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text[:TEXT_LIMIT]