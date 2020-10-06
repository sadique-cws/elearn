from django.urls import path
from cws.views import *
urlpatterns = [
    path('', HomeView.as_view(), name="homepage"),
    path('c/<slug>/', CourseView.as_view(), name="course"),
    path('cart/', OrderSummary.as_view(), name="cart"),
    path('add-to-cart/<str:slug>/', AddToCart.as_view(), name="add-cart"),
    path('remove-from-cart/<str:slug>/', RemoveCartItem.as_view(), name="remove-from-cart"),
    path('add-coupon/', add_coupon, name="add-coupon"),
    path('remove-coupon/', RemoveAppliedCoupon.as_view(), name="remove-coupon"),
]
