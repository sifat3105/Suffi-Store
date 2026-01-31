import random
from django.utils import timezone
from uuid import uuid4
from rest_framework.response import Response
from datetime import timedelta
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from .serializers import UserSerializer
from apps.common.response import custom_response
from apps.user.models import Account, UserOtp
from utils.forget_email import send_password_reset_email

User = get_user_model()

class RegisterAPIView(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        confirm_password = request.data.get("confirm_password")
        name = request.data.get("name", '')
        if not email or not password or not confirm_password:
            return custom_response(
                status="error",
                status_code=status.HTTP_400_BAD_REQUEST,
                message="Email and password and confirm password are required",
                data=None
            )
        try:
            User.objects.get(email=email)
            return custom_response(
                status="error",
                status_code=status.HTTP_400_BAD_REQUEST,
                message="User already exists",
                data=None
            )
        except User.DoesNotExist:
            pass

        if password != confirm_password:
            return custom_response(
                status="error",
                status_code=status.HTTP_400_BAD_REQUEST,
                message="Passwords do not match",
                data=None
            )
        user = User.objects.create_user(email, password=password)
        if not user:
            return custom_response(
                status="error",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message="An error occurred",
                data=None
            )
        Account.objects.create(user=user, name=name)
        refresh = RefreshToken.for_user(user)
        
        return custom_response(
            status="success",
            status_code=status.HTTP_201_CREATED,
            message="User created successfully",
            data={
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "user": UserSerializer(user).data
            }
        )

class LoginAPIView(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        user = authenticate(email=email, password=password)
        if not user:
            return custom_response(
                status="error",
                status_code=status.HTTP_401_UNAUTHORIZED,
                message="Invalid email or password",
                data=None
            )

        refresh = RefreshToken.for_user(user)

        return custom_response(
            status="success",
            status_code=status.HTTP_200_OK,
            message="Login successful",
            data={
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "user": UserSerializer(user).data
            }
        )


class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            return custom_response(
                status="error",
                status_code=status.HTTP_400_BAD_REQUEST,
                message="Token is invalid or expired",
                data=None
            )

        return custom_response(
            status="success",
            status_code=status.HTTP_200_OK,
            message="Token refreshed successfully",
            data=serializer.validated_data 
        )
    
class LogoutAPIView(APIView):
    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            token = RefreshToken(refresh_token)
            token.blacklist()
            return custom_response(
                status="success",
                status_code=status.HTTP_200_OK,
                message="Logout successful",
                data=None
            )
        except Exception as e:
            return custom_response(
                status="error",
                status_code=status.HTTP_400_BAD_REQUEST,
                message="Invalid token",
                data=None
            )
        
class ForgotPasswordAPIView(APIView):
    def post(self, request):
        email = request.data.get("email")
        if not email:
            return Response(
                status="error",
                status_code=status.HTTP_400_BAD_REQUEST,
                message="Email is required",
                data=None
            )

        user = User.objects.filter(email=email).first()
        if not user:
            return Response(
                status="error",
                status_code=status.HTTP_404_NOT_FOUND,
                message="User not found",
                data=None
            )

        user_otp, created = UserOtp.objects.get_or_create(user=user)

        user_otp.otp = random.randint(10000, 99999)
        user_otp.token = uuid4()
        user_otp.save()

        # Send OTP email
        send_password_reset_email(user.email, user_otp.otp)
        return Response({
            "status": "success",
            "status_code": status.HTTP_200_OK,
            "message": "OTP sent to your email.",
            "token": str(user_otp.token)
        })
        
    

class VerifyResetCodeAPIView(APIView):
    def post(self, request):
        otp = request.data.get("otp")
        email = request.data.get("email")
        
        if not otp or not email:
            return Response({
                "status": "error",
                "status_code": status.HTTP_400_BAD_REQUEST,
                "message": "OTP and email are required."
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            email_match = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({
                "status": "error",
                "status_code": status.HTTP_404_NOT_FOUND,
                "message": "Email not found in our records. Please sign up first."
            }, status=status.HTTP_404_NOT_FOUND)

        try:
            match = UserOtp.objects.get(otp=otp)
        except UserOtp.DoesNotExist:
            return Response({
                "status": "error",
                "status_code": status.HTTP_400_BAD_REQUEST,
                "message": "Invalid OTP."
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # OTP expiry check
        expiry_time = match.updated_at + timedelta(minutes=5)
        if timezone.now() > expiry_time:
            return Response({
                "status": "error",
                "status_code": status.HTTP_400_BAD_REQUEST,
                "message": "OTP has expired."
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            "status": "success",
            "status_code": status.HTTP_200_OK,
            "message": "OTP verified successfully.",
            "token": match.token
        }, status=status.HTTP_200_OK)
    

class SetNewPasswordView(APIView):
    def post(self, request):
        new_password = request.data.get("new_password")
        confirm_password = request.data.get("confirm_password")
        token = request.data.get("token")

        try:
            obj = UserOtp.objects.get(token=token)
        except UserOtp.DoesNotExist:
            error_response = {
                "status": "error",
                "status_code": status.HTTP_404_NOT_FOUND,
                "message": "Invalid or not given token."
            }
            return Response(error_response, status=status.HTTP_404_NOT_FOUND)
        if not new_password:
            error_response = {
                "status": "error",
                "status_code": status.HTTP_400_BAD_REQUEST,
                "message": "New password is required."
            }
            return Response(error_response, status=status.HTTP_400_BAD_REQUEST)
        if new_password != confirm_password:
            error_response = {
                "status": "error",
                "status_code": status.HTTP_400_BAD_REQUEST,
                "message": "Passwords do not match."
            }
            return Response(error_response, status=status.HTTP_400_BAD_REQUEST)
        obj.user.set_password(new_password)
        obj.user.save()
        obj.delete()
        response = {
            "status": "success",
            "status_code": status.HTTP_200_OK,
            "message": "Password reset successfully."
        }
        return Response(response, status=status.HTTP_200_OK)
