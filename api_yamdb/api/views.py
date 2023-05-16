from django.shortcuts import get_object_or_404
from rest_framework import viewsets
# CategoryViewSet, GenreViewSet, TitleViewSet
from api.models import Category, Genre, Title
from .serializers import (CategorySerializer, GenreSerializer, TitleSerializer)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer