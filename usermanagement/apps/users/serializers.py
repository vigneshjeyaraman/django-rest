from django.db.models import Q
from django.contrib.auth import authenticate
from rest_framework.serializers import ModelSerializer, ValidationError, EmailField, CharField, IntegerField
from rest_framework.authtoken.models import Token
from .models import User

class UserSerializer(ModelSerializer):
    """
        Serializer to serialize users information.
    """
    class Meta:
        model = User
        fields = ('username', 'email', 'phone_number', 'is_verified', 'is_approved')

class SignupSerializer(ModelSerializer):
    """
        Serializer to validate users information provided during signup.
    """
    def validate(self, attrs):
        email = attrs['email'].lower()
        if User.objects.filter(Q(email=email) | Q(phone_number=attrs['phone_number'])).exists():
            raise ValidationError("You are already registered with us!!!")
        return attrs
    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_data['email'] = validated_data['email'].lower()
        user_obj = User.objects.create(**validated_data)
        user_obj.set_password(password)
        user_obj.save()
        return user_obj
    class Meta:
        model = User
        fields = ('username', 'email', 'phone_number','password')

class LoginSerializer(ModelSerializer):
    """
        Login serializer to validate login info.
    """
    email = EmailField(required=True, min_length=3, max_length=70)
    password = CharField(required=True, write_only=True, min_length=8, max_length=20)
    def validate(self, attrs):
        email = attrs['email'].lower()
        user_obj = authenticate(email=email, password=attrs['password'])
        if not user_obj:
            raise ValidationError("Please signup to continue!!")
        if not user_obj.is_verified:
            raise ValidationError("Please verify to continue!!")
        if not user_obj.is_approved:
            raise ValidationError("Contact Admin!!")
        attrs['user'] = user_obj
        return attrs
    
    class Meta:
        model = User
        fields = ('email','password')

class VerifyOTPSerializer(ModelSerializer):
    email = EmailField(required=True, min_length=3, max_length=70)
    otp = IntegerField(required=True)

    def validate(self, attrs):
        user_obj = User.objects.prefetch_related('user_otp').filter(email=attrs['email']).first()
        if not user_obj:
            raise ValidationError("Invalid email!!")
        if user_obj.user_otp.get().customer_otp != attrs['otp']:
            raise ValidationError("Invalid OTP!!")
        user_obj.is_verified = True
        user_obj.save()
        return attrs
    
    class Meta:
        model = User
        fields = ('email','otp')

class ApproveUserSerializer(ModelSerializer):
    email = EmailField(required=True, min_length=3, max_length=70)
    user_id = IntegerField(required=True)

    def validate(self, attrs):
        user_obj = User.objects.filter(id=attrs['user_id'], email=attrs['email']).first()
        if not user_obj:
            raise ValidationError("Invalid User!!")
        user_obj.is_approved = True
        user_obj.save()
        return attrs
    class Meta:
        model = User
        fields = ("email","user_id")