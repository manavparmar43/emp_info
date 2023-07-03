from django.contrib import admin

# Register your models here.
from .models import *

@admin.register(Company)
class Companys(admin.ModelAdmin):
        list_display=['id',"name"]
    
@admin.register(Department)
class Departments(admin.ModelAdmin):
        list_display=['id',"name","company"]

@admin.register(Project)
class Projects(admin.ModelAdmin):
        list_display=['id',"name"]

@admin.register(Employee)
class Employees(admin.ModelAdmin):
        list_display=['id','user',"name","phone","is_manager","department","project"]