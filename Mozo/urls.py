"""Mozo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from rest_framework import routers

from mozorest.views import ExpenseViewSet, AccountViewSet, UserViewSet, UserDetailViewSet, TransactionViewSet, TokenViewSet
from rest_framework.authtoken import views


router = routers.DefaultRouter()
router.register(r'User', UserViewSet)
router.register(r'UserDetail', UserDetailViewSet)
router.register(r'account', AccountViewSet)
router.register(r'expense', ExpenseViewSet)
router.register(r'transactions', TransactionViewSet)


urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^auth-social/', TokenViewSet.as_view())
]


urlpatterns += [
    url(r'^auth-user-token/', views.obtain_auth_token)
]