from django.db import models
from django.contrib.auth.models import User
# Create your models here.

#In this db  admin created company 
class Company(models.Model):
    name=models.CharField(max_length=100,null=True,blank=True)
    
    def __str__(self) :
        return self.name
    
#In this db  admin created department to company
    
class Department(models.Model):
    name=models.CharField(max_length=100,null=True,blank=True)
    company=models.ForeignKey(Company,on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self) :
        return self.name
    
#In this db admin create projects to assign the candidate  
class Project(models.Model):
    name=models.CharField(max_length=100,null=True,blank=True)

    def __str__(self) :
        return self.name
# In this db Employee are register with its user object this user object are relation with perticular employee    
class Employee(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    name=models.CharField(max_length=100,null=True,blank=True)
    phone=models.CharField(max_length=10,null=True,blank=True)
    is_manager=models.BooleanField(default=False)
    department=models.ForeignKey(Department,on_delete=models.CASCADE,null=True,blank=True)
    projects=models.ManyToManyField(Project)

    def project(self):
        return ",".join([str(b) for b in self.projects.all() ])
    


