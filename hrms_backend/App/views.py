from django.shortcuts import render, redirect,get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import stripe
from django.conf import settings  
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login, logout
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from rest_framework.parsers import MultiPartParser, FormParser
# Create your views here.
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.db.models import F,Q, ExpressionWrapper
# Create your views here.
from decimal import Decimal,ROUND_HALF_UP
from django.utils import timezone
from datetime import datetime






class EmployerSignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = MyUserSerializer(data=request.data)
        print(request.data)
        if serializer.is_valid():
            
            user = serializer.save()
            user.set_password(request.data.get('password'))
            user.is_employer = True
            user.save()
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            user_data = {
                'id': user.id,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'isLoggedIn':'true',
                'auth_token': token.key, 
                'isEmployer': user.is_employer,
            }
            return Response({'success': True, 'message': 'Signup successful', 'user': user_data}, status=status.HTTP_201_CREATED)
        return Response({'success': False, 'message': 'Signup failed', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)





class GeneralLoginView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = [TokenAuthentication]

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        print('request.data:',request.data)
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, email=email, password=password)

        if user.is_employer:
            print(request.data)
            login(request, user)
            serializer = MyUserSerializer(user)

            #return Response(serializer.data)
            token, created = Token.objects.get_or_create(user=user)
            
            user_data = {
                'id': user.id,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name, 
                'isLoggedIn':'true',
                'auth_token': token.key, 
                'isEmployer': True,
                'isInstructor': False,
                'isClient': False,
                'isEmployee': False,
            }
            print(user_data)
            return Response({'success': True, 'message': 'Login successful', 'user': user_data},status=status.HTTP_201_CREATED)
        elif user.is_employee:
            print(request.data)
            login(request, user)
            serializer = MyUserSerializer(user)

            #return Response(serializer.data)
            token, created = Token.objects.get_or_create(user=user)
            
            user_data = {
                'id': user.id,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name, 
                'isLoggedIn':'true',
                'auth_token': token.key, 
                'isEmployer': False,
                'isInstructor': False,
                'isClient': False,
                'isEmployee': True,
            }
            print(user_data)
            return Response({'success': True, 'message': 'Login successful', 'user': user_data},status=status.HTTP_201_CREATED)

        elif user.is_instructor:
            print(request.data)
            login(request, user)
            serializer = MyUserSerializer(user)

            #return Response(serializer.data)
            token, created = Token.objects.get_or_create(user=user)
            
            user_data = {
                'id': user.id,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name, 
                'isLoggedIn':'true',
                'auth_token': token.key, 
                'isEmployer': False,
                'isInstructor': True,
                'isClient': False,
                'isEmployee': False,
            }
            print(user_data)
          
            return Response({'success': True, 'message': 'Login successful', 'user': user_data},status=status.HTTP_201_CREATED)

        elif user.is_client:
            print(request.data)
            login(request, user)
            serializer = MyUserSerializer(user)

            #return Response(serializer.data)
            token, created = Token.objects.get_or_create(user=user)
            
            user_data = {
                'id': user.id,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name, 
                'isLoggedIn':'true',
                'auth_token': token.key, 
                'isEmployer': False,
                'isInstructor': True,
                'isClient': True,
                'isEmployee': False,
            }
            print(user_data)
          
            return Response({'success': True, 'message': 'Login successful', 'user': user_data},status=status.HTTP_201_CREATED)
        else:
            return Response({'success': False, 'error': 'Invalid credentials'}, status=401)




class EmployerLoginView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = [TokenAuthentication]

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        print('request.data:',request.data)
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, email=email, password=password)

        if user.is_employer:
            print(request.data)
            login(request, user)
            serializer = MyUserSerializer(user)

            #return Response(serializer.data)
            token, created = Token.objects.get_or_create(user=user)
            
            user_data = {
                'id': user.id,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name, 
                'isLoggedIn':'true',
                'auth_token': token.key, 
                'isEmployer': user.is_employer,
            }
            print(user_data)
          
            return Response({'success': True, 'message': 'Login successful', 'user': user_data},status=status.HTTP_201_CREATED)
        else:
            return Response({'success': False, 'error': 'Invalid credentials'}, status=401)




class OrganizationCreateView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    
    def post(self, request, *args, **kwargs):
        auth_header = request.headers.get('Authorization', '')
        _, token = auth_header.split()
        # Check if the token is valid
        token_obj = Token.objects.get(key=token)
        user = token_obj.user
        print('request.data:',request.data)
       
    
        serializer = OrganizationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(employer=user)  # Set the instructor to the current user
            return Response({'success': True, },status=status.HTTP_201_CREATED)
       
        return Response({'success': False,'message':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class EmployerOrganizationsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        auth_header = request.headers.get('Authorization', '')
        _, token = auth_header.split()
        # Check if the token is valid
        token_obj = Token.objects.get(key=token)
        user = token_obj.user
        organizations = Organization.objects.filter(employer = user)
        
        all_organizations = []
        for data in organizations:
          
            org_data = {
                'id': data.id,
                'employer': f"{data.employer.first_name} {data.employer.last_name}",
                'name': data.name,
                'overview': data.overview,
                'logo': data.logo.url if data.logo else '',
                'employee_count': data.employees.count(),
                'organization_type': data.organization_type,
                
    
            }
            all_organizations.append(org_data)#
     
        print('all_organizations:',all_organizations)
        return Response({'all_organizations':all_organizations}, status=status.HTTP_200_OK)



class OrganizationEditView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request,pk, *args, **kwargs):
        auth_header = request.headers.get('Authorization', '')
        _, token = auth_header.split()
        # Check if the token is valid
        token_obj = Token.objects.get(key=token)
        user = token_obj.user
        organization = Organization.objects.get(id = pk,employer = user)
        
        org_data = {
            'id': organization.id,
            'employer': f"{organization.employer.first_name} {organization.employer.last_name}",
            'name': organization.name,
            'overview': organization.overview,
            'logo': organization.logo.name,
            'employee_count': organization.employees.count(),    
    
        }
     
       
        return Response(org_data, status=status.HTTP_200_OK)

    def put(self, request,pk,*args, **kwargs):
        auth_header = request.headers.get('Authorization', '')
        _, token = auth_header.split()
        # Check if the token is valid
        token_obj = Token.objects.get(key=token)
        user = token_obj.user
        # Retrieve the organization based on the user making the request
        mutable_data = request.data.copy()
        logo = request.data['logo']
        organization_type = request.data['organization_type']
        print(' mutable_data:', mutable_data)
        if logo == '':
            # If not present, remove the field from serializer's excluded fields
            mutable_data.pop('logo', None)
       
        if organization_type == '':
            # If not present, remove the field from serializer's excluded fields
            mutable_data.pop('organization_type', None)
       
        organization = Organization.objects.get(id = pk,employer = user)
        serializer = OrganizationSerializer(organization, data=mutable_data,partial = True)
        if serializer.is_valid():
            serializer.save()
            #return Response(serializer.data)
            return Response({'success': True, },status=status.HTTP_201_CREATED)
       
        return Response({'success': False,'message':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class OrganizationDeleteView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request, pk, *args, **kwargs):
        auth_header = request.headers.get('Authorization', '')
        _, token = auth_header.split()
        # Check if the token is valid
        token_obj = Token.objects.get(key=token)
        user = token_obj.user
        try:
            # Retrieve the organization based on the user making the request
            organization = Organization.objects.get(id=pk, employer=user)
        except Organization.DoesNotExist:
            return Response({"message": "Organization not found."}, status=status.HTTP_404_NOT_FOUND)

        organization.delete()
        return Response({'success': True, "detail": "Organization deleted successfully."},status=status.HTTP_201_CREATED)
     

    

class DepartmentListView(APIView):
    def get(self, request, *args, **kwargs):
        departments = Department.objects.all()
        serializer = DepartmentSerializer(departments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


"""class InvitationCreateView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        print(data)
        auth_header = request.headers.get('Authorization', '')
        _, token = auth_header.split()
        # Check if the token is valid
        token_obj = Token.objects.get(key=token)
        user = token_obj.user
        #organization = Organization.objects.get(id = data.organizationId)
        #print(organization)
        serializer = InvitationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(invited_by = user)
            # Perform any additional actions (e.g., sending an email with the invitation code)
            return Response({'success': True}, status=status.HTTP_201_CREATED)

        return Response({'success': False,'message':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
"""
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
class InvitationCreateView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
       
        auth_header = request.headers.get('Authorization', '')
        _, token = auth_header.split()
        # Check if the token is valid
        token_obj = Token.objects.get(key=token)
        user = token_obj.user
        print('data:',request.data)
        email = request.data['invited_user']

        serializer = InvitationSerializer(data=request.data)
        print('serializer:',serializer.is_valid())
        if serializer.is_valid():
            invitation = serializer.save(invited_by=user)
            if myuser.objects.filter(email = email).exists():
                registration_link = f'https://mango-field-0800b630f.4.azurestaticapps.net/employee-invite/{invitation.invitation_code}/'
            else:   
                registration_link = f'https://mango-field-0800b630f.4.azurestaticapps.net/employee-signup/{invitation.invitation_code}/'
            # Send email with the invitation code
            subject = 'Invitation to join our organization'
            body = f'You are invited to join our organization. Click the link below to register:\n\n{registration_link}'
            from_email = 'hmrs@nobtec.co.uk'  # Replace with your email
            recipient_list = [invitation.invited_user]
            password = "URc9JUctpRXF"

            #send_mail(subject, message, from_email, recipient_list, fail_silently=False)
            #email = EmailMessage(subject, message, from_email, recipient_list,)
            #email.send()
            message = MIMEMultipart()
            message['From'] = from_email
            message['To'] = ', '.join(recipient_list)
            message['Subject'] = subject

            # Attach the body to the message
            message.attach(MIMEText(body, 'plain'))

            # Connect to the SMTP server
            with smtplib.SMTP_SSL("smtp.zoho.eu", port=465) as connection:
                # Login to the server
                connection.login(user=from_email, password=password)
                
                # Send the email
                connection.sendmail(from_addr=from_email, to_addrs=recipient_list, msg=message.as_string())
                connection.quit()

            return Response({'success': True}, status=status.HTTP_201_CREATED)

        return Response({'success': False, 'message': 'An error occurred'}, status=status.HTTP_201_CREATED)



class ClientInvitationCreateView(APIView):
    #http://localhost:3000/client/FxAx5HbgmUXa/
    def post(self, request, *args, **kwargs):
        data = request.data
       
        auth_header = request.headers.get('Authorization', '')
        _, token = auth_header.split()
        # Check if the token is valid
        token_obj = Token.objects.get(key=token)
        user = token_obj.user

        serializer = ClientInvitationSerializer(data=request.data)
        if serializer.is_valid():
            invitation = serializer.save(invited_by=user)
           
            registration_link = f'https://mango-field-0800b630f.4.azurestaticapps.net/client/{invitation.invitation_code}/'
            # Send email with the invitation code
            subject = "You've received an invitation to join a partnership"
            body = f'You are invited to partner with our organization,{invitation.organization}. Click the link below to register:\n\n{registration_link}'
            from_email = 'hmrs@nobtec.co.uk'  # Replace with your email
            recipient_list = [invitation.invited_user]

            password = "URc9JUctpRXF"

            #send_mail(subject, message, from_email, recipient_list, fail_silently=False)
            #email = EmailMessage(subject, message, from_email, recipient_list,)
            #email.send()
            message = MIMEMultipart()
            message['From'] = from_email
            message['To'] = ', '.join(recipient_list)
            message['Subject'] = subject

            # Attach the body to the message
            message.attach(MIMEText(body, 'plain'))

            # Connect to the SMTP server
            with smtplib.SMTP_SSL("smtp.zoho.eu", port=465) as connection:
                # Login to the server
                connection.login(user=from_email, password=password)
                
                # Send the email
                connection.sendmail(from_addr=from_email, to_addrs=recipient_list, msg=message.as_string())
                connection.quit()

            return Response({'success': True}, status=status.HTTP_201_CREATED)

        return Response({'success': False, 'message': 'An error occurred'}, status=status.HTTP_201_CREATED)



    
class RegisterViaLinkView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, invitation_code, format=None):
        if Invitation.objects.filter(invitation_code=invitation_code, is_accepted=True).exists():
            return Response({'success':False,'message':'Expired or invalid invitation link.'}, status=status.HTTP_201_CREATED)
        else:          

            invitation = get_object_or_404(Invitation, invitation_code=invitation_code, is_accepted=False)

            serializer = MyUserSerializer(data=request.data)
            if serializer.is_valid():
             
                user = serializer.save()
                user.set_password(request.data.get('password'))
                user.is_employee = True
                #user.department = invitation.invited_by.department
                user.save()
                organization = Organization.objects.get(id = invitation.organization.id)
                organization.employees.add(user)
                # Mark the invitation as accepted
                invitation.is_accepted = True
                invitation.save()
                Membership.objects.create(
                    user = user,
                    organization = organization,
                    department = invitation.department
                )
                if Enrollment.objects.filter(organization=organization).exists():
                    enrollment = Enrollment.objects.filter(organization=organization).first()
                    enrollment.enrolled_members.add(user)

                token, created = Token.objects.get_or_create(user=user)

                user_data = {
                    'id': user.id,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name, 
                    'isLoggedIn':True,
                    'auth_token': token.key, 
                    'isEmployer': user.is_employer,
                    'isEmployee': user.is_employee,
                    'isInstructor': user.is_instructor,
                }
                

                return Response({'data':user_data , 'message': 'Registration successful! You have joined the organization.','success':True,}, status=status.HTTP_201_CREATED)

            return Response({'message':serializer.errors,'success':False}, status=status.HTTP_400_BAD_REQUEST)




class OrganizationDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request,Id, *args, **kwargs):

        
        organization = Organization.objects.get(id = Id)
       
        org_data = {
            'id': organization .id,
            'employer': f"{organization.employer.first_name} {organization.employer.last_name}",
            'name': organization.name,
            'overview': organization.overview,
            'logo': organization.logo.url,
            'employee_count': organization.employees.count(),
            'organization_type':organization.organization_type
            

        }
       
       
        return Response(org_data, status=status.HTTP_200_OK)


class EmployeeListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request,Id, *args, **kwargs):
       
        membership = Membership.objects.filter(organization__id = Id)
        
        all_members = []
        for data in membership:
            org_data = {
                'id': data.id,
                'userId': data.user.id,
                'first_name': data.user.first_name,
                'last_name':data.user.last_name,
                'department':data.department.title, 
                'organization':data.organization.name, 
                'status':data.status, 

    
            }
            all_members.append(org_data)#
        print('all_members:',all_members)
        
       
        return Response(all_members, status=status.HTTP_200_OK)




