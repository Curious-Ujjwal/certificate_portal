from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index , name="index"),
    path('accounts/logout/', views.logoutView , name="logoutView"),
    re_path(r'^certificate/(?P<cert_id>ALC-[A-Z]{3}-[0-9]+-20[0-9]{2}-[0-9]+)/$', views.certificate , name="certificate"),
]

