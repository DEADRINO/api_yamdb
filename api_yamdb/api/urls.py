from django.urls import include, path
from rest_framework import routers

from api.views import CategoryViewSet, GenreViewSet, TitleViewSet


router = routers.DefaultRouter()


router.register('categories', CategoryViewSet)
router.register('genres', GenreViewSet)
router.register(r'titles', TitleViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
