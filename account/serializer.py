from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth.hashers import make_password

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)


    class Meta:
        model = CustomUser
        fields = ("username", "email", "password", "confirm_password")

    def validate(self, attrs):
        confirm = attrs.pop('confirm_password')
        password = attrs.get('password')

        if confirm != password:
            raise serializers.ValidationError("Passwords do not match")
        attrs["password"] = make_password(password)
        return attrs
    
    def create(self, validated_data):
        validated_data.pop("confirm_password")
        validated_data["password"] = make_password(validated_data["password"])
        return CustomUser.objects.create(**validated_data)
    

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

class RefreshSerializer(serializers.Serializer):
    token = serializers.CharField(write_only=True)

class LogoutSerializer(serializers.Serializer):
    token = serializers.CharField(write_only=True)