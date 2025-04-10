from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *

# Registration serializer
class RegisterSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(write_only=True, required=False, allow_blank=True)  # For UserProfile
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password', 'phone']

    def create(self, validated_data):
        phone = validated_data.pop('phone', None)  # Extract phone for UserProfile
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            password=validated_data['password']
        )
        # Create associated UserProfile
        if phone:
            UserProfile.objects.create(user=user, phone=phone)
        else:
            UserProfile.objects.create(user=user)  # Create profile even if phone is not provided
        return user

# Existing serializers (unchanged, included for context)
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['phone', 'created_at', 'updated_at']

class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'profile']

# ... (other serializers remain the same)

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['phone', 'created_at', 'updated_at']

class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'profile']

class RoomTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomType
        fields = '__all__'

class RoomSerializer(serializers.ModelSerializer):
    type_id = RoomTypeSerializer()

    class Meta:
        model = Room
        fields = '__all__'

class ServiceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceType
        fields = '__all__'

class ServiceSerializer(serializers.ModelSerializer):
    service_type_id = ServiceTypeSerializer()

    class Meta:
        model = Service
        fields = '__all__'

class ReservationSerializer(serializers.ModelSerializer):
    user_id = UserSerializer()
    room_id = RoomSerializer()

    class Meta:
        model = Reservation
        fields = '__all__'

class ReservationServiceSerializer(serializers.ModelSerializer):
    reservation_id = ReservationSerializer()
    service_id = ServiceSerializer()

    class Meta:
        model = ReservationService
        fields = '__all__'

class PaymentSerializer(serializers.ModelSerializer):
    reservation_id = ReservationSerializer()

    class Meta:
        model = Payment
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    user_id = UserSerializer()
    reservation_id = ReservationSerializer()

    class Meta:
        model = Review
        fields = '__all__'