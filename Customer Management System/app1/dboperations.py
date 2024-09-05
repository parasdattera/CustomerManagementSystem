import psycopg2
from django.db import connection

def audit_trail():
    try:
        with connection.cursor() as cursor:
            cursor.callproc('public.udf_display_audit_trail')
            results = cursor.fetchall()
    finally:
        cursor.close()
        connection.close()
    
    return results




def update_customer(p_customer_firstname, p_customer_lastname, p_phone, p_address, p_email, p_modified_by):
    try:
        # Establish a database connection
        conn = psycopg2.connect(dbname="postgres6",
            user="postgres",
            password="postgres",
            host="localhost",
            port="5432")
        
        # Create a cursor object
        cursor = conn.cursor()
        
        # Call the PostgreSQL function
        cursor.callproc("public.udf_update_customer", [
            p_customer_firstname, p_customer_lastname, p_phone, p_address, p_email, p_modified_by
        ])
        
        # Fetch the result returned by the PostgreSQL function
        result = cursor.fetchone()
        
        # Commit the transaction
        conn.commit()
        
        # Close the cursor and connection
        cursor.close()
        conn.close()
        
        return result  # Return the result from the PostgreSQL function
    
    except Exception as e:
        return str(e)



# def UpdateCustomer(p_customer_firstname,p_customer_lastname,p_phone,p_address,p_email,p_modified_by):
#     try:
#         with connection.cursor() as cursor:
#             cursor.callproc('udf_update_customer',[p_customer_firstname,p_customer_lastname,p_phone,p_address,p_email,p_modified_by])
#             result_text=cursor.fetchone()[0]
#             return result_text
#     except psycopg2.DatabaseError as e:
#         error_message=f"Database error: {e}"
#         print(error_message)
#         raise
#     except Exception as e:
#         error_message = f"An error occurred: {e}"
#         print(error_message)
#         raise        
    



def soft_delete_customer(p_customer_id,p_deleted_by):
    try:
        with connection.cursor() as cursor:
            cursor.callproc('udf_soft_delete_customer',[p_customer_id,p_deleted_by])
            result_text=cursor.fetchone()[0]
            return result_text
    except psycopg2.DatabaseError as e:
        error_message=f"Database error: {e}"
        print(error_message)
        raise
    except Exception as e:
        error_message = f"An error occurred: {e}"
        print(error_message)
        raise










def insert_cust_password(customer_id,password):
    try:
        with connection.cursor() as cursor:
            cursor.callproc('udf_insert_cust_password',[customer_id,password])
            result_text = cursor.fetchone()[0]
            return result_text
    except psycopg2.DatabaseError as e:
        error_message = f"Database error: {e}"
        print(error_message)
        raise
    except Exception as e:
        error_message = f"An error occurred: {e}"
        print(error_message)
        raise









def addCustomer(p_customer_firstname,
                p_customer_lastname,
                p_phone,
                p_address,
                p_email,
                p_added_by):
    try:
        with connection.cursor() as cursor:
            cursor.callproc('udf_insert_customer', [p_customer_firstname, p_customer_lastname, p_phone, p_address, p_email, p_added_by])
            # Fetch the inserted customer's ID
            cursor.execute("SELECT currval('customer_id_seq')")
            customer_id = cursor.fetchone()[0]
            return customer_id
    except psycopg2.DatabaseError as e:
        error_message = f"Database error: {e}"
        print(error_message)
        raise
    except Exception as e:
        error_message = f"An error occurred: {e}"
        print(error_message)
        raise








def change_password_by_ID(user_id_param,old_password_param,new_password_param):
    with connection.cursor() as cursor:
        cursor.callproc('udf_change_password_by_id',[user_id_param,old_password_param,new_password_param])
        result=cursor.fetchone()
        return result[0]



def change_password(username_param,old_password_param,new_password_param):
    with connection.cursor() as cursor:
        cursor.callproc('udf_change_password',[username_param,old_password_param,new_password_param])
        result=cursor.fetchone()
        return result[0]


def insert_user(username,password,role):
    try:
        connection = psycopg2.connect(
            dbname="postgres6",
            user="postgres",
            password="postgres",
            host="localhost",
            port="5432"

        )
        cursor= connection.cursor()

        cursor.callproc("udf_insert_user",(username,password,role))
        connection.commit()
    except psycopg2.Error as e:
        print("Error:",e)

    finally:
        if connection:
            connection.close()



def user_login(username_param,password_param):
    try:
        connection=psycopg2.connect(
            dbname="postgres6",
            user="postgres",
            password="postgres",
            host="localhost",
            port="5432"
        )
        cursor=connection.cursor()
        cursor.callproc("udf_user_login",(username_param,password_param))
        result=cursor.fetchone()[0]
        connection.commit()
        return result
    except psycopg2.Error as e:
        print("Error:",e)

    finally:
        if connection:
            connection.close()





def get_user_id_by_username(username):
    connection=psycopg2.connect(
            dbname="postgres6",
            user="postgres",
            password="postgres",
            host="localhost",
            port="5432"
    )
    cursor = connection.cursor()
    query = "SELECT user_id FROM public.users WHERE username = %s"
    cursor.execute(query,(username,))
    user_id = None
    result = cursor.fetchone()
    if result:
        user_id = result[0]
    cursor.close()
    connection.close()
    return user_id

































































# def addCustomer(p_customer_firstname,
#                 p_customer_lastname,
#                 p_phone,
#                 p_address,
#                 p_email,
#                 p_added_by):
#     try:
#         with connection.cursor() as cursor:
#             cursor.callproc('udf_insert_customer',[p_customer_firstname,p_customer_lastname,p_phone,p_address,p_email,p_added_by])
#     except psycopg2.DatabaseError as e:
#         error_message = f"Database error: {e}"
#         print(error_message)
#         raise
#     except Exception as e:
#         error_message = f"An error occurred: {e}"
#         print(error_message)
#         raise
