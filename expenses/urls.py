from django.urls import path
from . import views
from django.shortcuts import redirect


urlpatterns = [
    path('', lambda request: redirect('home') if request.user.is_authenticated else redirect('login'), name='login'),

    path('expenses/', views.expenses_list, name='expenses_list'),
    path('add-expense/', views.add_expense, name='add_expense'),
    path('export-expenses/', views.export_expenses, name='export_expenses'),
    path('edit-expenses/<int:pk>/', views.edit_expense, name='edit_expense'),
    path('delete_all/', views.delete_all_expenses, name='delete_all_expenses'),
    path('delete_expense/<int:pk>/', views.delete_expense, name='delete_expense'),
]

