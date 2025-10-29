from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('upload_customer/', views.upload_customer, name='upload_customer'),
    path('export_customer/', views.export_customer, name='export_customer'),

    path('upload_book/', views.upload_book, name='upload_book'),
    path('export_book/', views.export_book, name='export_book'),

    path('upload_bookshop/', views.upload_bookshop, name='upload_bookshop'),
    path('export_bookshop/', views.export_bookshop, name='export_bookshop'),

    path('upload_availability/', views.upload_availability, name='upload_availability'),
    path('export_availability/', views.export_availability, name='export_availability'),
]