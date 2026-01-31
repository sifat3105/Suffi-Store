from django.urls import path
from .views import LoginAPIView, CustomTokenRefreshView, RegisterAPIView, LogoutAPIView, ForgotPasswordAPIView, VerifyResetCodeAPIView, SetNewPasswordView

urlpatterns = [
    path('register', RegisterAPIView.as_view(), name='register'),
    path('login', LoginAPIView.as_view(), name='login'),
    path('token/refresh', CustomTokenRefreshView.as_view(), name='token-refresh'),
    path('logout', LogoutAPIView.as_view(), name='logout'),
    path('forgot-password-request/', ForgotPasswordAPIView.as_view(), name='forgot-password'),
    path('verify-reset-code/', VerifyResetCodeAPIView.as_view(), name='verify-reset-code'),
    path('reset-password/', SetNewPasswordView.as_view(), name='reset-password'),
]