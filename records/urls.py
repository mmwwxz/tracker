from django.urls import path
from . import views
from django.shortcuts import redirect


urlpatterns = [
    path('', lambda request: redirect('home') if request.user.is_authenticated else redirect('login'), name='login'),

    path('records/', views.record_list, name='record_list'),
    path('add-records/', views.add_record, name='add_record'),
    path('export-records/', views.export_records, name='export_records'),
    path('edit-record/<int:pk>/', views.edit_record, name='edit_record'),
    path('delete_all_records/', views.delete_all_records, name='delete_all_records'),
    path('delete_record/<int:pk>/', views.delete_record, name='delete_record'),
]
