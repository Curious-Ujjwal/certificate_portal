from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index , name="index"),
    path('candidform', views.candidForm , name="candidForm"),
    path('candidlist', views.candidList , name="candidList"),
    path('accounts/logout/', views.logoutView , name="logoutView"),
    path('mail_sent/<slug:alcher_id>', views.send_email , name="send_email"),
    re_path(r'^certificate/(?P<cert_id>ALC-[A-Z]{3}-[0-9]+-20[0-9]{2}-[0-9]+)/$', views.certificate , name="certificate"),
]

