from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet,ViewSet
from rest_framework.response import Response
from .serializers import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny,IsAdminUser,IsAuthenticated
# Create your views here.
from .models import *
# ------------------------------------------------------------------------------------------------------
# We can Create Update Delete And Retrieve this company data and this operations is perform by only admin
class CompanyViewSet(ModelViewSet):
    queryset=Company.objects.all()
    serializer_class=CompanySerializer
    permission_classes=[IsAdminUser]
# ------------------------------------------------------------------------------------------------------

# ------------------------------------------------------------------------------------------------------
# We can Create Update Delete And Retrive this department data and this operations is perform by only admin
# This list  method is usefull to the admin can get the department data so the admin can read the
# Foreignkey data
# This Rertrieve method is use full to show perticular department   
class DepartmentViewSet(ModelViewSet):
    queryset=Department.objects.all()
    serializer_class=DepartmentSerializer
    permission_classes=[IsAdminUser]

    def list(self,request):
        if request.user.is_superuser:
            serializer=DepartmentListSerializer(self.queryset,many=True)
            return Response({"Success":serializer.data})
        else:
            return Response({"Error":"Only Admin Can Access"}) 
    def retrieve(self, request, *args,pk):
        if request.user.is_superuser:
            department=Department.objects.filter(id=pk)
            if department:
                serializer=DepartmentListSerializer(department,many=True)
                return Response({"Success":serializer.data})
            else:
                return Response({"Error-Status":status.HTTP_404_NOT_FOUND})
        else:
            return Response({"Error":"Only Admin Can Access"})    
# ------------------------------------------------------------------------------------------------------   

          
# ------------------------------------------------------------------------------------------------------ 
#This Viewset use full to login the user and user can get tokens acccess and refresh
class LoginView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
# ------------------------------------------------------------------------------------------------------ 

# ------------------------------------------------------------------------------------------------------ 
# We Create employee and user both with this api view 
# The List Method is override beacuse the user can read the foreign key data
class RegisterAndEmployee(ViewSet):
    permission_classes=[AllowAny]
    def create(self,request):
        if User.objects.filter(username=request.data["username"]).exists():
            return Response({"username-error":"user name already exists"})
        elif User.objects.filter(email=request.data["email"]).exists():
            return Response({"Email-error":"Email already exists"})
        else:
            
            user_data={
                "first_name":request.data["first_name"],
                "last_name":request.data["last_name"],
                "email":request.data['email'],
                "username":request.data['username'],
                "password":request.data['password']
            }
            serializer=UserSerializer(data=user_data)
            if serializer.is_valid():
                user=serializer.save()
                candidate_data={
                    "user":user.id,
                    "name":request.data["first_name"] +" "+ request.data['last_name'],
                    "phone":request.data["phone"],
                    "is_manager":False,
                    "department":request.data["department"], 
                    "projects":request.data["projects"]   
                }
                serializer=EmployeeSerializer(data=candidate_data)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    return Response({"Success":serializer.data})
                else:
                    return Response({"Candidate-Create-Error":serializer.errors})
            else:
                return Response({"user-Create-Error":serializer.errors})
            
    def list(self,request):
            queryset=Employee.objects.all()
            serializer=EmployeeListSerializer(queryset,many=True)
            return Response(serializer.data)
# ------------------------------------------------------------------------------------------------------  


