from django.urls import path
from . import views

urlpatterns = [
    # Home page
    path('', views.home, name='home'),

    # ---------------- Upload CSV routes ----------------
    # Keep the old "lambda" approach to match your current HTML forms
    path('upload_customer/', lambda request: views.upload_csv(request, 'customer'), name='upload_customer'),
    path('upload_book/', lambda request: views.upload_csv(request, 'book'), name='upload_book'),
    path('upload_bookshop/', lambda request: views.upload_csv(request, 'bookshop'), name='upload_bookshop'),
    path('upload_availability/', lambda request: views.upload_csv(request, 'availability'), name='upload_availability'),

    # ---------------- Export CSV routes ----------------
    path('export/customer/', views.export_customer, name='export_customer'),
    path('export/book/', views.export_book, name='export_book'),
    path('export/bookshop/', views.export_bookshop, name='export_bookshop'),
    path('export/availability/', views.export_availability, name='export_availability'),
]