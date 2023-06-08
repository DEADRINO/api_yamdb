from warnings import filters
from .permissions import *
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.db import IntegrityError
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, status, viewsets, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from reviews.models import *
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import action


from api.serializers import (CommentSerializer, ReviewSerializer,
                             SignupSerializer)

from .serializers import (
    AdminUserSerializer,
    CategorySerializer,
    GenreSerializer,
    TitleSerializer,
    TokenSerializer,
    UserSerializer
)

class SignUpView(APIView):
    http_method_names = ['post']
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        existing_user = self.check_existing_user(username, email)
        if existing_user:
            return Response(
                'Пользователь с таким именем пользователя или email уже существует.',
                status=status.HTTP_400_BAD_REQUEST
            )

        user = self.create_user(username, email, password)
        if not user:
            return Response(
                'Не удалось создать пользователя.',
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        confirmation_code = default_token_generator.make_token(user)
        self.send_confirmation_email(email, confirmation_code)

        response_data = {
            'username': user.username,
            'email': user.email
        }
        return Response(response_data, status=status.HTTP_201_CREATED)


    def check_existing_user(self, username, email):
        return User.objects.filter(Q(username=username) | Q(email=email)).exists()


    def create_user(self, username, email):
        try:
            user = User.objects.create(
                email=email,
                username=username
            )
            return user
        except IntegrityError:
            return None
        

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
            return Response({'token': access_token}, status=status.HTTP_201_CREATED)

        return Response('Некорректный код.', status=status.HTTP_400_BAD_REQUEST)

class UserViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
    queryset = User.objects.all()
    serializer_class = AdminUserSerializer
    permission_classes = (IsAdminPermission,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'

    @action(detail=False, methods=['get', 'patch'], permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        if request.method == 'GET':
            return self._get_current_user(request)
        elif request.method == 'PATCH':
            return self._update_current_user(request)
        else:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def _get_current_user(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def _update_current_user(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)



class CategoryViewSet(mixins.ListModelMixin,
                      mixins.CreateModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'


class GenreViewSet(mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
    queryset = Title.objects.all()
    serializer_class = TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsReadOnlyAuthor)

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
    permission_classes = (IsReadOnlyAuthor)

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        serializer.save(
            author=self.request.user,
            review=review
        )
