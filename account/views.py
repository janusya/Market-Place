from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from . import serializers
from .serializers import RegistrationSerializer, CreateNewPasswordSerializer
from .models import User
from rest_framework_simplejwt.tokens import RefreshToken
from .utils import send_activation_code


class RegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        serializer = RegistrationSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                'Registration was successful, please check your email!',
            )


class ActivationView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, code, email):
        user = User.objects.get(
            email=email, activation_code=code
        )
        msg = (
            'User not found',
            'Account was successfully activated'
        )
        if not user:
            return Response(msg[0], 400)
        user.is_seller = True
        user.is_active = True
        user.activation_code = ''
        user.save()
        return Response(msg[-1], 200)


class LogoutView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(token=refresh_token)
            token.blacklist()
            return Response("Try again!")
        except Exception as e:
            return Response('You have successfully logged out of your account!')


class ForgotPasswordView(APIView):
    def get(self, request, email):
        user = get_object_or_404(User, email=email)
        user.is_active = False
        user.is_seller = False
        user.create_activation_code()
        user.save()
        send_activation_code(
            email=user.email,
            code=user.activation_code,
            status='forgot_password'
        )
        return Response('The message has been sent to your email!', status=200)


class CompleteResetPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = CreateNewPasswordSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response('You have successfully changed your password!', status=200)


class UserChangePassword(APIView):
    """
        if old password is correct set new password
    """

    serializer_class = serializers.UserChangePasswordSerializer
    permission_classes = (
        IsAuthenticated,
    )

    @swagger_auto_schema(request_body=serializer_class)
    def put(self, request):
        srz_data = self.serializer_class(data=request.data)
        if srz_data.is_valid(raise_exception=True):
            data = srz_data.validated_data
            if request.user.check_password(data['old_password']):
                request.user.set_password(data['new_password'])
                request.user.save()
                return Response({'password changed.'}, status=status.HTTP_200_OK)
            return Response({'old password is wrong.'}, status=status.HTTP_400_BAD_REQUEST)
