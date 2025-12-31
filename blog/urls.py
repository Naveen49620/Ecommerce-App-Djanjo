from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('header/', views.header, name='header'),
    path('post/<int:post_id>/', views.postinfo, name='postinfo'),
    path('contact/',views.contact, name='contact'),
    path('about/',views.about, name='about')

]


