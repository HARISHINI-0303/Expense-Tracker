from django.urls import path
from .import views

urlpatterns=[
    path("",views.home,name="home"),
    path("register/",views.register,name="register"),
    path("login/",views.login,name="login"),
    path("main/",views.main,name="main"),
    path("reports/",views.reports,name="reports"),
    path("logout/",views.logout,name="logout"),

]