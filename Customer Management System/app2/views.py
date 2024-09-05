from django.http import HttpResponse
from django.shortcuts import redirect, render
from rest_framework.decorators import api_view
from app2.dboperations import customer_login
from rest_framework.response import Response
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render,HttpResponse,redirect
from django.urls import reverse
from rest_framework import status

# Create your views here.

from django.shortcuts import render
from django.http import HttpResponse

from app2.utils import send_password_reset_email
from .dboperations import customer_login, reset_customer_password, token_generation_reset_customer_password
from django.contrib.auth import logout




def reset_password_request_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        token_duration = '1 day'
        token=token_generation_reset_customer_password(email,token_duration)
        send_password_reset_email(email,token)

        return HttpResponse(f'Token generated: {token}')
    return render(request,'password_reset_request.html')


def reset_password_view(request,token):
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        reset_customer_password(token,new_password)
         # Implement code to update the customer's password based on the token
        # You may need to create another database function for this

        return HttpResponse('Password reset successfully')
    return render(request,'password_reset_form.html')





















def customer_login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        result = customer_login(email, password)

        if result == 'Login successful.':
            request.session['authenticated'] = True
            return redirect('customer-homepage')
        else:
            return render(request, 'customerlogin.html', {'error': result})

    return render(request, 'customerlogin.html')

def customer_logout_view(request):
    if request.session.get('authenticated'):
        request.session.pop('authenticated', None)
        logout(request)
    return redirect('customer-login')

def CustomerHomePage(request):
    if request.session.get('authenticated'):
        response = render(request, 'customerhome.html')
        # Add cache prevention headers
        response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        return response
    else:
        return HttpResponseRedirect(reverse('customer-login'))

 

    












# def customer_login_view(request):
#     if request.method == 'POST':
#         email = request.POST.get('email')
#         password = request.POST.get('password')
#         result = customer_login(email, password)

#         if result == 'Login successful.':
#             request.session['authenticated'] = True
#             return redirect('customer-homepage')
#         else:
#             return render(request, 'customerlogin.html', {'error': result})

#     return render(request, 'customerlogin.html')


# def CustomerHomePage(request):
#     if request.session.get('authenticate'):
#         return render(request,'customerhome.html')
#     else:
#         return redirect('customer-login')


# def customer_logout_view(request):
#     request.session.pop('authenticate',None)
#     logout(request)
#     return redirect('customer-login')