from rest_framework import serializers
from django.contrib.auth.models import User

from .models import profile
from .util import sendEmail


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = profile
        fields = ['fullname', 'username', 'phone', 'email', 'gender', 'profile_pics', 'bio']


class RegistrationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    profile_pics = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = profile
        fields = ['fullname', 'username', 'phone', 'email', 'gender', 'profile_pics', 'bio', 'password1', 'password2']

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError({'password2': 'Passwords did not match.'})
        return data

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('email already exists.')
        return value

    def create(self, validated_data):
        password = validated_data.pop('password1')
        validated_data.pop('password2')
        username = validated_data.pop('username')
        email = validated_data.pop('email')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
        )

        profile_obj = profile.objects.create(
            user=user,
            username=username,
            email=email,
            fullname=validated_data['fullname'],
            phone=validated_data['phone'],
            gender=validated_data['gender'],
            profile_pics=validated_data.get('profile_pics', ''),
            bio=validated_data.get('bio', ''),
        )

        sendEmail(username, email)
        return profile_obj

