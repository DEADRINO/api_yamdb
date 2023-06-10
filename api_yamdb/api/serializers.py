from rest_framework import serializers
from reviews.validators import names_validator, symbols_validator
from reviews.models import Comment, Review, User

from reviews.models import Category, Genre, Title

USERNAME_LENGHT = 150
EMAIL_LENGHT = 250

class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=USERNAME_LENGHT,
        required=True,
        validators=[symbols_validator, names_validator]
    )
    confirmation_code = serializers.CharField(required=True)


class SignupSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=USERNAME_LENGHT,
        required=True,
        validators=[symbols_validator, names_validator]
    )
    email = serializers.EmailField(
        max_length=EMAIL_LENGHT,
        required=True
    )


class AdminUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'role',
            'bio',
            'first_name',
            'last_name'
        )


class UserSerializer(AdminUserSerializer):
    class Meta(AdminUserSerializer.Meta):
        model = User
        read_only_fields = ('role',)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'slug')
        lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('id', 'name', 'slug')
        lookup_field = 'slug'


class TitleSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field=('slug')
    )

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'category', 'genre')


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    def validate(self, data):
        if self.context.get('request').method != 'POST':
            return data
        author = self.context.get('request').user
        title_id = self.context.get('view').kwargs.get('title_id')
        if Review.objects.filter(author=author, title=title_id).exists():
            raise serializers.ValidationError(
                'Невозможно повторно отправить отзыв на данное произведение.'
            )
        return data

    class Meta:
        model = Review
        fields = (
            'id', 'text', 'author', 'score', 'pub_date'
        )


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Comment
        fields = (
            'id', 'text', 'author', 'pub_date'
        )
