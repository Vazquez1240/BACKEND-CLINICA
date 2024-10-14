
from .serializers import UserSerializer
from rest_framework.parsers import JSONParser
from .permissions import IsAuthenticatedAndObjUserOrIsStaff
from rest_framework import exceptions
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken, TokenBackendError
from rest_framework.permissions import AllowAny
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework_simplejwt.tokens import UntypedToken
from users.managers import CustomRefreshToken
from rest_framework.decorators import action
from .models import User

class UserViewSet(viewsets.ModelViewSet):
    parser_classes = [JSONParser]
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticatedAndObjUserOrIsStaff]
    http_method_names = ['get', 'options', 'head']

    # Define the queryset
    queryset = User.objects.all()

    def get_queryset(self):
        if self.request.user.is_superuser:
            return User.objects.all()
        elif self.request.user.is_staff:
            return User.objects.all()
        elif self.request.user.is_authenticated:
            return User.objects.filter(pk=self.request.user.pk)
        else:
            raise exceptions.PermissionDenied('Forbidden')

class Logout(viewsets.ViewSet):
    permission_classes = [IsAuthenticatedAndObjUserOrIsStaff]
    parser_classes = [MultiPartParser, FormParser]
    http_method_names = ['post', 'options', 'head']

    def create(self, request):
        try:
            refresh_token = request.data.get('refresh')
            token = CustomRefreshToken(refresh_token)
            token.blacklist()

            return Response({'token': 'Delete token'}, status=status.HTTP_205_RESET_CONTENT)

        except TokenError as e:
            return Response({'error':'El token ya se encuentra en la lista negra'}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class RegisterViewSet(viewsets.ViewSet):
    http_method_names = ['post', 'options', 'head']
    permission_classes = [AllowAny]

    def create(self, request):
        print(request.data['username'],' data')
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'status': '201'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AuthTokenViewset(viewsets.ViewSet):
    http_method_names = ['post', 'options', 'head']
    permission_classes = [AllowAny]

    def create(self, request):
        view = TokenObtainPairView.as_view()
        try:
            response = view(request._request)
            data = response.data
            if 'refresh' in data and 'access' in data:
                return Response({
                    'refresh': data['refresh'],
                    'access': data['access'],
                }, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid response from token view'}, status=status.HTTP_400_BAD_REQUEST)
        except TokenError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except InvalidToken as e:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
        except TokenBackendError as e:
            return Response({'error': 'Token backend error'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class TokenRefreshViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    def create(self, request):
        try:
            refresh_token = request.data.get('refresh')
            if not refresh_token:
                return Response({'error': 'Refresh token is required'}, status=status.HTTP_400_BAD_REQUEST)

            refresh = CustomRefreshToken(refresh_token)
            print('pasando')
            refresh.verify()
            access_token = refresh.get_new_access_token()  # Obtiene un nuevo access token

            data = {
                'access': access_token,
                'refresh': str(refresh)
            }
            return Response(data, status=status.HTTP_200_OK)
        except TokenError as e:
             return Response({'error': 'Refresh token is invalid.'},
                                status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({'error': f'Unexpected error occurred: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)


class TokenVerifyViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    @action(detail=False, methods=['post'])
    def verify(self, request):
        token = request.data.get('token')
        try:
            UntypedToken(token)
        except InvalidToken as e:
            print('Invalid token error:', e)
            return Response({'detail': str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        except TokenError as e:
            print('Token error:', e)
            return Response({'detail': str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            print('General error:', e)
            return Response({'detail': 'Unexpected error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'detail': 'Token is valid'}, status=status.HTTP_200_OK)