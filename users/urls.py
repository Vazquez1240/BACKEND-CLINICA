from apirest.urls import drf_router
from django.urls import path
from .viewsets import UserViewSet, AuthTokenViewset, TokenRefreshViewSet, RegisterViewSet, TokenVerifyViewSet, Logout

urlpatterns = [
]

drf_router.register(r'users', UserViewSet)
drf_router.register(r'login', AuthTokenViewset, basename='auth_token_login')
drf_router.register(r'logout', Logout, basename='aut_token_logout')
drf_router.register('refresh-token', TokenRefreshViewSet, basename='auth_token_refresh')
drf_router.register(r'register', RegisterViewSet, basename='user_register')
drf_router.register(r'verify-token', TokenVerifyViewSet, basename='token_verify')

urlpatterns += drf_router.urls