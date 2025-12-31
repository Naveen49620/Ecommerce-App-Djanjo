from django.contrib import admin  
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name="home"),

    # Auth
    path('register/', views.register, name="register"),
    path('login/', views.login_page, name="login"),
    path('logout/', views.logout_page, name="logout"),

    # Cart
    path('cart/', views.cart_page, name="cart"),
    path('addtocart/', views.add_to_cart, name="addtocart"),
    path('delete-cart/', views.delete_cart_item, name='delete_cart'),


    # Favourite
    path('fav/', views.fav_page, name="fav"),   # AJAX add-to-fav
    path('favviewpage/', views.favviewimage, name="favviewpage"),  # HTML favourites page
    path('remove_fav/<str:cid>/', views.reomve_cart, name="remove_fav"),

    # Collections
    path('collections/', views.collections, name="collections"),
    path('collections/<str:name>/', views.collectionsview, name="collectionsview"),

    # Product details
    path('collections/<str:cname>/<str:pname>/', views.product_details, name="product_details"),
]
