from rest_framework import serializers
from .models import User, Customer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username', 'password', 'email','role']
    def get_jwt_token(self,data):

        user = authenticate(username=data['username'],password=data['password'])
        if not user:
            return {'message':'invalid credentials','data':{}}
        refersh = RefreshToken.for_user(user)
        return {'message':'login success','data':{'token':{'refresh':str(refersh),'access':str(refersh.access_token  )}}} 

class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = ['id','username','password','email']
        extra_kwargs = {
            'password':{'write_only':True}
        }
    def create(self, validated_data):
        password = validated_data.pop('password',None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance 



class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password=serializers.CharField()
    def validate(self, data):
        if not User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError('account not found')
        return data
    def get_jwt_token(self,data):

        user = authenticate(username=data['username'],password=data['password'])
        if not user:
            return {'message':'invalid credentials','data':{}}
        refersh = RefreshToken.for_user(user)
        return {'refresh':str(refersh),'access':str(refersh.access_token  ),'user': UserSerializer(user).data}
    