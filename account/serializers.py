from rest_framework import serializers

from .models import User
from .utils import send_activation_code


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        min_length=4, required=True, write_only=True
    )
    password_confirm = serializers.CharField(
        min_length=4, required=True, write_only=True
    )

    class Meta:
        model = User
        fields = (
            'email', 'name', 'password', 'password_confirm'
        )

    def validate(self, attrs):
        password = attrs.get('password')
        password_confirm = attrs.pop('password_confirm')
        if password != password_confirm:
            msg = ('passwords dont match')
            raise serializers.ValidationError(msg)
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        send_activation_code(user.email, user.activation_code, status='register')
        return user


class CreateNewPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=30, required=True)
    password = serializers.CharField(min_length=4, required=True)
    password_confirm = serializers.CharField(min_length=4, required=True)

    def validate_email(self, email):
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError('User not found')
        return email

    def validate_code(self, code):
        if not User.objects.filter(
            activation_code=code,
            is_active=False,
            is_seller=False
            ).exists():
            raise serializers.ValidationError('Invalid activation code')
        return code

    def validate(self, attrs):
        password = attrs.get('password')
        password_confirm = attrs.pop('password_confirm')
        if password != password_confirm:
            raise serializers.ValidationError(
                'passwords dont match'
            )
        return attrs

    def save(self, **kwargs):
        validated_data = self.validated_data
        email = validated_data.get('email')
        code = validated_data.get('code')
        password = validated_data.get('password')
        try:
            user = User.objects.get(
                email=email,
                activation_code=code,
                is_seller=False,
                is_active=False
            )
        except User.DoesNotExist:
            raise serializers.ValidationError(
                'User not found'
            )
        user.is_seller = True
        user.is_active = True
        user.activation_code = ''
        user.set_password(password)
        user.save()
        return user


class UserChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(min_length=4)
    new_password = serializers.CharField(min_length=4)

    def validate_new_password(self, password):
        if not any(char.isdigit() for char in password):
            raise serializers.ValidationError('Password must contain digit.')
        if not any(char.isalpha() for char in password):
            raise serializers.ValidationError('Password must contain alpha.')
        return password

    def validate_old_password(self, password):
        if not any(char.isdigit() for char in password):
            raise serializers.ValidationError('Password must contain digit.')
        if not any(char.isdigit() for char in password):
            raise serializers.ValidationError('Password must contain alpha.')
        return password