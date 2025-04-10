from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from knox.views import LoginView as KnoxLoginView
from knox.views import LogoutView as KnoxLogoutView
from knox.models import AuthToken
from django.contrib.auth import login
from rest_framework.authtoken.serializers import AuthTokenSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import *
from .serializers import *

# Register view
class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        operation_description="Register a new user and receive an authentication token",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['username', 'email', 'password'],
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, description='Unique username'),
                'email': openapi.Schema(type=openapi.TYPE_STRING, format='email', description='User email'),
                'first_name': openapi.Schema(type=openapi.TYPE_STRING, description='First name (optional)', default=''),
                'last_name': openapi.Schema(type=openapi.TYPE_STRING, description='Last name (optional)', default=''),
                'password': openapi.Schema(type=openapi.TYPE_STRING, format='password', description='Password'),
                'phone': openapi.Schema(type=openapi.TYPE_STRING, description='Phone number (optional)'),
            },
        ),
        responses={
            201: openapi.Response(
                description="User created successfully",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'user': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                'username': openapi.Schema(type=openapi.TYPE_STRING),
                                'email': openapi.Schema(type=openapi.TYPE_STRING, format='email'),
                                'first_name': openapi.Schema(type=openapi.TYPE_STRING),
                                'last_name': openapi.Schema(type=openapi.TYPE_STRING),
                                'profile': openapi.Schema(
                                    type=openapi.TYPE_OBJECT,
                                    properties={
                                        'phone': openapi.Schema(type=openapi.TYPE_STRING, nullable=True),
                                        'created_at': openapi.Schema(type=openapi.TYPE_STRING, format='date-time'),
                                        'updated_at': openapi.Schema(type=openapi.TYPE_STRING, format='date-time'),
                                    }
                                ),
                            }
                        ),
                        'token': openapi.Schema(type=openapi.TYPE_STRING, description='Authentication token'),
                    }
                )
            ),
            400: "Bad Request - Validation errors"
        }
    )
    def post(self, request, format=None):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            _, token = AuthToken.objects.create(user)
            login(request, user)
            return Response({
                "user": UserSerializer(user).data,
                "token": token
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Login view
class LoginView(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    @swagger_auto_schema(
        operation_description="Log in a user and receive an authentication token",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['username', 'password'],
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, description='Username'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, format='password', description='Password'),
            },
        ),
        responses={
            200: openapi.Response(
                description="Login successful",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'expiry': openapi.Schema(type=openapi.TYPE_STRING, format='date-time', nullable=True),
                        'token': openapi.Schema(type=openapi.TYPE_STRING, description='Authentication token'),
                    }
                )
            ),
            400: "Bad Request - Invalid credentials"
        }
    )
    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginView, self).post(request, format=None)

# Logout view
class LogoutView(KnoxLogoutView):
    @swagger_auto_schema(
        operation_description="Log out a user and invalidate their token",
        responses={204: "No Content - Logout successful"}
    )
    def post(self, request, format=None):
        return super(LogoutView, self).post(request, format=None)

# User viewset
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return User.objects.all()
        return User.objects.filter(id=self.request.user.id)

    @swagger_auto_schema(operation_description="List all users (admin) or the current user")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Create a new user (admin only)")
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

# RoomType viewset
class RoomTypeViewSet(viewsets.ModelViewSet):
    queryset = RoomType.objects.all()
    serializer_class = RoomTypeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(operation_description="List all room types (public)")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Create a new room type (authenticated)")
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

# Room viewset
class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(operation_description="List all rooms (public)")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

# ServiceType viewset
class ServiceTypeViewSet(viewsets.ModelViewSet):
    queryset = ServiceType.objects.all()
    serializer_class = ServiceTypeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(operation_description="List all service types (public)")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

# Service viewset
class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(operation_description="List all services (public)")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

# Reservation viewset
class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Reservation.objects.all()
        return Reservation.objects.filter(user_id=self.request.user)

    @swagger_auto_schema(operation_description="List user's reservations (authenticated)")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

# ReservationService viewset
class ReservationServiceViewSet(viewsets.ModelViewSet):
    queryset = ReservationService.objects.all()
    serializer_class = ReservationServiceSerializer
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(operation_description="List reservation services (authenticated)")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

# Payment viewset
class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Payment.objects.all()
        return Payment.objects.filter(reservation_id__user_id=self.request.user)

    @swagger_auto_schema(operation_description="List user's payments (authenticated)")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

# Review viewset
class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Review.objects.all()
        return Review.objects.filter(user_id=self.request.user)

    @swagger_auto_schema(operation_description="List user's reviews (authenticated)")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)