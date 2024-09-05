"""
URL configuration for cms project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from app1 import views
from app2.views import CustomerHomePage, customer_login_view,customer_logout_view, reset_password_request_view, reset_password_view



urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/',views.SignupPage,name='signup'),
    path('login/',views.LoginPage,name='login'),
    path('home/',views.HomePage,name='home'),
    path('logout/',views.LogoutPage,name='logout'),
    path('home/change-password',views.change_password_view,name='change-password'),
    path('home/add-customer',views.add_customer,name='add-customer'),
    path('insert-password/',views.insert_password,name='insert-password'),
    path('soft-delete-customer/', views.soft_delete_customer_view, name='soft-delete-customer'),
    path('update-customer/',views.update_customer_api,name='update-customer'),
    path('audit-trail/',views.display_audit_trail,name='audit-trail'),

#  below are customer login urls

    path('customer-login/',customer_login_view,name='customer-login'),
    path('customer-logout/',customer_logout_view,name='customer-logout'),
    path('customer-homepage/',CustomerHomePage,name='customer-homepage'),
    path('reset-password/',reset_password_request_view,name='reset-password'),
    path('reset-password/<str:token>/',reset_password_view,name='reset-password')

    

]
