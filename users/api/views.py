import json
import os

from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.http import HttpRequest
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser

from users.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ForgotPasswordViewSet(APIView):

    def post(self, request):
        data = request.data
        email = data['email']
        user = User.objects.filter(email=email).first()

        try:
            if user.email:
                form = PasswordResetForm({'email': user.email})

                assert form.is_valid()
                request = HttpRequest()
                request.META['SERVER_NAME'] = "127.0.0.1:8000"
                request.META['SERVER_PORT'] = '80'
                form.save(
                    request=request,
                    from_email="rizqimaulana.1988@gmail.com",
                    email_template_name='registration/password_reset_email.html')
        except Exception as e:
            print(e)

        message = """ We've emailed you instructions for setting your password, if an account exists with the email you entered. You should receive them shortly.
    If you don't receive an email, please make sure you've entered the address you registered with, and check your spam folder"""

        return Response({
            'message': message
        })
