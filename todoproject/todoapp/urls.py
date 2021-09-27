from django.contrib import admin
from django.urls import path, re_path, include
from rest_framework.routers import DefaultRouter
from . import views

router =  DefaultRouter()
router.register('accounts', views.UserViewSet, 'users')
router.register('tasks', views.TaskViewSet, 'tasks')

urlpatterns = [
    path('', include(router.urls)),

]