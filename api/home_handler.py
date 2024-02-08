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
from django.core import serializers

from . import http_handler
@api_view(['POST'])
def home(request):
    if not request.is_authenticated:
        return http_handler.get_http_response({"message": "Unauthorized"}, status=401)
    return http_handler.get_http_response({"message": "Welcome to home page!!!"}, status=200)