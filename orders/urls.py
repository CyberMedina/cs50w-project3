from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register_view, name="register"),
    path('addCart/<int:product_id>/', views.addCart, name='addCart'),
    path('deleteCart/', views.deleteCart, name='deleteCart'),
    path('createOrder', views.createOrder, name='createOrder'),
]
