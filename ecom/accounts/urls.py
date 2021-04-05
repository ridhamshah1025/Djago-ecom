from django.urls import path, include
from . import views
urlpatterns = [

    path('home/', views.home, name="home"),
    path('home_generic/', views.home_generic.as_view(), name="home_generic"),
    path('login/', views.user_login, name="login"),
    path('logout/', views.user_logout, name="logout"),
    path('login_page/', views.login_page, name="login_page"),
    path('add_to_cart/', views.add_to_cart, name="add_to_cart"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('payment/', views.payment, name="payment"),
    path('confirm_order/', views.confirm_order, name="confirm_order"),
    path('search_result/', views.search_result, name="search_result"),
    path('contact/', views.contact, name="contact"),
    path('user_profile/', views.user_profile, name="user_profile"),
    path('single_product/<int:pk>/', views.single_product, name="single_product"),
    path('shop_category/', views.shop_category, name="shop_category"),
    path('category_result/', views.category_result, name="category_result"),
    path('shop_brand/', views.shop_brand, name="shop_brand"),
    path('brand_result/', views.brand_result, name="brand_result"),
    path('update/', views.update, name="update"),
    path('delete_cart/', views.delete_cart, name="delete_cart"),
]
