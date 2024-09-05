from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render,HttpResponse,redirect
from django.urls import reverse
from .dboperations import  addCustomer, audit_trail, change_password_by_ID, get_user_id_by_username, insert_cust_password, insert_user, update_customer, user_login
from django.contrib.auth import logout
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .dboperations import change_password
from .dboperations import soft_delete_customer


@api_view(['GET'])
def display_audit_trail(request):
    audit_tail_data = audit_trail()
    return JsonResponse({'audit_tail':audit_tail_data})


@api_view(['POST'])
def update_customer_api(request):
    try:
        # Assuming you send JSON data in the request body
        data = request.data

        # Extract customer data from the JSON data
        customer_firstname = data.get("customer_firstname")
        customer_lastname = data.get("customer_lastname")
        phone = data.get("phone")
        address = data.get("address")
        email = data.get("email")
        modified_by = request.session.get("user_id")  # Use the user_id from the session

        # Call the update_customer function to update the customer
        result = update_customer(customer_firstname, customer_lastname, phone, address, email, modified_by)

        if result is not None:
            return Response({"message": result})
        else:
            return Response({"error": "Error updating customer"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    except Exception as e:
        error_message = str(e)
        return Response({"error": error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# @api_view(['POST'])
# def UpdateCustomerView(request):
#     if request.method == 'POST':
#         p_customer_firstname=request.POST.get('Customer_firstname')
#         p_customer_lastname=request.POST.get('Customer_lastname')
#         p_phone=request.POST.get('Phone_no')
#         p_address=request.POST.get('Address')
#         p_email=request.POST.get('Email_id')
#         p_modified_by=request.session.get('user_id')
#         try:
#             result_text=UpdateCustomer(p_customer_firstname,p_customer_lastname,p_phone,p_address,p_email,p_modified_by)
#             if result_text =='Customer updated successfully.':
#                 return JsonResponse({'message': result_text},status=200)
#             else:
#                 return JsonResponse({'message': result_text},status=400)
#         except Exception as e:
#             return JsonResponse({'message': f'Error updating customer: {e}'}, status=400)
#     return JsonResponse({'message': 'Invalid request'}, status=400)








def soft_delete_customer_view(request):
    if request.method == 'POST':
        p_customer_id = request.POST.get('customer_id')
        p_deleted_by = request.session.get('user_id')
        try:
            result_text = soft_delete_customer(p_customer_id, p_deleted_by)
            if result_text == 'Customer deleted successfully':
                return JsonResponse({'message': result_text}, status=200)
            else:
                return JsonResponse({'message': result_text}, status=400)
        except Exception as e:
            return JsonResponse({'message': f'Error deleting customer: {e}'}, status=400)
    return JsonResponse({'message': 'Invalid request'}, status=400)





            
def add_customer(request):
    if request.method == 'POST':
        customer_firstname = request.POST.get('customer_firstname')
        customer_lastname = request.POST.get('customer_lastname')        
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        email = request.POST.get('email')
        added_by = request.session.get('user_id')
        try:
            customer_id = addCustomer(customer_firstname, customer_lastname, phone, address, email, added_by)
            
            # Store the customer_id in the session for later use
            request.session['newly_added_customer_id'] = customer_id
            
            # Set a flag in the session to indicate successful customer addition
            request.session['customer_added'] = True
            
            return JsonResponse({'message': 'Customer added successfully.', 'customer_id': customer_id}, status=200)
        except Exception as e:
            return JsonResponse({'message': f'Error adding customer: {e}'}, status=400)
    return JsonResponse({'message':'Invalid request'}, status=400)




def insert_password(request):
    customer_id= request.session.get('newly_added_customer_id')
    if customer_id is None:
        return HttpResponse('Customer ID not found in session. Please add a customer first')
    if request.method == 'POST':
        password = request.POST.get('password')        
        try:
            result_text = insert_cust_password(customer_id, password)
            # return JsonResponse({'message': result_text}, status=200)
            return HttpResponseRedirect(reverse('home'))
        except Exception as e:
            return JsonResponse({'message': f'Error inserting password: {e}'}, status=400)
    return JsonResponse({'message': 'Invalid request'}, status=400)







@api_view(['POST'])
def change_password_view(request):
    if request.method == 'POST':
        user_id_param=request.session.get('user_id')
        old_password_param=request.data.get('old_password')
        new_password_param=request.data.get('new_password')
        result=change_password_by_ID(user_id_param,old_password_param,new_password_param)
        if result== 'Password changed successfully':
            return Response({'message':result}, status=status.HTTP_200_OK)
        else:
            return Response({'message':result},status=status.HTTP_400_BAD_REQUEST)





def HomePage(request):
    if request.session.get('authenticated'):
        return render(request,'home.html')
    else:
        return redirect('login')
    





def SignupPage(request):
    if request.method == 'POST':
        uname= request.POST.get('username')
        pword= request.POST.get('password')
        confrim_password= request.POST.get('confirmpassword')
        urole= request.POST.get('role')  
        if pword == confrim_password:
            insert_user(uname,pword,urole)
            return redirect('login')
        else:
            error_message="Password do not match. Please try again!"  
            return HttpResponse(error_message)


            
    return render(request,'signup.html')


def set_authenticated_false(request):
    request.session['authenticated'] = False

def LoginPage(request):
    if request.method == 'POST':
        username_param = request.POST.get('username')
        password_param = request.POST.get('password')
        
        login_result = user_login(username_param, password_param)
        
        if login_result == 'Login Successful !':
            request.session['authenticated'] = True
            request.session['username'] = username_param  # Store username in session
            user_id = get_user_id_by_username(username_param)
            if user_id is not None:
                request.session['user_id']=user_id

            return redirect('home')
        else:
            return HttpResponse("Username or Password is incorrect !!!")
        
    return render(request, 'login.html')



def LogoutPage(request):
    request.session.pop('authenticated',None)
    logout(request)
    return redirect('login')













































# def LoginPage(request):
#     if request.method=='POST':
#         username_param=request.POST.get('username')
#         password_param=request.POST.get('password')
#         login_result=user_login(username_param,password_param)
#         if login_result=='Login Successful !':
#             user=authenticate(request,username=username_param,password=password_param)
#             if user is not None:
#                 login(request,user)
#                 return redirect("home")
#         else:
#             error_message = login_result
#             return render(request,"login.html",{"error_message":error_message})
        
#     return render(request,"login.html")




# Create your views here.

# def add_customer(request):
#     if request.method == 'POST':
#         customer_firstname = request.POST.get('customer_firstname')
#         customer_lastname = request.POST.get('customer_lastname')        
#         phone = request.POST.get('phone')
#         address = request.POST.get('address')
#         email = request.POST.get('email')
#         added_by = request.session.get('user_id')
#         try:
#             addCustomer(customer_firstname,customer_lastname
#                         ,phone,address,email,added_by)
#             return JsonResponse({'message': 'Customer added successfully.'},status=200)
#         except Exception as e :
#             return JsonResponse({'message':f'Error adding customer: {e}'},status=400)
#     return JsonResponse({'message':'Invalid request'},status=400)