# ------------------------------------------------------------------------------------------------------     
# Employee login and get token and this token use full to view the perticular employee data and update its data 
class ViewPerticularEmployeeData(ModelViewSet):

    
    def list(self,request):
        employee_queryset=Employee.objects.filter(user__id=request.user.id)
        serializer=EmployeeListSerializer(employee_queryset,many=True)
        return Response(serializer.data)
    
    def update(self,request,pk, format=None):
            instance = Employee.objects.get(id=pk)
            if instance:
                if instance.user.id == request.user.id:
                    serializer=EmployeeSerializer(instance=instance,data=request.data, partial=True)
                    if serializer.is_valid(raise_exception=True):
                            serializer.save()
                            return Response({"Success":serializer.data})
                    else:
                        return Response({"Error":serializer.errors})
                else:
                    return Response({"Error":"Not Update Any Other Employee Detail"})
            else:
                return Response({"Error-Status":status.HTTP_404_NOT_FOUND})
            
    def partial_update(self, request, pk):
            instance=Employee.objects.get(id=pk)
            if instance:
                if instance.user.id == request.user.id:
                    serializer=EmployeeSerializer(instance=instance,data=request.data,partial=True)
                    if serializer.is_valid(raise_exception=True):
                        serializer.save()
                        return Response({"Success":serializer.data})
                    else:
                        return Response({"Error":serializer.errors})
                else:
                    return Response({"Error":"Not Update Any Other Employee Detail"})
            else:
                return Response({"Error-Status":status.HTTP_404_NOT_FOUND})
# ------------------------------------------------------------------------------------------------------  
            
# ------------------------------------------------------------------------------------------------------
# In this view all employee are register and register employee show list to admin 
# and admin can decided which employee to make manager      
class ActiveManagerByAdminViewSet(ModelViewSet):
    queryset=Employee.objects.filter(is_manager=False)
    serializer_class=EmployeeListSerializer  
    permission_classes=[IsAdminUser]

            
    def update(self,request,pk, format=None):
            if request.user.is_superuser:
                instance = Employee.objects.get(id=pk)
                serializer=EmployeeSerializer(instance=instance,data=request.data, partial=True)
                if serializer.is_valid(raise_exception=True):
                        serializer.save()
                        return Response({"Success":serializer.data})
                else:
                    return Response({"Error":serializer.errors})
            else:
                return Response({"Error":"Only Admin Can Access"})
    def partial_update(self, request, pk):
            if pk :
                if request.user.is_superuser:
                    instance=Employee.objects.get(id=pk)
                    serializer=EmployeeSerializer(instance=instance,data=request.data,partial=True)
                    if serializer.is_valid(raise_exception=True):
                        serializer.save()
                        return Response({"Success":serializer.data})
                    else:
                        return Response({"Error":serializer.errors})
                else:
                    return Response({"Error":"Only Admin can Update"})
            else:
                return Response({"Error-Status":status.HTTP_404_NOT_FOUND})
# ------------------------------------------------------------------------------------------------------              

# ------------------------------------------------------------------------------------------------------ 
# This View is usefull to manager can view his department employee data and only manager can              
class TeamView(ViewSet):
    
    def list(self,request):
        manager=Employee.objects.get(user__id=request.user.id)
        if manager.is_manager:
            queryset=Employee.objects.filter(department__id=manager.department.id,is_manager=False)
            serializer=EmployeeListSerializer(queryset,many=True)
            return Response({f"{manager.department.name}-Department-List":serializer.data})
        else:
            return Response({"Error":"You are not manager"})
        
    def destroy(self, request, *args, pk):
        manager=Employee.objects.get(user__id=request.user.id)
        if manager.is_manager:
                employee = Employee.objects.get(id=pk)
                if employee.department.id == manager.department.id:
                    instance = User.objects.get(id=employee.user.id)
                    self.perform_destroy(instance)
                    return Response({"Success":"Deleted SuccessFully"})
                else:
                    return Response({"Error":"Deleted Only Your Department Employee Data"})
        else:
            return Response({"Error":"You are not manager"})

    def perform_destroy(self, instance):
        instance.delete()
# ------------------------------------------------------------------------------------------------------ 

