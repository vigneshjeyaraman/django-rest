from django.db import models
from django.contrib.auth.models import AbstractUser

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now = True)

class User(AbstractUser, BaseModel):
    email = models.EmailField('Email', unique=True, blank=False, null=False)
    username = models.CharField('Username', null=False, blank=False, max_length=25)
    phone_number = models.CharField('Phone Number', null=False, blank=False, max_length=30)
    is_verified = models.BooleanField('Verified', default=False)
    is_approved = models.BooleanField('Approved', default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username',)

    class Meta:
        ordering = ['id']

class Otp(BaseModel):
    """
        UserToken models to save the user token.
    """

    VERIFICATION = 1
    FORGOT_PASSWORD = 2

    OTP_CHOICES = (
        (VERIFICATION, 'Verification'),
        (FORGOT_PASSWORD, 'Forgot Password')
    )
    customer = models.ForeignKey(User, blank=False, on_delete=models.CASCADE, related_name='user_otp')
    customer_otp = models.IntegerField('User Otp', blank=True,null=True)
    expired_at = models.DateTimeField(null=True)
    otp_type = models.IntegerField('Otp type', choices=OTP_CHOICES, blank=False,null=True)
    is_used = models.BooleanField('Is Used', default=False)

