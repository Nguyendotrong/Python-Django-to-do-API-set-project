from django.contrib import admin
from django.urls import path, re_path, include
from rest_framework.routers import DefaultRouter
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)

router =  DefaultRouter()
router.register('accounts', views.UserViewSet, 'users')
router.register('tasks', views.TaskViewSet, 'tasks')

urlpatterns = [
    path('', include(router.urls)),
    path('accounts/sign-in/', TokenObtainPairView.as_view(),
            name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(),
            name='token_refresh'),

]