from rest_framework import serializers
from reviews.validators import names_validator, symbols_validator
from reviews.models import (
    Category,
    Comment,
    Genre,
    Review,
    Title,
    User,
)

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

    def create(self, validated_data):
        # Валидация данных пользователя
        validated_data = self.validate(validated_data)

        # Создание нового пользователя
        user = User.objects.create(**validated_data)

        return user

    def validate(self, data):
        username = data.get('username')
        email = data.get('email')

        # Проверка на существование пользователя с таким же именем или почтой
        if User.objects.filter(username=username, email=email).exists():
            raise serializers.ValidationError('Пользователь уже существует.')

        return data


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
        fields = ('name', 'slug')
        lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')
        lookup_field = 'slug'


class TitleReadSerializer(serializers.ModelSerializer):
    rating = serializers.FloatField(read_only=True)
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'category',
            'genre'
        )


class TitleSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug')
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True
    )

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')


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
