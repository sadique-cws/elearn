from django.contrib import admin
from django.urls import path, include
from cws.views import *
urlpatterns = [
    path('',HomeView.as_view(),name="homepage"),
    path('c/<slug>/',CourseView.as_view(),name="course"),
    path('cart/',OrderSummary.as_view(),name="cart"),
    path('add-to-cart/<str:slug>/',AddToCart.as_view(),name="add-cart"),
]