class EmployeeDepartmentChangeView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = [TokenAuthentication]

    def put(self, request,pk,*args, **kwargs):
        auth_header = request.headers.get('Authorization', '')
        _, token = auth_header.split()
        # Check if the token is valid
        token_obj = Token.objects.get(key=token)
        user = token_obj.user
        department = Department.objects.get(id = request.data['department'])
        # Retrieve the organization based on the user making the request
        if Membership.objects.filter(id = pk).exists():
            membership = Membership.objects.get(id = pk)
            membership.department = department
            membership.save()
           
            return Response({'success': True, },status=status.HTTP_201_CREATED)
       
        return Response({'success': False,'message':'An unknown error occured'}, status=status.HTTP_400_BAD_REQUEST)



class EmployeeRemoveView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = [TokenAuthentication]

    def post(self, request,pk,*args, **kwargs):
        auth_header = request.headers.get('Authorization', '')
        _, token = auth_header.split()
        # Check if the token is valid
        token_obj = Token.objects.get(key=token)
        user = token_obj.user
        
        # Retrieve the organization based on the user making the request
        if Membership.objects.filter(id = pk).exists():
            membership = Membership.objects.get(id = pk)
            membership.status = request.data['status']
            membership.save()
            EmployeeNotification.objects.create(
                user = membership.user,
                organization = membership.organization,
                status = membership.status,
                reason = request.data['reason'],
                end_date = request.data['date'],
            )
           
            return Response({'success': True, },status=status.HTTP_201_CREATED)
       
        return Response({'success': False,'message':'An unknown error occured'}, status=status.HTTP_400_BAD_REQUEST)



class EmployeeOffboardingList(APIView):
    permission_classes = [AllowAny]

    def get(self, request,Id, *args, **kwargs):
       
        membership = Membership.objects.filter(organization__id = Id,status = 'Inactive')
        
        all_members = []
        for data in membership:
            org_data = {
                'id': data.id,
                'first_name': data.user.first_name,
                'last_name':data.user.last_name,
                'department':data.department.title, 
                'organization':data.organization.name, 
                'status':data.status, 

    
            }
            all_members.append(org_data)#
       
       
        return Response(all_members, status=status.HTTP_200_OK)


class EmployeeOnboardingList(APIView):
    permission_classes = [AllowAny]

    def get(self, request,Id, *args, **kwargs):
       
        invitation = Invitation.objects.filter(organization__id = Id)
        
        all_members = []
        for data in invitation:
            org_data = {
                'id': data.id,
                'invited_by': f"{data.invited_by.first_name} {data.invited_by.last_name}",
                'department':data.department.title, 
                'organization':data.organization.name, 
                'invited_user':data.invited_user, 
                'status':'Accepted' if data.is_accepted else 'Pending', 

    
            }
            all_members.append(org_data)#
       
       
        return Response(all_members, status=status.HTTP_200_OK)



"""class CreateTimeSheetAPIView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = [TokenAuthentication]

    def post(self, request, format=None):
        auth_header = request.headers.get('Authorization', '')
        _, token = auth_header.split()
        # Check if the token is valid
        token_obj = Token.objects.get(key=token)
        user = token_obj.user

        # Check if a timesheet already exists for the user on the specified day
        today_start = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = today_start + timezone.timedelta(days=1)
        organization =  Organization.objects.get(id = request.data.get('organization'))

        existing_timesheet = TimeSheet.objects.filter(
            organization = organization,
            user=user,
            start_date__gte=today_start,
            start_date__lt=today_end
        )

        if existing_timesheet.exists():
            print("You've already created a timesheet for today:",organization )
            return Response({'success': False, 'message': "You've already created a timesheet for today."}, status=status.HTTP_201_CREATED)

        serializer = TimeSheetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=user)  # Assuming you're associating the timesheet with the logged-in user
            return Response({'success': True, 'data': serializer.data}, status=status.HTTP_201_CREATED)

        return Response({'success': False, 'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)"""


