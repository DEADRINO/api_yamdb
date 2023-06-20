from . import views
from django.urls import include, path
from rest_framework import routers
from v1.views import (
    CategoryViewSet,
    CommentViewSet,
    GenreViewSet,
    ReviewViewSet,
    TitleViewSet,
)

router_v1 = routers.DefaultRouter()
router_v1.register('users', views.UserViewSet, basename='users')
router_v1.register('categories', CategoryViewSet)
router_v1.register('genres', GenreViewSet)
router_v1.register(r'titles', TitleViewSet)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

auth_urls = [
    path('signup/', views.SignUpView.as_view()),
    path('token/', views.GetTokenView.as_view()),
]

urlpatterns = [
    path('', include(router_v1.urls)),
    path('auth/', include(auth_urls)),
]
