from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import User, OTP
from .serializers import UserSerializer
from .utils import otp_code_expire


class SignInViewSet(ViewSet):
    @swagger_auto_schema(
        operation_description="Sign in ",
        operation_summary="Enter phone number",
        responses={200: 'otp_key'},
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, maxLength=13),
            },
            required=['username']
        ),
        tags=['auth']

    )
    def sign_in(self, request, *args, **kwargs):
        data = request.data
        user = User.objects.filter(username=data.get('username')).first()
        if user:
            otp_obj = OTP.objects.create(otp_user=user)
            otp_obj.save()
            return Response(data={"otp_key": otp_obj.otp_key}, status=status.HTTP_200_OK)
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            otp_obj = OTP.objects.create(otp_user=serializer.instance)
            otp_obj.save()
            return Response(data={"otp_key": otp_obj.otp_key}, status=status.HTTP_200_OK)
        return Response({"error": "Input valid phone number"}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Verify Sign in ",
        operation_summary="Enter otp code with key",
        responses={200: 'ok'},
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'otp_key': openapi.Schema(type=openapi.TYPE_STRING, maxLength=100),
                'otp_code': openapi.Schema(type=openapi.TYPE_INTEGER, maxLength=20),
            },
            required=['otp_key', 'otp_code']
        ),
        tags=['auth']

    )
    def verify_sign_in(self, request, *args, **kwargs):
        otp_key = request.data.get('otp_key')
        otp_code = request.data.get('otp_code')
        otp_obj = OTP.objects.filter(otp_key=otp_key, otp_code=otp_code).first()
        if otp_obj:
            if otp_code_expire(otp_obj.created_at):
                return Response({"ok": True}, status=status.HTTP_200_OK)
            return Response({"error": "Expired"}, status.HTTP_400_BAD_REQUEST)
        return Response({"error": "Invalid code"}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Resend otp",
        operation_summary="Enter otp key to get new otp",
        responses={200: 'otp_key'},
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'otp_key': openapi.Schema(type=openapi.TYPE_STRING, maxLength=100),
            },
            required=['otp_key']
        ),
        tags=['auth']

    )
    def resend_otp_code(self, request, *args, **kwargs):
        otp_key = request.data.get('otp_key')
        otp_obj = OTP.objects.filter(otp_key=otp_key).first()
        if not otp_obj:
            return Response({"error": "Invalid otp_key"}, status.HTTP_400_BAD_REQUEST)
        new_otp_obj = OTP.objects.create(otp_user=otp_obj.otp_user)
        new_otp_obj.save()
        otp_obj.delete()
        return Response({"otp_key": new_otp_obj.otp_key}, status.HTTP_200_OK)
