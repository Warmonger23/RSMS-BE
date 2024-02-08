from django.shortcuts import render
from django.http import HttpResponse
import django.http as http
from api.models import User, Rent_Items
import json
from rest_framework.decorators import api_view
from . import http_handler

@api_view(['POST'])
def create_rent_item(request):
    data = json.loads(request.body)
    RentItem = Rent_Items(**data)
    qry = Rent_Items.objects.filter(number_plate=RentItem.number_plate)
    if qry.count() == 1:
        return http_handler.get_http_response({"message": "Item is already registered to rent"}, status=401)
    else:
        RentItem.save()
        return http_handler.get_http_response({"message": "Item Registered"}, status=200)


@api_view(['GET'])
def fetch_rent_items(request):
    Show = Rent_Items.objects.all().defer('created_at')[:9]
    if Show.count() == 0:
        return http_handler.get_http_response({"message": "No Items available to rent."}, status=200)
    else:

        return http_handler.get_http_response(list(Show.values()), status=200)
