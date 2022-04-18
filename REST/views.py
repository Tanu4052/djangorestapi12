from django.shortcuts import render

# Create your views here.
from rest_framework import status
from django.shortcuts import render,redirect,get_object_or_404
from rest_framework.views import  APIView
import random
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework import permissions
from django.contrib.auth import login
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import generics,permissions
from knox.models import AuthToken
from .serializers import UserSerializer,RegisterSerializer ,LoginSerializer
from django.http import HttpResponse
#django.http import HttpResponse
from django.template import Context,loader
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from .serializers import ChangePasswordSerializer
#from .forms import*
from .models import*
from django.contrib.auth.models import User
    
# Create your views here.
#register api
#from django.views.decorators.csrf import csrf_protect
#from django.views.decorators.csrf import csrf_exempt
#@csrf_protect

class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    #permission_classes = [permissions.AllowAny,]
    permission_classes = [permissions.IsAuthenticated,]
    authentication_classes = [BasicAuthentication,]

    def post(self,request,*args,**kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user=serializer.save()
        #return Response(data, status=status.HTTP_200_OK)

        
        return Response({
            "user":UserSerializer(user,context=self.get_serializer_context()).data,
            "token":AuthToken.objects.create(user)[1]
       })


    def get(self,request,*args,**kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True )
        user=serializer.save()
        return Response(data, status=status.HTTP_200_OK)
       # pass

#@csrf_exempt
#login api
class LoginAPI(KnoxLoginView):
    serializer_class=LoginSerializer
    permissions_classes = [permissions.AllowAny,]
    permission_classes = [IsAuthenticated,]
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    #permissions_classes = [permissions.AllowAny,]
    
    

    def post(self,request,format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)   
        user = serializer.validated_data['user']
        login(request,user)
        #user=serializer.save()
        return super(LoginAPI,self).post(request,format=None)
       # return Response(data, status=status.HTTP_200_OK)

    def get(self,request,*Args,**kwargs ):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)   
        user = serializer.validated_data['user']
        login(request,user)
        return super(LoginAPI,self).post(request,format=None)
        #return Response(data, status=status.HTTP_200_OK)
     #   pass

class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
