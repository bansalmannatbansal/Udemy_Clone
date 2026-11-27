from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("courses/", views.courses, name="courses"),
    path("courses/<slug:slug>/", views.course_detail, name="course_detail"),
    path("pricing/", views.pricing, name="pricing"),
    path("login/", views.login_view, name="login"),
    path("signup/", views.signup_view, name="signup"),
    path("logout/", views.logout_view, name="logout"),
]