# ------------------------------------------------------------------------------------------------------ 
# In this view the admin can show update and delete the perticular department only manager data               
class TeamManagerView(ViewSet):
    permission_classes=[IsAdminUser] 
    def retrieve(self, request, *args,pk):
        employee=Employee.objects.filter(department__id=pk,is_manager=True)
        if employee:
            serializer=EmployeeListSerializer(employee,many=True)
            return Response({"Success":serializer.data})
        else:
            return Response({"Error-Status":status.HTTP_404_NOT_FOUND})
        
    def update(self,request,pk, format=None):
                instance = Employee.objects.get(id=pk)
                if instance:
                    if instance.is_manager:
                        serializer=EmployeeSerializer(instance=instance,data=request.data, partial=True)
                        if serializer.is_valid(raise_exception=True):
                            serializer.save()
                            return Response({"Success":serializer.data})
                        else:
                            return Response({"Error":serializer.errors})
                    else:
                        return Response({"Error":"Change Only Manager Detail"})
                else:
                     return Response({"Error-Status":status.HTTP_404_NOT_FOUND})
    def partial_update(self, request, pk):
                instance=Employee.objects.get(id=pk)
                if instance:
                    if instance.is_manager:
                        serializer=EmployeeSerializer(instance=instance,data=request.data,partial=True)
                        if serializer.is_valid(raise_exception=True):
                            serializer.save()
                            return Response({"Success":serializer.data})
                        else:
                            return Response({"Error":serializer.errors})
                    else:
                        return Response({"Error":"Change Only Manager Detail"})
                else:
                        return Response({"Error":status.HTTP_404_NOT_FOUND})
        
    def destroy(self, request, *args, pk):
        manager=Employee.objects.get(id=pk)
        if manager:
            if manager.is_manager:
                    instance = User.objects.get(id=manager.user.id)
                    self.perform_destroy(instance)
                    return Response({"Success":"Deleted SuccessFully"})
            else:
                return Response({"Error-Status":"Delete Only Manager Detail"})
        else:
             return Response({"Error":status.HTTP_404_NOT_FOUND})

    def perform_destroy(self, instance):
        instance.delete()
# ------------------------------------------------------------------------------------------------------              

# ------------------------------------------------------------------------------------------------------
# In this view the admin can show update and delete the perticular department employee and all department 
# employee  data   
class TeamEmployeeDataView(ViewSet):

    permission_classes=[IsAdminUser]

    def list(self,request):
        employee=Employee.objects.all()
        serializer=EmployeeListSerializer(employee,many=True)
        return Response({"Success":serializer.data})
    
    def retrieve(self, request, *args,pk):
        employee=Employee.objects.filter(department__id=pk)
        if employee:
            serializer=EmployeeListSerializer(employee,many=True)
            return Response({"Success":serializer.data})
        else:
             return Response({"Error":status.HTTP_404_NOT_FOUND})

    def update(self,request,pk, format=None):
                instance = Employee.objects.filter(id=pk)
                if instance:
                        serializer=EmployeeSerializer(instance=instance,data=request.data, partial=True)
                        if serializer.is_valid(raise_exception=True):
                                serializer.save()
                                return Response({"Success":serializer.data})
                        else:
                            return Response({"Error":serializer.errors})
                else:
                     return Response({"Error-Status":status.HTTP_404_NOT_FOUND})
    def partial_update(self, request, pk):
                instance=Employee.objects.filter(id=pk)
                if instance:
                        serializer=EmployeeSerializer(instance=instance,data=request.data,partial=True)
                        if serializer.is_valid(raise_exception=True):
                            serializer.save()
                            return Response({"Success":serializer.data})
                        else:
                            return Response({"Error":serializer.errors})
                else:
                        return Response({"Error":status.HTTP_404_NOT_FOUND})
        
    def destroy(self, request, *args, pk):
        manager=Employee.objects.get(id=pk)
        if manager:
                    instance = User.objects.get(id=manager.user.id)
                    self.perform_destroy(instance)
                    return Response({"Success":"Deleted SuccessFully"})
        else:
             return Response({"Error":status.HTTP_404_NOT_FOUND})

    def perform_destroy(self, instance):
        instance.delete()    
         
# ------------------------------------------------------------------------------------------------------     
    
    
     

           
