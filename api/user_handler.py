from django.shortcuts import render
from django.http import HttpResponse
import django.http as http
from api.models import User, Rent_Items
import json
from rest_framework.decorators import api_view
from django.http import JsonResponse
import jwt
from datetime import datetime, timedelta
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from . import http_handler, token_handler

@api_view(['POST'])
def login(request):
    data = json.loads(request.body)
    request_user = User(**data)
    query_res = User.objects.filter(email_id=request_user.email_id)
    if query_res.count() != 1:
        return http_handler.get_http_response({"message": "Unauthorized"}, status=401)
    if request_user.password != query_res.get().password:
        return http_handler.get_http_response({"message": "Unauthorized"}, status=401)
    token = token_handler.generate_jwt(query_res.get().id)
    return http_handler.get_http_response({"message": "Success", "token": token}, status=200)

@api_view(['POST'])
def sign_up(request):
    data = json.loads(request.body)
    u = User(**data)
    u.set_role_type("CUSTOMER")
    try:
        u.full_clean()
    except Exception as e:
        print("unable to login ", e)
        return http_handler.get_http_response({"message": "Unauthorized"}, status=401)
    u.save()
    token = token_handler.generate_jwt(u.id)
    return http_handler.get_http_response({"message": "Success", "token": token}, status=200)

@api_view(['POST'])
def forgot_password(request):
    data = json.loads(request.body)
    if "email_id" not in data:
        return http_handler.get_http_response({"message": "email id is missing"}, status=403)
    u = User(**data)
    query_res = User.objects.filter(email_id=u.email_id)
    if query_res.count() != 1:
        return http_handler.get_http_response({"message": "Unauthorized"}, status=401)
    content = "<strong>localhost:8000/forgot?token=%s</strong>" % (token_handler.generate_jwt(u.id))
    message = Mail(
        from_email='isshaikh@iu.edu',
        to_emails=u.email_id,
        subject='You forgot your password dumbass!',
        html_content=content
    )
    sg = SendGridAPIClient("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")
    response = sg.send(message)
    return http_handler.get_http_response({"message": "Welcome to forgot page!!!"}, status=200)

@api_view(['POST'])
def update_password(request):
    data = json.loads(request.body)
    if "token" not in data or "password" not in data:
        return http_handler.get_http_response({"message": "invalid params"}, status=403)
    jwt_token = data["token"]
    password = data["password"]
    try:
        jwt_res = token_handler.decode_jwt(jwt_token)
        token_time = (datetime.strptime(jwt_res["ttl"], '%Y-%m-%d %H:%M:%S.%f'))
        if token_time < datetime.now():
            return http_handler.get_http_response({"message": "link expired"}, status=403)
        user_id = jwt_res["user_id"]
        query_res = User.objects.filter(id=user_id).update(password=password)
        if query_res != 1:
            return http_handler.get_http_response({"message": "invalid params"}, status=403)
        return http_handler.get_http_response(None, status=200)
    except Exception as e:
        print("exception while jwt verify", e)
        return http_handler.get_http_response({"message": "jwt verficiation failed"}, status=401)


@api_view(['POST'])
def fetch_user_details(request):
    data = json.loads(request.body)
    request_user = User(**data)
    query_res = User.objects.filter(email_id=request_user.email_id)
    if query_res.count() != 1:
        return http_handler.get_http_response({"message": "Unauthorized"}, status=401)
    if request_user.password != query_res.get().password:
        return http_handler.get_http_response({"message": "Unauthorized"}, status=401)
    user_details = {"first_name": query_res.get().first_name, "last_name": query_res.get().last_name, "email_id": query_res.get().email_id, "password": query_res.get().password}
    return http_handler.get_http_response(user_details, status=200)