class CreateTimeSheetAPIView(APIView):
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        auth_header = request.headers.get('Authorization', '')
        _, token = auth_header.split()
        # Check if the token is valid
        token_obj = Token.objects.get(key=token)
        user = token_obj.user
        print('request.data:',request.data)
        serializer = TimeSheetSerializer(data=request.data,partial = True)
        if serializer.is_valid():
            print('valid:')
            serializer.save(user = user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print('serializer.errors:',serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserTimeSheet(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request,Id, *args, **kwargs):
        auth_header = request.headers.get('Authorization', '')
        _, token = auth_header.split()
        # Check if the token is valid
        token_obj = Token.objects.get(key=token)
        user = token_obj.user
       
        timesheet = TimeSheet.objects.filter(organization__id = Id,user = user)
        
        all_timesheet = []
        for data in timesheet:
            print('data.user.first_name:',data.user.first_name,data.client)
            if data.client != None:
                for item in data.client.clients.all():
                    org_data = {
                        'id': data.id,
                        'user': f"{data.user.first_name} {data.user.last_name}",
                        'organization':data.organization.name, 
                        'client':f"{item.first_name} {item.last_name}", 
                        'start_date':data.formatted_start_date(), 
                        'end_date':data.formatted_end_date(), 
                        'hours_worked':data.total_hours, 
                    
                        'hours_worked':data.total_hours, 
                        'client_approved':data.client_approved, 
                        'organization_approved':data.organization_approved, 

            
                    }
                    all_timesheet.append(org_data)#
            else:
                org_data = {
                    'id': data.id,
                    'user': f"{data.user.first_name} {data.user.last_name}",
                    'organization':data.organization.name, 
                    #'client':f"{item.first_name} {item.last_name}", 
                    'start_date':data.formatted_start_date(), 
                    'end_date':data.formatted_end_date(), 
                    'hours_worked':data.total_hours, 
                
                    'hours_worked':data.total_hours, 
                    'client_approved':data.client_approved, 
                    'organization_approved':data.organization_approved, 


                }
                all_timesheet.append(org_data)#
        
        print('######:',all_timesheet)
        return Response(all_timesheet, status=status.HTTP_200_OK)


class EmployeeTimeSheetList(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request,Id,organizationId, *args, **kwargs):
        
       
        timesheet = TimeSheet.objects.filter(user__id = Id,organization__id = organizationId)
        print('organizationId:', organizationId)
        if OrganizationRate.objects.filter(organization__id = organizationId).exists():
            rate = OrganizationRate.objects.get(organization__id = organizationId)
            print('rate:',rate.hourly_rate)
            rateExist = True
        else:
            #rate = OrganizationRate.objects.filter(organization__id = Id)
            rateExist = False
        
        all_timesheet = []
        for data in timesheet:
            print('data.user.first_name:',data.user.first_name,data.client)
            if data.client != None:
                for item in data.client.clients.all():
                    org_data = {
                        'id': data.id,
                        'user': f"{data.user.first_name} {data.user.last_name}",
                        'organization':data.organization.name, 
                        'client':f"{item.first_name} {item.last_name}",
                        'clientId':data.client.id, 
                        'start_date':data.formatted_start_date(), 
                        'end_date':data.formatted_end_date(), 
                        'hours_worked':data.total_hours,
                        'bill':data.client.hourly_rate * data.total_hours,
                        'hourly_rate':data.client.hourly_rate,
                    
                        
                        'client_approved':data.client_approved, 
                        'organization_approved':data.organization_approved, 

            
                    }
                    all_timesheet.append(org_data)#
            else:
                org_data = {
                    'id': data.id,
                    'user': f"{data.user.first_name} {data.user.last_name}",
                    'organization':data.organization.name, 
                    #'client':f"{item.first_name} {item.last_name}", 
                    'rate': rate.hourly_rate*data.total_hours if rateExist else '',
                    'rateExist':rateExist,
                    'start_date':data.formatted_start_date(), 
                    'end_date':data.formatted_end_date(), 
                    'hours_worked':data.total_hours, 
                
                    'hours_worked':data.total_hours, 
                    'client_approved':data.client_approved, 
                    'organization_approved':data.organization_approved, 


                }
                all_timesheet.append(org_data)#
                    
            
            
        print('######:',all_timesheet)
        return Response(all_timesheet, status=status.HTTP_200_OK)



class EmployeesTimeSheetList(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request,Id, *args, **kwargs):
        auth_header = request.headers.get('Authorization', '')
        _, token = auth_header.split()
        # Check if the token is valid
        token_obj = Token.objects.get(key=token)
        user = token_obj.user
       
        timesheet = TimeSheet.objects.filter(organization__id = Id)
        if OrganizationRate.objects.filter(organization__id = Id).exists():
            rate = OrganizationRate.objects.get(organization__id = Id)
            rateExist = True
        else:
            #rate = OrganizationRate.objects.filter(organization__id = Id)
            rateExist = False
        
        all_timesheet = []
        for data in timesheet:
            print('data.user.first_name:',data.user.first_name,data.client)
            if data.client != None:
                for item in data.client.clients.all():
                    org_data = {
                        'id': data.id,
                        'user': f"{data.user.first_name} {data.user.last_name}",
                        'organization':data.organization.name, 
                        'client':f"{item.first_name} {item.last_name}", 
                        'clientId':data.client.id, 
                        'start_date':data.formatted_start_date(), 
                        'end_date':data.formatted_end_date(), 
                        'bill':data.client.hourly_rate * data.total_hours,
                        'hourly_rate':data.client.hourly_rate,
                    
                        'hours_worked':data.total_hours, 
                        'client_approved':data.client_approved, 
                        'organization_approved':data.organization_approved, 

            
                    }
                    all_timesheet.append(org_data)#
            else:
                org_data = {
                    'id': data.id,
                    'user': f"{data.user.first_name} {data.user.last_name}",
                    'organization':data.organization.name, 
                    'rate': rate.hourly_rate*data.total_hours if rateExist else '',
                    'rateExist':rateExist,
                    #'client':f"{item.first_name} {item.last_name}", 
                    'start_date':data.formatted_start_date(), 
                    'end_date':data.formatted_end_date(), 
                    'hours_worked':data.total_hours, 
                
                    'hours_worked':data.total_hours, 
                    'client_approved':data.client_approved, 
                    'organization_approved':data.organization_approved, 


                }
                all_timesheet.append(org_data)#
        
       
        return Response(all_timesheet, status=status.HTTP_200_OK)




class EmployeeLoginView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = [TokenAuthentication]

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, email=email, password=password)
        
       
        if user and user.is_employee:
            print(request.data)
            login(request, user)
            serializer = MyUserSerializer(user)

            #return Response(serializer.data)
            token, created = Token.objects.get_or_create(user=user)
            
            user_data = {
                'id': user.id,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name, 
                'isLoggedIn':True,
                'auth_token': token.key, 
                'isEmployer': user.is_employer,
            }
           
          
            return Response({'success': True, 'message': 'Login successful', 'user': user_data},status=status.HTTP_201_CREATED)
        else:
            return Response({'success': False, 'error': 'Invalid credentials'}, status=401)




class EmployeeOrganizationsView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = [TokenAuthentication]

    def get(self, request, *args, **kwargs):
        auth_header = request.headers.get('Authorization', '')
        print('auth_header:',auth_header)
        _, token = auth_header.split()
        # Check if the token is valid
        token_obj = Token.objects.get(key=token)
        user = token_obj.user
        organizations = Membership.objects.filter(user = user)
        
        all_organizations = []
        for data in organizations:
            org_data = {
                'id': data.organization.id,
                'user': f"{data.user.first_name} {data.user.last_name}",
                'organization': data.organization.name,
                'department': data.department.title,
                'overview': data.organization.overview,
                'logo': data.organization.logo.url,
            }
            all_organizations.append(org_data)#
       
       
        return Response({'all_organizations':all_organizations}, status=status.HTTP_200_OK)




class CreateRequestView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = [TokenAuthentication]

    def post(self, request, format=None):
        auth_header = request.headers.get('Authorization', '')
        _, token = auth_header.split()
        # Check if the token is valid
        token_obj = Token.objects.get(key=token)
        user = token_obj.user
        
        serializer = RequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=user)  # Assuming you're associating the request with the logged-in user
            return Response({'success': True, 'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'success': False, 'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)




class RequestListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        auth_header = request.headers.get('Authorization', '')
        _, token = auth_header.split()
        # Check if the token is valid
        token_obj = Token.objects.get(key=token)
        user = token_obj.user
        requests = Request.objects.filter(user = user)
        
        all_requests = []
        for data in requests:
            org_data = {
                'id': data.organization.id,
                'user': f"{data.user.first_name} {data.user.last_name}",
                'organization': data.organization.name,
                'request_type': data.request_type,
                'start_date': data.start_date,
                'end_date': data.end_date,
                'status': data.status,
            }
            all_requests.append(org_data)#
      
       
        return Response({'all_requests':all_requests}, status=status.HTTP_200_OK)



"""class OrganizationTimeSheet(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request,Id, *args, **kwargs):
        auth_header = request.headers.get('Authorization', '')
        _, token = auth_header.split()
        # Check if the token is valid
        token_obj = Token.objects.get(key=token)
        user = token_obj.user
       
        timesheet = TimeSheet.objects.filter(organization__id = Id).exclude(user = user)
        
        all_timesheet = []
        for data in timesheet:
            membership = Membership.objects.get(user = data.user)
            org_data = {
                'id': data.id,
                'user': f"{data.user.first_name} {data.user.last_name}",
                'employeeId':data.user.id,
                'task_name':data.task_name, 
                'organization':data.organization.name, 
                'date':data.formatted_end_date(), 
                'hours_worked':data.hours_worked, 
                'activity_description':data.activity_description, 
                'hours_worked':data.hours_worked, 
                'status':data.status, 
                'department':membership.department.title, 

    
            }
            all_timesheet.append(org_data)#
        print(all_timesheet)
       
        return Response(all_timesheet, status=status.HTTP_200_OK)"""



class CheckPaymentSchedule(APIView):
    permission_classes = [AllowAny]

    def get(self,request,Id,format = None):
        payment_schedule = PaymentSchedule.objects.filter(organization__id=Id).first()
        schedule = payment_schedule.payment_schedule if payment_schedule else 'Monthly'
        print('schedule:',schedule)
        return Response({'success': True, 'schedule': schedule}, status=status.HTTP_200_OK)



class SetPaymentSchedule(APIView):
    permission_classes = [AllowAny]

    def post(self,request,format = None):
        organizationId = request.data['organizationId']
        payment_schedule = PaymentSchedule.objects.filter(organization__id=organizationId)
        schedule_type = request.data['payment_schedule']
       
        if payment_schedule.exists():
            schedule = PaymentSchedule.objects.filter(organization__id=organizationId).first()
            schedule.payment_schedule = schedule_type
            schedule.save()
            return Response({'success': True}, status=status.HTTP_200_OK)
            
        else:
            organization = Organization.objects.get(id = organizationId )
            PaymentSchedule.objects.create(organization = organization,payment_schedule = schedule_type)
        
            return Response({'success': True,}, status=status.HTTP_200_OK)


from datetime import timedelta
class OrganizationTimeSheet(APIView):
    permission_classes = [IsAuthenticated]

    def get_total_hours_worked(self, timesheets):
        total_hours = sum(timesheet.hours_worked for timesheet in timesheets)
        return total_hours

    def get_payment_schedule(self, organization_id):
        payment_schedule = PaymentSchedule.objects.filter(organization__id=organization_id).first()
        return payment_schedule.payment_schedule if payment_schedule else 'Monthly'

    def get_current_month(self):
        return datetime.now().month

    def get(self, request, Id, format=None):
        auth_header = request.headers.get('Authorization', '')
        _, token = auth_header.split()
        # Check if the token is valid
        token_obj = Token.objects.get(key=token)
        user = token_obj.user
        # Assuming the organization is associated with the logged-in user
        organization_id = Id
       

        # Get the payment schedule for the organization
        payment_schedule = self.get_payment_schedule(organization_id)

        # Get all timesheets for employees in the organization
        timesheets = TimeSheet.objects.filter(organization__id=organization_id,status='Approved').exclude(user=user)#status='Approved'

        # add filter too if payment schedule is Bi-Weekly, Weekly
        if payment_schedule == 'Monthly':
            timesheets = timesheets.filter(start_date__month=self.get_current_month())  # Update with the current month
            
        elif payment_schedule == 'Bi-Weekly':
            # Assuming a bi-weekly schedule means the last two weeks
            today = datetime.now().date()
            two_weeks_ago = today - timedelta(days=14)
            timesheets = timesheets.filter(start_date__range=[two_weeks_ago, today])
        elif payment_schedule == 'Weekly':
            # Assuming a weekly schedule means the last week
            today = datetime.now().date()
            one_week_ago = today - timedelta(days=7)
            timesheets = timesheets.filter(start_date__range=[one_week_ago, today])

        # Group timesheets by employee
        timesheets_by_employee = {}
        for data in timesheets:
            if data.user.id not in timesheets_by_employee:
                timesheets_by_employee[data.user.id] = []
            timesheets_by_employee[data.user.id].append(data)

        all_timesheet = []
        for employee_id, employee_timesheets in timesheets_by_employee.items():
            total_hours_worked = self.get_total_hours_worked(employee_timesheets)
            membership = Membership.objects.get(user__id=employee_id,organization__id=organization_id)
            # Fetch additional data for the employee (e.g., department)
           
            org_data = {
                'employeeId': membership.user.id,
                'user': f"{membership.user.first_name} {membership.user.last_name}",
                'task_name': ', '.join([data.task_name for data in employee_timesheets]),
                'organization': ', '.join([data.organization.name for data in employee_timesheets]),
                'date': ', '.join([data.formatted_end_date() for data in employee_timesheets]),
                'hours_worked': total_hours_worked,
                'department': membership.department.title,
            }
            all_timesheet.append(org_data)

        return Response({'success': True, 'timesheets': all_timesheet}, status=status.HTTP_200_OK)


class CalculateSalaryAPIView(APIView):
    permission_classes = [AllowAny]

    def get_total_hours_worked(self, timesheets):
        total_hours = sum(timesheet.hours_worked for timesheet in timesheets)
        return total_hours

    def calculate_salary(self, total_hours_worked, hourly_rate):
        # Convert hourly_rate to Decimal before multiplication
        hourly_rate_decimal = Decimal(str(hourly_rate))

        return total_hours_worked * hourly_rate_decimal

    def get_payment_schedule(self, organization_id):
        payment_schedule = PaymentSchedule.objects.filter(organization__id=organization_id).first()
        return payment_schedule.payment_schedule if payment_schedule else 'Monthly'

    def post(self, request, user_id, format=None):
        # Assuming user_id is the ID of the employee for whom you want to calculate the salary
        timesheets = TimeSheet.objects.filter(user__id=user_id,status='Approved')#status='Approved'

        total_hours_worked = self.get_total_hours_worked(timesheets)

        hourly_rate = request.data.get('hourly_rate')
        if hourly_rate is None:
            return Response({'success': False, 'message': 'Hourly rate is required'}, status=status.HTTP_400_BAD_REQUEST)

        salary = self.calculate_salary(total_hours_worked, float(hourly_rate))
        print('salary:',salary,'total_hours_worked:',total_hours_worked)

        return Response({'success': True,'hourly_rate':hourly_rate ,'total_hours_worked': total_hours_worked, 'salary': salary}, status=status.HTTP_200_OK)





class SubmitPayrollAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request,Id, format=None):
        # Assuming the organization is associated with the logged-in user
        organization_id = Id
        payroll_data = request.data.get('payroll_data', [])

        total_salary = request.data.get('total_amount')
        print('payroll_data:',request.data)
        print('total_salary:',total_salary)
        organization = Organization.objects.get(id = organization_id)
        for payroll_entry in payroll_data:
            employee_id = payroll_entry.get('employeeId')
            hours_worked = payroll_entry.get('hours_worked')
            salary = payroll_entry.get('salary')
            hourly_rate = salary / hours_worked
            user  = myuser.objects.get(id = employee_id)
            
           

            print('hours_worked:',hours_worked)
            print('hourly_rate:', hourly_rate)
            print('employee_id:', employee_id)
            Payroll.objects.create(
                employee = user,
                organization = organization,
                hourly_rate = hourly_rate,
                salary_amount = salary
            )
            
            # You may want to calculate the salary_amount based on the hourly_rate and hours_worked
            #salary_amount = hourly_rate * hours_worked

            # Create or update the payroll entry
        if total_salary:
            Invoice.objects.create(organization=organization,total_amount = total_salary)
            

        return Response({'success': True, 'message': 'Payroll submitted successfully'}, status=status.HTTP_201_CREATED)


    


