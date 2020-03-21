import random
from django.shortcuts import render

# Create your views here.
from rest_framework import mixins, viewsets, views, permissions
from .serializers import (SignupSerializer, UserSerializer, LoginSerializer, 
                          VerifyOTPSerializer, ApproveUserSerializer)
from response import CustomResponse
from rest_framework.authtoken.models import Token
from .models import Otp, User
from .utils import send_email
from pagination import Pagination

class SignupView(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
        Signup API to let user register with us.
    """

    def create(self, request):
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_obj = serializer.save()
        serializer = UserSerializer(user_obj)
        token, created = Token.objects.get_or_create(user=user_obj)
        otp = random.randint(1000,9999)
        Otp.objects.get_or_create(customer=user_obj, otp_type= Otp.VERIFICATION, customer_otp=otp)
        data = serializer.data
        data.update({"token":token.key, "otp":otp})
        ## For now we are showing otp in response later we can integrate send grid to send otp over email.
        try:
            send_email(user_obj.email, otp)
        except:
            pass
        return CustomResponse(data)

class Login(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
        Login API to let user login into the app. It will check whether user verified email else 
        it will not let user login into the system. Also, it will check whether user is approved by the 
        admin.
    """

    def create(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_obj = serializer.validated_data.get('user')
        serializer = UserSerializer(user_obj)
        token, created = Token.objects.get_or_create(user=user_obj)
        data = serializer.data
        data.update({"token":token.key})
        return CustomResponse(data)

class VerifyOtp(mixins.UpdateModelMixin, viewsets.GenericViewSet):
    """
        To let user verify the otp
    """
    def update(self, request):
        serializers = VerifyOTPSerializer(data=request.data)
        serializers.is_valid(raise_exception=True)
        return CustomResponse(data={"message":"OTP verified successfully"})

class ListVerifiedUsers(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
        It will give the paginated response if page_size is passed on params and it will list all users in one
        go. Also this API endpoint will be accessed only by admin token.
        It will list only the users who verified their email.
    """
    pagination_class = Pagination
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAdminUser,)
    def list(self, request):
        user_obj = User.objects.filter(is_verified = True).all()
        pagination_class = self.pagination_class()
        page = pagination_class.paginate_queryset(user_obj, request)
        if page is not None:
            serializer = self.serializer_class(page, many=True, context={'request': request})
            return CustomResponse(pagination_class.get_paginated_response(serializer.data).data)
        serializer = self.serializer_class(user_obj, many=True)
        return CustomResponse(data=serializer.data)

class ListAllUsers(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
        This API is similar to above one but it will list all the users in system except admin.
    """
    pagination_class = Pagination
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAdminUser,)
    def list(self, request):
        user_obj = User.objects.exclude(is_superuser=True).all()
        pagination_class = self.pagination_class()
        page = pagination_class.paginate_queryset(user_obj, request)
        if page is not None:
            serializer = self.serializer_class(page, many=True, context={'request': request})
            return CustomResponse(pagination_class.get_paginated_response(serializer.data).data)
        serializer = self.serializer_class(user_obj, many=True)
        return CustomResponse(data=serializer.data)

class ApproveUser(mixins.UpdateModelMixin, viewsets.GenericViewSet):
    """
        API for admin to approve user to use app.
    """
    permission_classes = (permissions.IsAdminUser,)
    def update(self, request):
        serializer = ApproveUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return CustomResponse(data={"message":"User is approved now!!"})
