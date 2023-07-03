from rest_framework.routers import DefaultRouter
from .views import *
from django.urls import path,include
router=DefaultRouter()

router.register("company",CompanyViewSet,basename="company"),
router.register("department",DepartmentViewSet,basename="department"),
router.register("register-employee",RegisterAndEmployee,basename="register-employee"),
router.register("view-update-delete-data",ViewPerticularEmployeeData,basename="view-update-delete-data"),
router.register("team-view",TeamView,basename="team-view"),
router.register("team-manager-view",TeamManagerView,basename="team-manager-view"),
router.register("team-employee-view",TeamEmployeeDataView,basename="team-employee-view"),