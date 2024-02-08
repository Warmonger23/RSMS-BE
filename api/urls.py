from django.urls import path
from . import user_handler, home_handler, rent_item_handler

#URLConf
urlpatterns = [
    path("login/", user_handler.login),
    path("signup/", user_handler.sign_up),
    path("forgot/", user_handler.forgot_password),
    path("updatepassword/", user_handler.update_password),
    path("home/", home_handler.home),
    path("fetchuserdetails/", user_handler.fetch_user_details),
    path("createrentitem/", rent_item_handler.create_rent_item),
    path("fetchrentitems/", rent_item_handler.fetch_rent_items)
]
