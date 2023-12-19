from . import views
from django.urls import path
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index),
    path('index/', views.index, name='index'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('contact/', views.contact, name='contact'),
    path('product?product_id=<int:product_id>/', views.detail, name='product_detail'),
    path('login/', views.login_form, name='login'),
    path('logout/',auth_views.LogoutView.as_view(next_page='/'),name='logout'),
    path('register/', views.register, name='register'),
    path('shop/', views.shop, name='shop'),
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('send_email/<str:email_ids>/', views.send_email_view, name='send_email'),
    path('search-products/', views.search_products, name='search_products'),
    path('subscribe/', views.subscribe, name='subscribe'),
    path('send_message/', views.send_message, name='send_message'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('remove_from_cart/', views.remove_from_cart, name='remove_from_cart'),
    path('place_order/', views.place_order, name='place_order'),
    path('order_done/', views.order_done, name='order_done'),
    path('profile/', views.profile_view, name='profile'),
    path('api/product-categories/', views.product_categories, name='product-categories'),
    path('api/add-review/', views.add_review, name='add_review'),
]
