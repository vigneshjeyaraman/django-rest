from django.conf.urls import url
from apps.users import views
urlpatterns = [
    url('signup', views.SignupView.as_view({"post":"create"}),name='signup'),
    url('login', views.Login.as_view({"post":"create"}),name='login'),
    url('verifyotp', views.VerifyOtp.as_view({"put":"update"}),name='verifyotp'),
    url('approveuser', views.ApproveUser.as_view({"put":"update"}),name='approveuser'),
    url('listverifieduser', views.ListVerifiedUsers.as_view({"get":"list"}),name='listverifiedusers'),
    url('listalluser', views.ListAllUsers.as_view({"get":"list"}),name='listallusers'),
]
