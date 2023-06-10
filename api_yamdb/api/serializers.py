from rest_framework import serializers
from reviews.models import Comment, Review, User
from reviews.models import Category, Genre, Title
from django.db.models import Avg

USERNAME_LENGHT = 150
EMAIL_LENGHT = 250


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=USERNAME_LENGHT,
        required=True
    )
    confirmation_code = serializers.CharField(required=True)


class SignupSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=USERNAME_LENGHT,
        required=True,
    )
    email = serializers.EmailField(
        max_length=EMAIL_LENGHT,
        required=True
    )


class AdminUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


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
    rating = serializers.SerializerMethodField()
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)

    def get_rating(self, obj):
        avg_scrores = obj.reviews.aggregate(rating=Avg('score'))
        if not avg_scrores['rating']:
            return None
        return int(avg_scrores['rating'])

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


class TitleEditSerializer(serializers.ModelSerializer):
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
