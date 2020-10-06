from django.contrib import admin
from django.urls import path, include
from cws.views import *
urlpatterns = [
    path('',HomeView.as_view(),name="homepage"),
    path('c/<slug>/',CourseView.as_view(),name="course"),
    path('cartview/',CartView.as_view(),name="cart"),
    path('Dashboard/',Dashboard.as_view(),name="dashboard"),
]
