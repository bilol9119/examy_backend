from django.urls import path
from .views import SignInViewSet

urlpatterns = [
    path('sign-in/', SignInViewSet.as_view({"post": "sign_in"})),
    path('sign-in/verify/', SignInViewSet.as_view({"post": "verify_sign_in"})),
    path('sign-in/resend/', SignInViewSet.as_view({"post": "resend_otp_code"})),
]
