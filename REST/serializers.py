from rest_framework import serializers
from django.contrib.auth.models import User
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username','email')

#register serializers
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=('id','username','email','password',)
        extra_kwargs={'password':{'write_only':True}#hone_number':{'write_only':True}
                      }
        #queryset=User.objects.all()

    def create(self,validated_data):
        user = User.objects.create_user(validated_data['username'],validated_data['email'],validated_data['password'])#validated_data['phone_number']\)
        return user
    
    #def update(self,instance,validated_data):
     #   instance.username=validated_data.get('username',instance.username)
      #  instance.email=validated_data.get('email',instance.email)
       # instance.password=validated_data.get('password',instance.password)
        #instance.save()
         #return instance
         
         
            
    
#login seializer
class LoginSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('username','password')
        extra_kwargs={'password':{'write_only':True}} 

    def create(self,validated_data):
        user = User.objects.create_user(validated_data['username'],validated_data['password'])
        return user
    
    
class ChangePasswordSerializer(serializers.Serializer):
    model = User

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

