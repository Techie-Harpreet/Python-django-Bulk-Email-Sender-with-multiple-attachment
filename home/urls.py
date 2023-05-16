from .views import *
from django.urls import path,include
urlpatterns = [
    path('' ,Home , name="Home"),
    path('bulk-mail' , Bulk_mail_send , name="Bulk_mail_send"),
    path('single-mail' , Single_mail_send , name="Single_mail_send"),
    path('register' , register_page ,name="register_page"),
    path('login', login_page, name="login_page"),
    path('logout', Logout, name="Logout"),



]