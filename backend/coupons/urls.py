from django.urls import path
from .views import CheckCouponView

urlpatterns =[
    # will have query parameter
    path('check-coupon', CheckCouponView.as_view())
]