class PayRollHistory(APIView):
    permission_classes = [AllowAny]

    def get(self, request,Id, *args, **kwargs):
        
        payroll = Payroll.objects.filter(organization__id = Id)
        print('payroll:',payroll)
        
        all_requests = []
        for data in payroll:
            org_data = {
                'id': data.organization.id,
                'payId': data.id,
                'user': f"{data.employee.first_name} {data.employee.last_name}",
                'organization': data.organization.name,
                'date': data.date,
                'hourly_rate': data.hourly_rate,
                'salary_amount': data.salary_amount,
                'status': data.status,
               
            }
            all_requests.append(org_data)#
      
       
        return Response({'all_payroll':all_requests}, status=status.HTTP_200_OK)




class EmployeePayRollHistory(APIView):
    permission_classes = [AllowAny]

    def get(self, request,Id, *args, **kwargs):
        auth_header = request.headers.get('Authorization', '')
        _, token = auth_header.split()
        # Check if the token is valid
        token_obj = Token.objects.get(key=token)
        user = token_obj.user
        
        payroll = Payroll.objects.filter(organization__id = Id, employee = user)
        print('payroll:',payroll)
        
        all_requests = []
        for data in payroll:
            org_data = {
                'id': data.organization.id,
                'payId': data.id,
                'user': f"{data.employee.first_name} {data.employee.last_name}",
                'organization': data.organization.name,
                'date': data.date,
                'hourly_rate': data.hourly_rate,
                'salary_amount': data.salary_amount,
                'status': data.status,
               
            }
            all_requests.append(org_data)#
      
       
        return Response({'all_payroll':all_requests}, status=status.HTTP_200_OK)



class InvoiceList(APIView):
    permission_classes = [AllowAny]

    def get(self, request,Id, *args, **kwargs):
        
        payroll = Invoice.objects.filter(organization__id = Id)
        print('payroll:',payroll)
        
        all_requests = []
        for data in payroll:
            org_data = {
                'invoiceId': data.id,
                'id': data.organization.id,
                'organization': data.organization.name,
                'date': data.date,
                'salary_amount': data.total_amount,
               
            }
            all_requests.append(org_data)#
      
       
        return Response({'all_invoice':all_requests}, status=status.HTTP_200_OK)






class OrganizationRequestListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request,Id, *args, **kwargs):
       
        requests = Request.objects.filter(organization__id = Id)
        
        all_requests = []
        for data in requests:
            org_data = {
                'id': data.id,
                'employeeId': data.user.id,
                'user': f"{data.user.first_name} {data.user.last_name}",
                'organization': data.organization.name,
                'request_type': data.request_type,
                'start_date': data.start_date,
                'end_date': data.end_date,
                'status': data.status,
            }
            all_requests.append(org_data)#
      
       
        return Response({'all_requests':all_requests}, status=status.HTTP_200_OK)


class RequestStatusView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        requestId = request.data.get('requestId')
        request_status = request.data.get('status')
        print('request.data:',request.data)
        requests = Request.objects.get(id = requestId)
        print('requests.status:',requests.status )
        requests.status = request_status
        requests.save()
        print('requests.status:',requests.status )
        
        return Response({'success':True}, status=status.HTTP_200_OK)


class EmployeesTimesheetStatusView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        timesheetId = request.data.get('timesheetId')
        timesheet_status = request.data.get('status')
        timesheet = TimeSheet.objects.get(id = timesheetId)
        timesheet.organization_approved = timesheet_status
        timesheet.save()
        
        return Response({'success':True}, status=status.HTTP_200_OK)


class StaffTimesheetStatusView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        print("request.data.get('status'):",request.data.get('status'))
        timesheetId = request.data.get('timesheetId')
        timesheet_status = request.data.get('status')
        timesheet = TimeSheet.objects.get(id = timesheetId)
        
        timesheet.client_approved = timesheet_status
        timesheet.save()
        print('timesheet :',timesheet.client_approved )
        
        return Response({'success':True}, status=status.HTTP_200_OK)



class InstuctorLoginView(APIView):
    permission_classes = [AllowAny]
    #authentication_classes = [TokenAuthentication]

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, email=email, password=password)
        
       
        if user.is_instructor:
            print(request.data)
            login(request, user)
            serializer = MyUserSerializer(user)

            #return Response(serializer.data)
            token, created = Token.objects.get_or_create(user=user)
            
            user_data = {
                'id': user.id,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name, 
                'isLoggedIn':'true',
                'auth_token': token.key, 
                'isEmployer': user.is_employer,
            }
            print(user_data)
          
            return Response({'success': True, 'message': 'Login successful', 'user': user_data},status=status.HTTP_201_CREATED)
        else:
            return Response({'success': False, 'error': 'Invalid credentials'}, status=401)





class InstructorSignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = MyUserSerializer(data=request.data)
        print(request.data)
        if serializer.is_valid():
            
            user = serializer.save()
            user.set_password(request.data.get('password'))
            user.is_instructor = True
            user.save()
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            user_data = {
                'id': user.id,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'isLoggedIn':'true',
                'auth_token': token.key, 
                'isEmployer': user.is_employer,
            }
            return Response({'success': True, 'message': 'Signup successful', 'user': user_data}, status=status.HTTP_201_CREATED)
        return Response({'success': False, 'message': 'Signup failed', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)



class CourseCreateView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    
    def post(self, request, *args, **kwargs):
        auth_header = request.headers.get('Authorization', '')
        _, token = auth_header.split()
        # Check if the token is valid
        token_obj = Token.objects.get(key=token)
        user = token_obj.user
        print('data:',request.data,user)
       
       
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(instructor=user)  # Set the instructor to the current user
            
            return Response({'success': True, },status=status.HTTP_201_CREATED)
       
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





class CategoryListAPIView(APIView):
    def get(self, request, *args, **kwargs):
        
        categories = Categories.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SubCategoryListAPIView(APIView):
    def get(self, request, category_id, *args, **kwargs):
        try:
            category = Categories.objects.get(id=category_id)
        except Categories.DoesNotExist:
            return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)

        subcategories = SubCategories.objects.filter(category=category)
        serializer = SubCategorySerializer(subcategories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



class InstructorCoursesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        auth_header = request.headers.get('Authorization', '')
        _, token = auth_header.split()
        # Check if the token is valid
        token_obj = Token.objects.get(key=token)
        user = token_obj.user
        courses = Course.objects.filter(instructor=user)
        serializer = InstructorCourseSerializer(courses, many=True)
        all_courses = []
        for course in courses:
            course_data = {
                'id': course.id,
                'instructor': f"{course.instructor.first_name} {course.instructor.last_name}",
                'category': course.category.title,
                'subCategory': course.sub_category.title,
                'thumbnail': course.thumbnail.url,
                'description': course.description,
                'title': course.title,
    
            }
            all_courses.append(course_data)#
       
        return Response({'all_courses':all_courses}, status=status.HTTP_200_OK)












class SectionCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, course_id, *args, **kwargs):
        # Check if the course exists
        try:
            auth_header = request.headers.get('Authorization', '')
            _, token = auth_header.split()
            # Check if the token is valid
            token_obj = Token.objects.get(key=token)
            user = token_obj.user
            course = Course.objects.get(id=course_id, instructor=user)
        except Course.DoesNotExist:
            return Response({'error': 'Course not found or you do not have permission to add sections to this course.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = SectionSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save(course=course)
        
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CourseSectionsView(APIView):
    def get(self, request, course_id, *args, **kwargs):
        try:
            sections = Section.objects.filter(course_id=course_id)
            serializer = SectionSerializer(sections, many=True)
            
            # Manually serialize contents for each section
            data = []
            for section in serializer.data:
                section_id = section['id']
                contents = Content.objects.filter(section_id=section_id)
                content_serializer = ContentSerializer(contents, many=True)
                
                section['contents'] = content_serializer.data
                data.append(section)
               
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class ContentDetailView(APIView):
    def get(self, request, content_id, format=None):
        try:
            # Fetch content details based on content_id
            content = Content.objects.get(pk=content_id)
            serializer = ContentSerializer(content)
            print('serializer.data:',serializer.data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Content.DoesNotExist:
            return Response({"error": "Content not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, pk):
        content = Content.objects.get(pk=pk)
        serializer = ContentSerializer(content, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        content = Content.objects.get(pk=pk)
        content.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SectionContentsView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, section_id, *args, **kwargs):
        try:
            section = Section.objects.get(id=section_id)
            serializer = ContentSerializer(data=request.data)
            print(request.data,serializer.is_valid())

            if serializer.is_valid():
                serializer.save(section=section)

                # List all contents under the section after saving
                contents = section.contents.all()  # Assuming related name is 'contents'
                content_serializer = ContentSerializer(contents, many=True)

                return Response({
                    'content': serializer.data,
                    'section_contents': content_serializer.data,
                    'success':True,
                }, status=status.HTTP_201_CREATED)
            else:
                return Response({'success':False,'message':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Section.DoesNotExist:
            return Response({'error': 'Section not found','success':False}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e),'success':False}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




class UpdateSectionView(APIView):
    def put(self, request, section_id, *args, **kwargs):
        try:
            section = Section.objects.get(id=section_id)
            serializer = SectionSerializer(instance=section, data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Section.DoesNotExist:
            return Response({'error': 'Section not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DeleteSectionView(APIView):
    def delete(self, request, section_id, *args, **kwargs):
        try:
            section = Section.objects.get(id=section_id)
            section.delete()
            return Response({'message': 'Section deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except Section.DoesNotExist:
            return Response({'error': 'Section not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class UpdateContentView(APIView):
    def put(self, request, section_id, content_id, *args, **kwargs):
        try:
            section = Section.objects.get(id=section_id)
            content = Content.objects.get(id=content_id, section=section)
            print('request.data:',request.data)
            mutable_data = request.data.copy()
            content_file = request.data['content_file']
            if content_file == 'null':
                # If not present, remove the field from serializer's excluded fields
                mutable_data.pop('content_file', None)
            
            # Assuming you have a ContentSerializer for updating content
            serializer = ContentSerializer(instance=content, data=mutable_data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Section.DoesNotExist:
            return Response({'error': 'Section not found'}, status=status.HTTP_404_NOT_FOUND)
        except Content.DoesNotExist:
            return Response({'error': 'Content not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print('str(e):',str(e))
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DeleteContentView(APIView):
    def delete(self, request, section_id, content_id, *args, **kwargs):
        try:
            section = Section.objects.get(id=section_id)
            content = Content.objects.get(id=content_id, section=section)
            content.delete()
            
            return Response({'message': 'Content deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except Section.DoesNotExist:
            return Response({'error': 'Section not found'}, status=status.HTTP_404_NOT_FOUND)
        except Content.DoesNotExist:
            return Response({'error': 'Content not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class CourseListView(APIView):
    permission_classes = []
    authentication_classes = []
   
    def get(self, request, format=None):
        auth_header = request.headers.get('Authorization', '')
      
        if  auth_header != 'Token undefined':
            _, token = auth_header.split()
            
            # Check if the token is valid
            token_obj = Token.objects.get(key=token)
            user = token_obj.user
        else:
            user = None
        
        courses = Course.objects.all()
       

        all_courses = []
        for course in courses:
            is_enrolled = False
            if user:
                is_enrolled = Enrollment.objects.filter( enrolled_members=user, course=course).exists()
            course_data = {
                'id': course.id,
                'instructor': f"{course.instructor.first_name} {course.instructor.last_name}",
                'category': course.category.title,
                'subCategory': course.sub_category.title,
                'thumbnail': course.thumbnail.url,
                'description': course.description,
                'title': course.title,
                'is_enrolled':is_enrolled,
                #'discountPrice':calculateDiscount(discount.amount,course.price),
    
            }
            all_courses.append(course_data)#
        print('all_courses#@...:',all_courses)
       
        return Response({'all_courses':all_courses}, status=status.HTTP_200_OK)


class CourseDetailView(APIView):
    def get(self, request, pk):
        try:
            course = Course.objects.get(pk=pk)
            serializer = CourseDetailSerializer(course)
          
            course_data = {
                'id': course.id,
                'instructor': f"{course.instructor.first_name} {course.instructor.last_name}",
                'category': course.category.title,
                'subCategory': course.sub_category.title,
                'thumbnail': course.thumbnail.url,
                'description': course.description,
                'title': course.title,
                'overview': course.overview,
                'preview_video':course.preview_video.url if course.preview_video else '',
                
    
            }
           
           
            return Response(course_data , status=status.HTTP_200_OK)
        except Course.DoesNotExist:
            return Response({'detail': 'Course not found.'}, status=status.HTTP_404_NOT_FOUND)


class SectionListView(APIView):
    def get(self, request,courseId, format=None):
        sections = Section.objects.filter(course__id = courseId)
        print('sections..:',sections)
        serializer = SectionSerializer(sections, many=True)        
        # Manually serialize contents for each section
        data = []
        for section in serializer.data:
            section_id = section['id']
            contents = Content.objects.filter(section_id=section_id)
            content_serializer = ContentSerializer(contents, many=True)
            
            section['contents'] = content_serializer.data
            data.append(section)
       
        return Response(data, status=status.HTTP_200_OK)


class RequirementsCreateView(APIView):
    def post(self, request, course_id, format=None):
        # Assuming the course_id is passed as a parameter in the URL
        data = request.data.copy()
        data['course'] = course_id

        serializer = RequirementsSerializer(data=data)
        if serializer.is_valid():
            serializer.save()

            # Fetch all requirements for the associated course after posting
            requirements = Requirements.objects.filter(course__id=course_id)
            requirements_serializer = RequirementsSerializer(requirements, many=True)

            return Response({
                'success': True,
                'message': 'Requirement created successfully',
                'requirements': requirements_serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response({'success': False, 'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, course_id, format=None):
        requirements = Requirements.objects.filter(course__id=course_id)
        serializer = RequirementsSerializer(requirements, many=True)
        print(' requirements :', requirements )
       
        return Response(serializer.data)


class RequirementsUpdateAPIView(APIView):
    def put(self, request, course_id, requirement_id, format=None):
        data = request.data.copy()
        data['course'] = course_id
       
        try:
            requirement = Requirements.objects.get(pk=requirement_id, course_id=course_id)
        except Requirements.DoesNotExist:
            return Response({'error': 'Requirement not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = RequirementsSerializer(requirement, data=data)
        if serializer.is_valid():
            serializer.save()
            #return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({'success': True, 'data': serializer.data}, status=status.HTTP_200_OK)
       
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RequirementsDeleteAPIView(APIView):
    def delete(self, request, course_id, requirement_id, format=None):
        try:
            requirement = Requirements.objects.get(pk=requirement_id, course_id=course_id)
        except Requirements.DoesNotExist:
            return Response({'error': 'Requirement not found'}, status=status.HTTP_404_NOT_FOUND)

        requirement.delete()
        return Response({'success': True}, status=status.HTTP_200_OK)
        


class ObjectivesCreateView(APIView):
    def post(self, request, course_id, format=None):
        # Assuming the course_id is passed as a parameter in the URL
        data = request.data.copy()
        data['course'] = course_id
       
        serializer = ObjectivesSerializer(data=data)
        if serializer.is_valid():
            serializer.save()

            # Fetch all requirements for the associated course after posting
            objectives = Objectives.objects.filter(course__id=course_id)
            objectives_serializer = ObjectivesSerializer(objectives, many=True)

            return Response({
                'success': True,
                'message': 'Objective created successfully',
                'objectives': objectives_serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response({'success': False, 'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, course_id, format=None):
       
        objectives = Objectives.objects.filter(course__id=course_id)
        serializer = ObjectivesSerializer(objectives, many=True)
        print('objectives:',objectives)
        return Response(serializer.data)




class ObjectivesUpdateAPIView(APIView):
    def put(self, request, course_id, requirement_id, format=None):
        data = request.data.copy()
        data['course'] = course_id
       
        try:
            objectives = Objectives.objects.get(pk=requirement_id, course_id=course_id)
        except Objectives.DoesNotExist:
            return Response({'error': 'objectives not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ObjectivesSerializer(objectives, data=data)
        if serializer.is_valid():
            serializer.save()
            #return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({'success': True, 'data': serializer.data}, status=status.HTTP_200_OK)
      
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ObjectivesDeleteAPIView(APIView):
    def delete(self, request, course_id, requirement_id, format=None):
        try:
            objective = Objectives.objects.get(pk=requirement_id, course_id=course_id)
        except Objectives.DoesNotExist:
            return Response({'error': 'objectives not found'}, status=status.HTTP_404_NOT_FOUND)

        objective.delete()
        return Response({'success': True}, status=status.HTTP_200_OK)
        



class ContentTypeCountView(APIView):
    def get(self, request, course_id, format=None):
        try:
            # Get the course
            course = Course.objects.get(pk=course_id)

            # Get distinct content types related to the course
            content_types = Content.objects.filter(section__course=course).values('content_type').distinct()

            # Count the number of each content type
            content_counts = []
            for content_type in content_types:
                count = Content.objects.filter(section__course=course, content_type=content_type['content_type']).count()
                content_counts.append({'content_type': content_type['content_type'], 'count': count})
          
            serializer = ContentTypeCountSerializer(content_counts, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Course.DoesNotExist:
            return Response({'error': 'Course not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)








class InstructorProfileCreateView(APIView):
    #permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # Assuming the user is authenticated, you can access the user through request.user
       
        
        auth_header = request.headers.get('Authorization', '')
        
        _, token = auth_header.split()
        
        # Check if the token is valid
        token_obj = Token.objects.get(key=token)
        user = token_obj.user
        data = request.data.copy()
        data['user'] = user.id
       

        # Validate the data sent in the request
        serializer = InstructorProfileSerializer(data=data)
        if serializer.is_valid():
            # Save the profile with the associated user
            serializer.save(user=user)
            print('serializer.data:',serializer.data)
            return Response({'success':True,'data':serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class FetchInstructorProfile(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    def get(self, request, *args, **kwargs):
        auth_header = request.headers.get('Authorization', '')
        
        _, token = auth_header.split()
        
        # Check if the token is valid
        token_obj = Token.objects.get(key=token)
        user = token_obj.user
        print('exist..:',InstructorProfile.objects.filter(user = user).exists())
        if InstructorProfile.objects.filter(user = user).exists():
            profile = InstructorProfile.objects.get(user = user)
            profile_data = {
                'title':profile.title,
                'biography':profile.biography,
                'website':profile.website,
                'picture':profile.picture.url if profile.picture else '',
                'phone':profile.phone,
                'exist':True,
            }
            print(' profile_data :', profile_data )
            return Response({'success': True,'data':profile_data}, status=status.HTTP_200_OK)
        else:
             return Response({'success': False,'data':{'exist':False,}}, status=status.HTTP_200_OK)
      



class InstructorProfileEditView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def put(self, request, *args, **kwargs):
        auth_header = request.headers.get('Authorization', '')
        
        _, token = auth_header.split()
        
        # Check if the token is valid
        token_obj = Token.objects.get(key=token)
        user = token_obj.user
        try:
            # Retrieve the user's profile
            profile = InstructorProfile.objects.get(user=user)

            # Check if the user making the request is the profile owner
            self.check_object_permissions(request, profile)
            mutable_data = request.data.copy()
            picture = request.data['picture']
            if picture == '':
                # If not present, remove the field from serializer's excluded fields
                mutable_data.pop('picture', None)

            # Serialize the existing profile data
            serializer = InstructorProfileSerializer(profile, data=mutable_data, partial=True)

            if serializer.is_valid():
                # Update the profile with the new data
                serializer.save()

                return Response({'success': True, 'data': serializer.data}, status=status.HTTP_200_OK)
            else:
                return Response({'success': False, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        except InstructorProfile.DoesNotExist:
            # Handle the case where the profile is not found
            return Response({'success': False, 'error_message': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            # Handle other exceptions and return an error response
            return Response({'success': False, 'error_message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




      
   
class EditCourseView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, course_id, *args, **kwargs):
        auth_header = request.headers.get('Authorization', '')
        
        _, token = auth_header.split()
        
        # Check if the token is valid
        token_obj = Token.objects.get(key=token)
        user = token_obj.user
        # Get the course to be updated
        mutable_data = request.data.copy()
        print('request.data:',request.data)
        thumbnail = request.data['thumbnail']
        preview_video = request.data['preview_video']
        print('thumbnail:',thumbnail,preview_video)

        if Course.objects.filter(id=course_id, instructor = user).exists():
            course = Course.objects.get(id=course_id)
            if thumbnail == '':
                # If not present, remove the field from serializer's excluded fields
                mutable_data.pop('thumbnail', None)
            if preview_video == '':
                # If not present, remove the field from serializer's excluded fields
                mutable_data.pop('preview_video', None)

            
            serializer = CourseSerializer(course, data=mutable_data, partial=True)
            
            if serializer.is_valid():
                # Update the course with the new data
                serializer.save()
                return Response({'success': True, 'data': serializer.data}, status=status.HTTP_200_OK)

        else:
            return Response({'success': False, 'error_message': 'Course not found'}, status=status.HTTP_404_NOT_FOUND)

   
class SearchCoursesView(APIView):
    def get(self, request, *args, **kwargs):
        query = request.query_params.get('query', '')
        print('query:',query)
        # Customize the search logic based on your requirements
        courses = Course.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) | 
            Q(category__title__icontains=query) |
            Q(sub_category__title__icontains=query) 
           
        )
        
        all_courses = []
        for course in courses:
            course_data = {
                'id': course.id,
                'instructor': f"{course.instructor.first_name} {course.instructor.last_name}",
                'category': course.category.title,
                'subCategory': course.sub_category.title,
                'thumbnail': course.thumbnail.url,
                'description': course.description,
                'title': course.title,
               
                
    
            }
            all_courses.append(course_data)#
        print(all_courses)
        #serializer = CourseSerializer(queryset, many=True)
        return Response({'all_courses':all_courses}, status=status.HTTP_200_OK)





class FetchProfileView(APIView):
    #permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request, *args, **kwargs):
        auth_header = request.headers.get('Authorization', '')
        _, token = auth_header.split()
        
        # Check if the token is valid
        token_obj = Token.objects.get(key=token)
        user = token_obj.user
       
        if InstructorProfile.objects.filter(user=user).exists():
            profile = InstructorProfile.objects.get(user=user)
            
            user_data = {
                'first_name':profile.user.first_name,
                'last_name':profile.user.last_name,
                'picture':profile.picture.url if profile.picture  else '',
                'title':profile.title,
                'biography':profile.biography, 
                'website':profile.website,
                'phone':profile.phone,
            }
            print(user_data)
            return Response({'data':user_data,'success':True}, status=status.HTTP_200_OK)
        else:
            return Response({'success':False}, status=status.HTTP_404_NOT_FOUND)
        



class CheckCourseOwnerView(APIView):
    #permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request,courseId, *args, **kwargs):
        auth_header = request.headers.get('Authorization', '')
        _, token = auth_header.split()
        
        # Check if the token is valid
        token_obj = Token.objects.get(key=token)
        user = token_obj.user
       
        if Course.objects.filter(instructor=user,id = courseId).exists():
            return Response({'success':True}, status=status.HTTP_200_OK)
        else:
            return Response({'success':False}, status=status.HTTP_404_NOT_FOUND)
     



class EnrollOrganizationInCourse(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, course_id, *args, **kwargs):
        
        auth_header = request.headers.get('Authorization', '')
        _, token = auth_header.split()
        
        # Check if the token is valid
        token_obj = Token.objects.get(key=token)
        user = token_obj.user
        print(' request.data:', request.data,user)
        # Assuming the user making the request is the organization or employer
        organization = Organization.objects.get(employer=user,id = request.data['organisation'])
        course = Course.objects.get(id=course_id)

        # Create an enrollment record
        if Enrollment.objects.filter(course=course, organization=organization).exists():
            return Response({'success': False, 'message': 'Already enrolled'}, status=status.HTTP_200_OK)
        else:
            try:
                enrollment = Enrollment.objects.create(course=course, organization=organization)
                
                # Enroll all members of the organization in the course
                enrollment.enrolled_members.set(organization.employees.all())
                enrollment.enrolled_members.add(user)

                serializer = EnrollmentSerializer(enrollment)
                return Response({'success': True, 'data': serializer.data}, status=status.HTTP_200_OK)

            except Organization.DoesNotExist:
                return Response({'success': False, 'error_message': 'Organization not found'}, status=status.HTTP_404_NOT_FOUND)





class FetchOrganizations(APIView):
    #permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request, *args, **kwargs):
        auth_header = request.headers.get('Authorization', '')
        _, token = auth_header.split()
        
        # Check if the token is valid
        token_obj = Token.objects.get(key=token)
        user = token_obj.user
        organization = Organization.objects.filter(employer = user)
        all_organizations = []
        for data in organization:
            org_data = {
                'logo':data.logo.url if data.logo else "",
                'id': data.id,
                'employer': f"{data.employer.first_name} {data.employer.last_name}",
                'name': data.name,
                'is_enrolled': '**Already enrolled' if Enrollment.objects.filter(organization__id=data.id).exists() else ''
   
            }
            all_organizations.append(org_data)#
       
        print('all_organizations:',all_organizations)
        return Response({'all_organization':all_organizations,'success':True}, status=status.HTTP_200_OK)


class FetchOrganizationsListCourse(APIView):
    #permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request,courseId, *args, **kwargs):
        auth_header = request.headers.get('Authorization', '')
        _, token = auth_header.split()
        
        # Check if the token is valid
        token_obj = Token.objects.get(key=token)
        user = token_obj.user
        organization = Organization.objects.filter(employer = user)
        all_organizations = []
        for data in organization:
            org_data = {
                'logo':data.logo.url if data.logo else "",
                'id': data.id,
                'employer': f"{data.employer.first_name} {data.employer.last_name}",
                'name': data.name,
                'is_enrolled': '**Already enrolled' if Enrollment.objects.filter(course__id = courseId,organization__id=data.id).exists() else ''
   
            }
            all_organizations.append(org_data)#
       
        print('all_organizations:',all_organizations)
        return Response({'all_organization':all_organizations,'success':True}, status=status.HTTP_200_OK)







class CheckOrganizationEnrollmentView(APIView):
    authentication_classes = [TokenAuthentication]


    def get(self, request, course_id, *args, **kwargs):
        auth_header = request.headers.get('Authorization', '')
        _, token = auth_header.split()
        
        # Check if the token is valid
        token_obj = Token.objects.get(key=token)
        user = token_obj.user
        #organization = Organization.objects.filter(employer = user)
      
        enrollment = Enrollment.objects.filter(enrolled_members = user,course__id=course_id)
        print('enrollment.exists():',enrollment.exists())
        if enrollment.exists():
            enrollment = Enrollment.objects.filter(enrolled_members = user,course__id=course_id)
           
            return Response({'enrolled': True}, status=status.HTTP_200_OK)
        else:
            return Response({'enrolled': False}, status=status.HTTP_200_OK)








class CheckEnrollmentView(APIView):
    authentication_classes = [TokenAuthentication]


    def get(self, request, course_id, *args, **kwargs):
        auth_header = request.headers.get('Authorization', '')
        _, token = auth_header.split()
        
        # Check if the token is valid
        token_obj = Token.objects.get(key=token)
        user = token_obj.user
      
        enrollment = Enrollment.objects.filter(enrolled_members =user, course__id=course_id)
        print('enrollment.exists():',enrollment.exists())
        if enrollment.exists():
            enrollment = Enrollment.objects.filter(enrolled_members =user, course__id=course_id)
           
            return Response({'enrolled': True}, status=status.HTTP_200_OK)
        else:
            return Response({'enrolled': False}, status=status.HTTP_200_OK)


      


class EnrolledCoursesView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = [TokenAuthentication]


    def get(self, request, *args, **kwargs):
        auth_header = request.headers.get('Authorization', '')
        _, token = auth_header.split()
        
        # Check if the token is valid
        token_obj = Token.objects.get(key=token)
        user = token_obj.user
        print('user :',user )
        # Retrieve the enrolled courses for the authenticated user
        enrolled_courses = Enrollment.objects.filter(enrolled_members=user)
        
        all_courses = []
        for enrollment in enrolled_courses:
            course = enrollment.course
            course_data = {
                'id': course.id,
                'instructor': f"{course.instructor.first_name} {course.instructor.last_name}",
                'category': course.category.title,
                'subCategory': course.sub_category.title,
                'thumbnail': course.thumbnail.url,
                'description': course.description,
                'title': course.title,
                'overview': course.overview,
               
            }
            all_courses.append(course_data)
        
        # Return the serialized data in the response
        return Response({'all_courses': all_courses}, status=status.HTTP_200_OK)




class CreateEmployeeProfileAPIView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = [TokenAuthentication]

    def post(self, request, *args, **kwargs):
        
        auth_header = request.headers.get('Authorization', '')
        _, token = auth_header.split()
        
        # Check if the token is valid
        token_obj = Token.objects.get(key=token)
        user = token_obj.user
        print('user :',user )

        # Check if the user already has an employee profile
        if Employee.objects.filter(user=user).exists():
            return Response({'success': False, 'message': 'Employee profile already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        # Create an employee profile for the user
        serializer = EmployeeSerializer(data=request.data,partial=True)
        print(serializer.is_valid())
        if serializer.is_valid():
            serializer.save(user=user)
            return Response({'success': True, 'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'success': False, 'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)



class CreateClientProfile(APIView):
    permission_classes = [AllowAny]
    authentication_classes = [TokenAuthentication]

    def post(self, request, *args, **kwargs):
        
        auth_header = request.headers.get('Authorization', '')
        _, token = auth_header.split()
        
        # Check if the token is valid
        token_obj = Token.objects.get(key=token)
        user = token_obj.user
        print('user :',user )

        # Check if the user already has an employee profile
        if ClientProfile.objects.filter(user=user).exists():
            return Response({'success': False, 'message': 'Client profile already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        # Create an employee profile for the user
        serializer = ClientProfileSerializer(data=request.data,partial=True)
        print(serializer.is_valid())
        if serializer.is_valid():
            serializer.save(user=user)
            return Response({'success': True, 'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'success': False, 'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)




class FetchClientProfile(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    def get(self, request, *args, **kwargs):
        auth_header = request.headers.get('Authorization', '')
        
        _, token = auth_header.split()
        
        # Check if the token is valid
        token_obj = Token.objects.get(key=token)
        user = token_obj.user
        print('profile_data :', ClientProfile.objects.filter(user = user).exists(),user.is_client )
        if ClientProfile.objects.filter(user = user).exists():
            profile = ClientProfile.objects.get(user = user)
            profile_data = {
                'date_of_birth':profile.date_of_birth,
                'gender':profile.gender,
                'marital_status':profile.marital_status,
                'picture':profile.image.url if profile.image else '',
                'previous_picture':profile.image.name if profile.image else '',
                'address':profile.address,
                'phone':profile.phone_number,
                'exist':True,
            }
            print('profile_data :', profile_data )
            return Response({'success': True,'data':profile_data}, status=status.HTTP_200_OK)
        else:
             return Response({'success': False,'data':{'exist':False,}}, status=status.HTTP_200_OK)
      



class FetchEmployeeProfile(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    def get(self, request, *args, **kwargs):
        auth_header = request.headers.get('Authorization', '')
        
        _, token = auth_header.split()
        
        # Check if the token is valid
        token_obj = Token.objects.get(key=token)
        user = token_obj.user
       
        if Employee.objects.filter(user = user).exists():
            profile = Employee.objects.get(user = user)
            profile_data = {
                'date_of_birth':profile.date_of_birth,
                'gender':profile.gender,
                'marital_status':profile.marital_status,
                'picture':profile.image.url if profile.image else '',
                'address':profile.address,
                'phone':profile.phone_number,
                'exist':True,
            }
            print(' profile_data :', profile_data )
            return Response({'success': True,'data':profile_data}, status=status.HTTP_200_OK)
        else:
             return Response({'success': False,'data':{'exist':False,}}, status=status.HTTP_200_OK)


class EmployeeProfileEditView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def put(self, request, *args, **kwargs):
        auth_header = request.headers.get('Authorization', '')
        
        _, token = auth_header.split()
        
        # Check if the token is valid
        token_obj = Token.objects.get(key=token)
        user = token_obj.user
        try:
            # Retrieve the user's profile
            profile = Employee.objects.get(user=user)

            # Check if the user making the request is the profile owner
            self.check_object_permissions(request, profile)
            mutable_data = request.data.copy()
            picture = request.data['image']
            if picture == '':
                # If not present, remove the field from serializer's excluded fields
                mutable_data.pop('image', None)

            # Serialize the existing profile data
            serializer = EmployeeSerializer(profile, data=mutable_data, partial=True)

            if serializer.is_valid():
                # Update the profile with the new data
                serializer.save()

                return Response({'success': True, 'data': serializer.data}, status=status.HTTP_200_OK)
            else:
                return Response({'success': False, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        except Employee.DoesNotExist:
            # Handle the case where the profile is not found
            return Response({'success': False, 'error_message': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            # Handle other exceptions and return an error response
            return Response({'success': False, 'error_message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class ClientProfileEditView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def put(self, request, *args, **kwargs):
        auth_header = request.headers.get('Authorization', '')
        
        _, token = auth_header.split()
        
        # Check if the token is valid
        token_obj = Token.objects.get(key=token)
        user = token_obj.user
        try:
            # Retrieve the user's profile
            profile = ClientProfile.objects.get(user=user)

            # Check if the user making the request is the profile owner
            self.check_object_permissions(request, profile)
            mutable_data = request.data.copy()
            picture = request.data['image']
            if picture == '':
                # If not present, remove the field from serializer's excluded fields
                mutable_data.pop('image', None)

            # Serialize the existing profile data
            serializer = ClientProfileSerializer(profile, data=mutable_data, partial=True)

            if serializer.is_valid():
                # Update the profile with the new data
                serializer.save()

                return Response({'success': True, 'data': serializer.data}, status=status.HTTP_200_OK)
            else:
                return Response({'success': False, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        except ClientProfile.DoesNotExist:
            # Handle the case where the profile is not found
            return Response({'success': False, 'error_message': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            # Handle other exceptions and return an error response
            return Response({'success': False, 'error_message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)






class CreateEmployerProfileAPIView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = [TokenAuthentication]

    def post(self, request, *args, **kwargs):
        
        auth_header = request.headers.get('Authorization', '')
        _, token = auth_header.split()
        
        # Check if the token is valid
        token_obj = Token.objects.get(key=token)
        user = token_obj.user
        print('user :',user )

        # Check if the user already has an employee profile
        if Employer.objects.filter(user=user).exists():
            return Response({'success': False, 'message': 'Employer profile already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        # Create an employee profile for the user
        serializer = EmployerSerializer(data=request.data,partial=True)
       
        if serializer.is_valid():
            serializer.save(user=user)
            return Response({'success': True, 'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'success': False, 'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)





class FetchEmployerProfile(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    def get(self, request, *args, **kwargs):
        auth_header = request.headers.get('Authorization', '')
        
        _, token = auth_header.split()
        
        # Check if the token is valid
        token_obj = Token.objects.get(key=token)
        user = token_obj.user
        print('exists:',Employer.objects.filter(user = user).exists())
        if Employer.objects.filter(user = user).exists():
            profile = Employer.objects.get(user = user)
            
            profile_data = {
                'date_of_birth':profile.date_of_birth,
                'gender':profile.gender,
                'marital_status':profile.marital_status,
                'picture':profile.image.url if profile.image else '',
                'previousPicture':profile.image.name if profile.image else '',
                'address':profile.address,
                'phone':profile.phone_number,
                'exist':True,
            }
            print(' profile_data :', profile_data )
            return Response({'success': True,'data':profile_data}, status=status.HTTP_200_OK)
        else:
             return Response({'success': False,'data':{'exist':False,}}, status=status.HTTP_200_OK)
      




class EmployerProfileEditView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def put(self, request, *args, **kwargs):
        auth_header = request.headers.get('Authorization', '')
        
        _, token = auth_header.split()
        
        # Check if the token is valid
        token_obj = Token.objects.get(key=token)
        user = token_obj.user
        try:
            # Retrieve the user's profile
            profile = Employer.objects.get(user=user)

            # Check if the user making the request is the profile owner
            self.check_object_permissions(request, profile)
            mutable_data = request.data.copy()
            picture = request.data['image']
            if picture == '':
                # If not present, remove the field from serializer's excluded fields
                mutable_data.pop('image', None)

            # Serialize the existing profile data
            serializer = EmployerSerializer(profile, data=mutable_data, partial=True)

            if serializer.is_valid():
                # Update the profile with the new data
                serializer.save()

                return Response({'success': True, 'data': serializer.data}, status=status.HTTP_200_OK)
            else:
                return Response({'success': False, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        except Employer.DoesNotExist:
            # Handle the case where the profile is not found
            return Response({'success': False, 'error_message': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            # Handle other exceptions and return an error response
            return Response({'success': False, 'error_message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




class PayRollStatusView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        Id = request.data.get('Id')
        pay_status = request.data.get('status')
        payroll = Payroll.objects.get(id = Id)
        payroll.status = pay_status
        payroll.save()
        print('requests:',request.data)
        
        return Response({'success':True}, status=status.HTTP_200_OK)






class FetchUserProfile(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    def get(self, request, *args, **kwargs):
        auth_header = request.headers.get('Authorization', '')
        
        _, token = auth_header.split()
        
        # Check if the token is valid
        token_obj = Token.objects.get(key=token)
        user = token_obj.user
        print('user.is_employee:',user.is_employee)
       
        if user.is_employee:
            if Employee.objects.filter(user = user).exists():
                profile = Employee.objects.get(user = user)
                profile_data = {
                    'picture':profile.image.url if profile.image else '',
                    'exist':True,
                }
                print(' profile_data :', profile_data )
                return Response({'success': True,'data':profile_data}, status=status.HTTP_200_OK)
            else:
                return Response({'success': False,'data':{'exist':False,}}, status=status.HTTP_200_OK)
        if user.is_employer:
            if Employer.objects.filter(user = user).exists():
                profile = Employer.objects.get(user = user)
                profile_data = {
                    'picture':profile.image.url if profile.image else '',
                    'exist':True,
                }
                print(' profile_data :', profile_data )
                return Response({'success': True,'data':profile_data}, status=status.HTTP_200_OK)
            else:
                return Response({'success': False,'data':{'exist':False,}}, status=status.HTTP_200_OK)

        if user.is_instructor :
            if InstructorProfile.objects.filter(user = user).exists():
                profile = InstructorProfile.objects.get(user = user)
                profile_data = {
                    'picture':profile.picture.url if profile.picture else '',
                    'exist':True,
                }
                print(' profile_data :', profile_data )
                return Response({'success': True,'data':profile_data}, status=status.HTTP_200_OK)
            else:
                return Response({'success': False,'data':{'exist':False,}}, status=status.HTTP_200_OK)
        if user.is_client :
            print('dd:',ClientProfile.objects.filter(user = user).exists())
            if ClientProfile.objects.filter(user = user).exists():
                profile = ClientProfile.objects.get(user = user)
                print('profile:',profile)
                profile_data = {
                    'picture':profile.image.url if profile.image else '',
                    'exist':True,
                }
                print(' profile_data :', profile_data )
                return Response({'success': True,'data':profile_data}, status=status.HTTP_200_OK)
            else:
                return Response({'success': False,'data':{'exist':False,}}, status=status.HTTP_200_OK)




#servername = 'hrmsappserver'
#admin = 'hrmsadmin'
#pass = Nkere5uwem
#hrms-email

      




class ClientSignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = MyUserSerializer(data=request.data)
        print(request.data)
        if serializer.is_valid():
            
            user = serializer.save()
            user.set_password(request.data.get('password'))
            user.is_client = True
            user.save()
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            user_data = {
                'id': user.id,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'isLoggedIn':'true',
                'auth_token': token.key, 
                'isEmployer': user.is_employer,
            }
            return Response({'success': True, 'message': 'Signup successful', 'user': user_data}, status=status.HTTP_201_CREATED)
        return Response({'success': False, 'message': 'Signup failed', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)




class FetchInvitation(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    def get(self, request,invitation_code, *args, **kwargs):
        auth_header = request.headers.get('Authorization', '')
        
        _, token = auth_header.split()
        
        # Check if the token is valid
        token_obj = Token.objects.get(key=token)
        user = token_obj.user
        print('invitation_code:',invitation_code)
        if ClientInvitation.objects.filter(invitation_code = invitation_code).exists():
            invitation = ClientInvitation.objects.get(invitation_code = invitation_code)
            if invitation.is_accepted:
                return Response({'success': False,}, status=status.HTTP_200_OK)
            else:
                data = {
                    'organization':invitation.organization.name,
                }
                return Response({'success': True,'data': data}, status=status.HTTP_200_OK)
        else:
            return Response({'success': False,}, status=status.HTTP_200_OK)
      




class AcceptClientInvitation(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        auth_header = request.headers.get('Authorization', '')
        
        _, token = auth_header.split()
        
        # Check if the token is valid
        token_obj = Token.objects.get(key=token)
        user = token_obj.user
        invitation_code  = request.data['invitation_code']
        print(request.data)
        invitation = ClientInvitation.objects.get(invitation_code  = invitation_code )
        invitation.is_accepted =True
        invitation.save()
        if Client.objects.filter(organization = invitation.organization,clients = user).exists():
            return Response({'success': False, 'message': "You've already joined this organization",}, status=status.HTTP_201_CREATED)
        else:
            client = Client.objects.create(organization = invitation.organization,hourly_rate = invitation.hourly_rate)
            client.clients.add(user)
            client.hourly_rate  = invitation.hourly_rate
            return Response({'success': True, 'message': 'successful',}, status=status.HTTP_201_CREATED)




class AcceptEmployeeInvitation(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        auth_header = request.headers.get('Authorization', '')
        
        _, token = auth_header.split()
        
        # Check if the token is valid
        token_obj = Token.objects.get(key=token)
        user = token_obj.user
        invitation_code  = request.data['invitation_code']
        print(request.data)
        invitation = Invitation.objects.get(invitation_code  = invitation_code )
        if Organization.objects.filter(id = invitation.organization.id,employees = user).exists():
            return Response({'success': False, 'message': "You've already joined this organization",}, status=status.HTTP_201_CREATED)
        else:
            invitation.is_accepted =True
            invitation.save()

            organization = Organization.objects.get(id = invitation.organization.id)
            organization.employees.add(user)
            # Mark the invitation as accepted
            
            Membership.objects.create(
                user = user,
                organization = organization,
                department = invitation.department
            )
            if Enrollment.objects.filter(organization=organization).exists():
                enrollment = Enrollment.objects.filter(organization=organization).first()
                enrollment.enrolled_members.add(user)
            return Response({'success': True, 'message': 'successful',}, status=status.HTTP_201_CREATED)
        




class FetchEmployeeInvitation(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    def get(self, request,invitation_code, *args, **kwargs):
        auth_header = request.headers.get('Authorization', '')
        
        _, token = auth_header.split()
        
        # Check if the token is valid
        token_obj = Token.objects.get(key=token)
        user = token_obj.user
        print('invitation_code:',invitation_code)
        if Invitation.objects.filter(invitation_code = invitation_code).exists():
            invitation = Invitation.objects.get(invitation_code = invitation_code)
            if invitation.is_accepted:
                return Response({'success': False,}, status=status.HTTP_200_OK)
            else:
                data = {
                    'organization':invitation.organization.name,
                }
                return Response({'success': True,'data': data}, status=status.HTTP_200_OK)
        else:
            return Response({'success': False,}, status=status.HTTP_200_OK)
      





class ClientOrganizationListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        # Get the authenticated user
        auth_header = request.headers.get('Authorization', '')
        
        _, token = auth_header.split()
        
        # Check if the token is valid
        token_obj = Token.objects.get(key=token)
        user = token_obj.user

        # Get the organizations for which the user is a client
        client_organizations = Client.objects.filter(clients=user)
        all_organizations = []
        for data in client_organizations:
          
            org_data = {
                'id': data.organization.id,
                'employer': f"{data.organization.employer.first_name} {data.organization.employer.last_name}",
                'name': data.organization.name,
                'overview': data.organization.overview,
                'logo': data.organization.logo.url if data.organization.logo else '',
                'employee_count': data.organization.employees.count(),
                'organization_type': data.organization.organization_type,
            }
            all_organizations.append(org_data)#
        return Response({'success': True, 'all_organizations':all_organizations}, status=status.HTTP_201_CREATED)

       
class ClientListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, Id, format=None):
        # Get the authenticated user
        auth_header = request.headers.get('Authorization', '')
        
        _, token = auth_header.split()
        
        # Check if the token is valid
        token_obj = Token.objects.get(key=token)
        user = token_obj.user

        # Get the organizations for which the user is a client
        client_organizations = Client.objects.filter(organization__id=Id)
        
        all_clients = []
        for data in client_organizations:
            #client_data = []
            print('data:',data)
            for client in data.clients.all():  # Iterate over the related clients
                client_data = {
                    'id': data.id,
                    'userId': client.id,
                    'name': f"{client.first_name} {client.last_name}",
                    'organization':data.organization.name,
                    'hourly_rate':data.hourly_rate,
                    # Add other fields as needed
                }
            all_clients.append(client_data)
        print('all_clients:',all_clients)
        
        return Response({'success': True, 'all_clients': all_clients}, status=status.HTTP_201_CREATED)




class ClientAssignmentCreateView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        print(data)
        auth_header = request.headers.get('Authorization', '')
        _, token = auth_header.split()
        # Check if the token is valid
        token_obj = Token.objects.get(key=token)
        user = token_obj.user
        #organization = Organization.objects.get(id = data.organization)
        #print(organization)
        if Assignment.objects.filter(organization__id = data['organization'],client__id = data['client'],staff__id =data['staff']).exists():
            print('EXIST')
            return Response({'success': False,'message':"Client already assign to employee."}, status=status.HTTP_201_CREATED)

        serializer = AssignmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            #print('serializer:',serializer)
            #serializer.save(invited_by = user)
            # Perform any additional actions (e.g., sending an email with the invitation code)
            return Response({'success': True}, status=status.HTTP_201_CREATED)

        return Response({'success': False,'message':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)





class UserTimeSheetDetail(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request,Id, *args, **kwargs):
        auth_header = request.headers.get('Authorization', '')
        _, token = auth_header.split()
        # Check if the token is valid
        token_obj = Token.objects.get(key=token)
        user = token_obj.user
       
        timesheet = TimeSheet.objects.get(id = Id)
        print('timesheet:',timesheet)
        
        all_timesheet = []
        print('timesheet.client:',timesheet.client)
        if timesheet.client != None:
            for item in timesheet.client.clients.all():

                org_data = {
                    'id': timesheet.id,
                    'user': f"{timesheet.user.id}",
                    'organization':timesheet.organization.id, 
                    'client':f"{timesheet.client.id}", 
                    'client_name':f"{item.first_name} {item.last_name}",
                    'has_client':'exist',
                    'start_date':timesheet.formatted_start_date(), 
                    'end_date':timesheet.formatted_end_date(),                
                    'total_hours':timesheet.total_hours, 
                    'hours_worked_sat': timesheet.hours_worked_sat,
                    'hours_worked_sun': timesheet.hours_worked_sun,
                    'hours_worked_mon': timesheet.hours_worked_mon,
                    'hours_worked_tue': timesheet.hours_worked_tue,
                    'hours_worked_wed': timesheet.hours_worked_wed,
                    'hours_worked_thur': timesheet.hours_worked_thur,
                    'hours_worked_fri': timesheet.hours_worked_fri,

                    'allowance_sat': timesheet.allowance_sat,
                    'allowance_sun': timesheet.allowance_sun,
                    'allowance_mon': timesheet.allowance_mon,
                    'allowance_tue': timesheet.allowance_tue,
                    'allowance_wed': timesheet.allowance_wed,
                    'allowance_thur': timesheet.allowance_thur,
                    'allowance_fri': timesheet.allowance_fri,

                    'activity_description_sat': timesheet.activity_description_sat,
                    'activity_description_sun': timesheet.activity_description_sun,
                    'activity_description_mon': timesheet.activity_description_mon,
                    'activity_description_tue': timesheet.activity_description_tue,
                    'activity_description_wed': timesheet.activity_description_wed,
                    'activity_description_thur': timesheet.activity_description_thur,
                    'activity_description_fri': timesheet.activity_description_fri,

                    'client_approved':timesheet.client_approved, 
                    'organization_approved':timesheet.organization_approved, 
                    'final_approval':timesheet.final_approval, 
                }
                all_timesheet.append(org_data)
        else:
            org_data = {
                'id': timesheet.id,
                'user': f"{timesheet.user.id}",
                'organization':timesheet.organization.id, 
                #'client':f"{timesheet.client.id}", 
                #'client_name':f"{item.first_name} {item.last_name}",
                'has_client':'',
                'start_date':timesheet.formatted_start_date(), 
                'end_date':timesheet.formatted_end_date(),                
                'total_hours':timesheet.total_hours, 
                'hours_worked_sat': timesheet.hours_worked_sat,
                'hours_worked_sun': timesheet.hours_worked_sun,
                'hours_worked_mon': timesheet.hours_worked_mon,
                'hours_worked_tue': timesheet.hours_worked_tue,
                'hours_worked_wed': timesheet.hours_worked_wed,
                'hours_worked_thur': timesheet.hours_worked_thur,
                'hours_worked_fri': timesheet.hours_worked_fri,

                'allowance_sat': timesheet.allowance_sat,
                'allowance_sun': timesheet.allowance_sun,
                'allowance_mon': timesheet.allowance_mon,
                'allowance_tue': timesheet.allowance_tue,
                'allowance_wed': timesheet.allowance_wed,
                'allowance_thur': timesheet.allowance_thur,
                'allowance_fri': timesheet.allowance_fri,

                'activity_description_sat': timesheet.activity_description_sat,
                'activity_description_sun': timesheet.activity_description_sun,
                'activity_description_mon': timesheet.activity_description_mon,
                'activity_description_tue': timesheet.activity_description_tue,
                'activity_description_wed': timesheet.activity_description_wed,
                'activity_description_thur': timesheet.activity_description_thur,
                'activity_description_fri': timesheet.activity_description_fri,

                'client_approved':timesheet.client_approved, 
                'organization_approved':timesheet.organization_approved, 
                'final_approval':timesheet.final_approval, 
            }
            all_timesheet.append(org_data)
        
        

        print('$%%%%%:', all_timesheet)
        return Response(all_timesheet, status=status.HTTP_200_OK)

    def put(self, request, Id, format=None):
        timesheet = TimeSheet.objects.get(id = Id)
        print('request.data:',request.data)
        serializer = TimeSheetSerializer(timesheet, data=request.data,partial = True)
        if serializer.is_valid():
            print('valid:')
            serializer.save()
            return Response(serializer.data)
        print('serializer.errors:',serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class ClientStaffsListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request,Id, *args, **kwargs):
        auth_header = request.headers.get('Authorization', '')
        _, token = auth_header.split()
        # Check if the token is valid
        token_obj = Token.objects.get(key=token)
        user = token_obj.user
       
        assignments = Assignment.objects.filter(organization__id = Id,client__clients = user )
        
        all_members = []
        for data in assignments:
            for item in data.staff.all():
                org_data = {
                'id': data.id,
                'userId': item.id,
                'first_name': item.first_name,
                'last_name':item.last_name,
                'organization':data.organization.name, 
                #'status':data.status, 

    
            }
            all_members.append(org_data)#
        print('all_members:',all_members)
        
       
        return Response(all_members, status=status.HTTP_200_OK)




class ClientRateUpdate(APIView):
    permission_classes = [AllowAny]
    #authentication_classes = [TokenAuthentication]

    def put(self, request,*args, **kwargs):
        print('request.data:',request.data)
        
        client = Client.objects.filter(id = request.data['clientId'])
        # Retrieve the organization based on the user making the request
        if client.exists():
            result = Client.objects.get(id = request.data['clientId'])
            result.hourly_rate = request.data['hourly_rate']
            result.save()
           
            return Response({'success': True, },status=status.HTTP_201_CREATED)
       
        return Response({'success': False,'message':'An error occured'}, status=status.HTTP_400_BAD_REQUEST)


class OrganizationRateUpdate(APIView):
    permission_classes = [AllowAny]
    #authentication_classes = [TokenAuthentication]

    def post(self, request,*args, **kwargs):
        
        Id = request.data['organizationId']
        rate = OrganizationRate.objects.filter(organization__id = Id)
       
        organization = Organization.objects.get(id = Id)
        # Retrieve the organization based on the user making the request
        if rate.exists():
            result = OrganizationRate.objects.get(organization__id = Id)
            result.hourly_rate = request.data['hourly_rate']
            result.save()
            return Response({'success': True, },status=status.HTTP_201_CREATED)
        else:
            OrganizationRate.objects.create(organization = organization,hourly_rate =  request.data['hourly_rate'])
            return Response({'success': True, },status=status.HTTP_201_CREATED)

       
        #return Response({'success': False,'message':'An error occured'}, status=status.HTTP_400_BAD_REQUEST)






class TimesheetApproval(APIView):
    def put(self, request, Id, format=None):
        timesheet = TimeSheet.objects.get(id = Id)
       
        print('timesheet.final_approval:######', timesheet.final_approval)
        serializer = TimeSheetSerializer(timesheet, data=request.data,partial = True)
        if serializer.is_valid():
            print('valid:')
            serializer.save()
            timesheet.final_approval = True
            timesheet.organization_approved = "Processing"
            timesheet.client_approved = "Processing"
            timesheet.save()
            email = timesheet.user.email
            subject = 'Timesheet status changed'
            body = f'Hi, Your timesheet has changed from processing to processed. The timesheet has now been processed for payment and you should recieve your  Payslip /  self Bill remittance on the portal within 24hours. If you are paid through an umbrella company, they will shortly be receiving the details from us. if you have any queries, please contact us. Regards'
            from_email = 'hmrs@nobtec.co.uk'  # Replace with your email
            recipient_list = [email]
            password = "URc9JUctpRXF"

            
            message = MIMEMultipart()
            message['From'] = from_email
            message['To'] = ', '.join(recipient_list)
            message['Subject'] = subject

            # Attach the body to the message
            message.attach(MIMEText(body, 'plain'))

            # Connect to the SMTP server
            with smtplib.SMTP_SSL("smtp.zoho.eu", port=465) as connection:
                # Login to the server
                connection.login(user=from_email, password=password)
                
                # Send the email
                connection.sendmail(from_addr=from_email, to_addrs=recipient_list, msg=message.as_string())
                connection.quit()
        return Response({'success': True, }, status=status.HTTP_200_OK)



class UserTimesheetDelete(APIView):
    def delete(self, request, Id, format=None):
        timesheet = TimeSheet.objects.get(id = Id)
        
        
        timesheet.delete()
        return Response({'success': True, }, status=status.HTTP_200_OK)    



from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordResetConfirmView
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.urls import reverse
class PasswordResetRequestView(APIView):
    serializer_class = PasswordResetSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = myuser.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)

            reset_url = reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
           
            main_link = f'https://mango-field-0800b630f.4.azurestaticapps.net{reset_url}'
            reset_link = request.build_absolute_uri(reset_url)
            print(' reset_url:',  reset_link)
            
            subject = 'Password Reset Request'
            body = f'Click the following link to reset your password: {main_link}'
            from_email = 'hmrs@nobtec.co.uk'  # Replace with your email
            recipient_list = [email]
            password = "URc9JUctpRXF"

            
            message = MIMEMultipart()
            message['From'] = from_email
            message['To'] = ', '.join(recipient_list)
            message['Subject'] = subject

            # Attach the body to the message
            message.attach(MIMEText(body, 'plain'))

            # Connect to the SMTP server
            with smtplib.SMTP_SSL("smtp.zoho.eu", port=465) as connection:
                # Login to the server
                connection.login(user=from_email, password=password)
                
                # Send the email
                connection.sendmail(from_addr=from_email, to_addrs=recipient_list, msg=message.as_string())
                connection.quit()

            return Response({'success': 'Password reset email sent'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode

class CustomPasswordResetConfirmView(APIView):
    def post(self, request, uidb64, token):
        serializer = PasswordResetSerializer(data=request.data)
        password = request.data['password']
        #print('request.data:',uidb64,token)
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = myuser.objects.get(pk=uid)
        print('uid:',uid)
        
        if not default_token_generator.check_token(user, token):
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            user.set_password(password)
            user.save()
            return Response({'success': 'Password reset successfully'}, status=status.HTTP_200_OK)
           

        
    