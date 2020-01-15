from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index , name="index"),
    path('candidform', views.candidForm , name="candidForm"),
    path('candidlist', views.candidList , name="candidList"),
    path('candidbulk', views.candidBulk , name="candidBulk"),
    path('accounts/logout/', views.logoutView , name="logoutView"),
    path('cnotfound', views.certificateNotFound , name="certificateNotFound"),
    path('mail_sent/<slug:alcher_id>', views.send_email , name="send_email"),
    path('candidupdate/<int:tpk>', views.candidUpdateForm , name="candidUpdateForm"),
    re_path(r'^certificate/(?P<cert_id>ALC-[A-Z]{3}-[0-9]+-20[0-9]{2}-[0-9]+)/$', views.certificate , name="certificate"),
]

