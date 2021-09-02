from django.contrib import admin
from django.urls import path, re_path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static


"""
Djoser urls for this project:
auth/users/: Create a user
auth/users/me/: Delete a user  
auth/users/reset_password/: Reset a password via a user's email 
auth/users/reset_password_confirm/: Confirm a password 
                                    by a url above.      
auth/jwt/create/: User login and create access and refresh token   
auth/jwt/refresh/: Token refresh  
auth/jwt/verify/: Verify a access token.
"""

urlpatterns = [

    # Urls for Djoser
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('auth/', include('djoser.social.urls')),

    # Url for apps
    path('api/user/', include('user.urls')),
    path('api/category/', include('category.urls')),
    path('api/coupon/', include('coupons.urls')),
    path('api/products/', include('product.urls')),
    path('api/cart/', include('cart.urls')),
    path('api/shipping/', include('shipping.urls')),
    path('api/orders/', include('orders.urls')),
    path('api/payment/', include('payment.urls')),
    path('api/profile/', include('user_profile.urls')),
    path('api/reviews/', include('reviews.urls')),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



# Using at React
# Catch all urls not included urls above.
urlpatterns += [re_path(r'^.*',
                        TemplateView.as_view(template_name='index.html'))]




