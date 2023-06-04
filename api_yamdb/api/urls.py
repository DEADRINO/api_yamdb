from . import views
from django.urls import include, path
from rest_framework import routers

from api.views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                       ReviewViewSet, TitleViewSet, SignUpView,)

router = routers.DefaultRouter()


router.register('categories', CategoryViewSet)
router.register('genres', GenreViewSet)
router.register(r'titles', TitleViewSet)
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)


urlpatterns = [
    path('v1/', include(router.urls)),
    path('auth/signup/', views.SignUpView.as_view()),
    path('auth/token/', views.GetTokenView.as_view())
]
