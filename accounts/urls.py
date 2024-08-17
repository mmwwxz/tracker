from django.urls import path
from . import views
from django.shortcuts import redirect


urlpatterns = [
    path('', lambda request: redirect('home') if request.user.is_authenticated else redirect('custom_login'), name='login'),
    path('home/', views.home, name='home'),
    path('login/', views.login_view, name='custom_login'),  # Изменено имя маршрута для входа
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),

    # path('not-found/', views.not_found, name='not_found'),
]
