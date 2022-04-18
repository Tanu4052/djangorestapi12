from .views import RegisterAPI,LoginAPI
from django.urls import path,include
from knox import views as knox_views
from rest_framework.permissions import IsAuthenticated
from .views import ChangePasswordView
from .models import password_reset_token_created
#from .settings import django_rest_passwordreset
app_name='REST'


urlpatterns = [
    #path('api/register/',RegisterView.as_view(),),
    #path('validate_phone/',ValidatePhoneSendOTP.as_view()),
    
    path('api/register/',RegisterAPI.as_view(), name='register'),
    path('api/login/',LoginAPI.as_view(),name='login'),
    path('api/logout/',knox_views.LogoutView.as_view(),name='logout'),
    path('api/logoutall/',knox_views.LogoutAllView.as_view(),name='logoutall'),
    path('api/change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('api/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
]