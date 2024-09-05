from django.http import HttpResponse
import psycopg2
from django.db import connection
from uuid import UUID

def token_generation_reset_customer_password(email, token_duration):
    with connection.cursor() as cursor:
        cursor.callproc('udf_reset_customer_password', (email, token_duration))
        token = cursor.fetchone()[0]
    return token


def reset_customer_password(p_token, p_new_password):
    try:
        p_token = UUID(p_token)
    except ValueError:
        # Handle the case where p_token is not a valid UUID
        return HttpResponse('Invalid token')

    with connection.cursor() as cursor:
        cursor.callproc('udf_customer_update_password', (str(p_token), p_new_password))  





def customer_login(email, password):
    with connection.cursor() as cursor:
        cursor.callproc('public.udf_customer_login', [email, password])
        result = cursor.fetchone()
        return result[0] if result else None

# def CustomerLogin(p_email,p_password):
#     try:
#         connection=psycopg2.connect(
#             dbname="postgres6",
#             user="postgres",
#             password="postgres",
#             host="localhost",
#             port="5432"
#         )
#         cursor=connection.cursor()
#         cursor.callproc("udf_customer_login",(p_email,p_password))
#         result=cursor.fetchone()[0]
#         connection.commit()
#         return result
#     except psycopg2.Error as e:
#         print("Error:",e)

#     finally:
#         if connection:
#             connection.close()
    
    
