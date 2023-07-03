from rest_framework.serializers import ModelSerializer
from .models import *
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import make_password

#---------------------------------------------------------------------------------------------------------------
# This Class is generated access and refresh token this class inherite with TokenObtainSerializer 
# and this is custom class 
# Use of this class is we can pass the value of login user with refresh and access token
# Example: data['username']=self.user.username
# Output:
# {
#       "refresh":"token",
#       "access":"token",
#       "username":"Loginuser Username"
# }     
class MyTokenObtainPairSerializer(TokenObtainSerializer):
    token_class = RefreshToken

    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)
        return data
#------------------------------------------------------------------------------------------------------------------

# This Serializers is use to create update delete retrive data and generate the inbuilt validations if field is empty
# This Serializers is use to Convert JSON formated data into python data  and python data to JSON data for responce
# And store the data in django models such as python data formate 
# We Use Nested Serializer Because We can easyly read ForeignKey Data    

class CompanySerializer(ModelSerializer):

    class Meta:
        model=Company
        fields="__all__"

class DepartmentSerializer(ModelSerializer):
    class Meta:
        model=Department
        fields="__all__"

class DepartmentListSerializer(ModelSerializer):
    company=CompanySerializer()
    class Meta:
        model=Department
        fields=("id","name","company")


class ProjectSerializer(ModelSerializer):
    class Meta:
        model=Project
        fields="__all__"

# This Serializer will use to  Create user and create method is use to save and make the password in hash formate
 
class UserSerializer(ModelSerializer):
    class Meta:
        model=User
        fields=("id","first_name","last_name","username","email","password")
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_data["password"] = make_password(password)
        instance = super().create(validated_data)
        instance.save()
        return instance

class EmployeeSerializer(ModelSerializer):
    class Meta:
        model=Employee
        fields=("id","user","name","phone","is_manager","department","projects")
    


class EmployeeListSerializer(ModelSerializer):
    user=UserSerializer()
    projects=ProjectSerializer(many=True, read_only=True)
    department=DepartmentListSerializer()
    class Meta:
        model=Employee
        fields=("id","user","name","phone","is_manager","department","projects")



#------------------------------------------------------------------------------------------------------------------