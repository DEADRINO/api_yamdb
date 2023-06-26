from warnings import filters
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Avg
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from reviews.models import (
    Category,
    User,
    Genre,
    Review,
    Title,
)
from .permissions import (
    IsAdminPermission,
    IsAdminOrReadOnlyPermission,
    IsReadOnlyAuthor,
)
from .serializers import (
    CommentSerializer,
    ReviewSerializer,
    SignupSerializer,
    AdminUserSerializer,
    CategorySerializer,
    GenreSerializer,
    TitleReadSerializer,
    TitleSerializer,
    TokenSerializer,
    UserSerializer,
)
from .filters import FilterTitle
from .mixins import BaseViewSet


class SignUpView(APIView):
    http_method_names = ['post', ]
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username')
        email = serializer.validated_data.get('email')
        user, some_data = User.objects.get_or_create(email=email,
                                                     username=username)
        if not user:
            return Response(
                'Не удалось создать пользователя.',
                status=status.HTTP_400_BAD_REQUEST
            )
        confirmation_code = default_token_generator.make_token(user)
        self.send_confirmation_email(email, confirmation_code)
        response_data = {
            'username': user.username,
            'email': user.email
        }
        return Response(response_data, status=status.HTTP_200_OK)

    def send_confirmation_email(self, email, confirmation_code):
        subject = 'Добро пожаловать!'
        message = f'Ваш код подтверждения: {confirmation_code}.'
        from_email = settings.YAMDB_EMAIL
        to_email = email

        email = EmailMessage(subject, message, from_email, [to_email])
        email.send(fail_silently=False)


class GetTokenView(APIView):
    http_method_names = ['post']
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        confirmation_code = serializer.validated_data['confirmation_code']
        user = get_object_or_404(User, username=username)
        if default_token_generator.check_token(user, confirmation_code):
            access_token = str(RefreshToken.for_user(user).access_token)
            return Response({'token': access_token},
                            status=status.HTTP_201_CREATED)

        return Response('Некорректный код.',
                        status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
    queryset = User.objects.all()
    serializer_class = AdminUserSerializer
    permission_classes = (IsAdminPermission,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'

    @action(
        detail=False,
        url_path='me',
        methods=['get', 'patch'],
        permission_classes=[permissions.IsAuthenticated, ]
    )
    def me(self, request):
        if request.method == 'GET':
            serializer = UserSerializer(request.user)
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        # elif request.method == 'PATCH':
        #     return self._update_current_user(request)

    # def _get_current_user(self, request):
    #     serializer = UserSerializer(request.user)
        # return Response(
        #     serializer.data,
        #     status=status.HTTP_200_OK
        # )

    # def _update_current_user(self, request):
        serializer = UserSerializer(request.user,
                                    data=request.data,
                                    partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )


class CategoryViewSet(BaseViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(BaseViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = LimitOffsetPagination


class TitleViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
    queryset = Title.objects.all()
    permission_classes = (IsAdminOrReadOnlyPermission,)
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = FilterTitle

    def get_serializer_class(self):
        if self.action in ("retrieve", "list"):
            return TitleReadSerializer
        return TitleSerializer

    def get_queryset(self):
        queryset = Title.objects.all().annotate(rating=Avg('reviews__score'))
        return queryset


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsReadOnlyAuthor,)

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(
            author=self.request.user,
            title=title
        )


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsReadOnlyAuthor,)

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        serializer.save(
            author=self.request.user,
            review=review
        )
