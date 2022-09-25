from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import (CategoryViewSet, GenresViewSet, TitlesViewSet,
                    ReviewViewSet, CommentsViewSet)
from users.views import UserViewSet, register, get_jwt_token


router = DefaultRouter()
router.register('categories', CategoryViewSet)
router.register('genres', GenresViewSet)
router.register('titles', TitlesViewSet)
router.register(r'titles/(?P<title_id>\d+)/reviews',
                ReviewViewSet, basename='reviews')
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentsViewSet, basename='comments'
),
router.register(r'users', UserViewSet)

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', register, name='register'),
    path('v1/auth/token/', get_jwt_token, name='token'),
]
