import csv
from io import TextIOWrapper
from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponse
from .models import Customer, Book, Bookshop, BookAvailability

# Home page
def home(request, message=None):
    return render(request, 'home.html', {'message': message})

# Generic upload function
def upload_csv(request, model_class, fields, special_handler=None):
    message = ""
    if request.method == 'POST':
        csv_file = request.FILES.get('csv_file')
        if not csv_file:
            message = "No file uploaded!"
            return render(request, 'home.html', {'message': message})

        csv_text = TextIOWrapper(csv_file.file, encoding='utf-8-sig')
        reader = csv.DictReader(csv_text)
        inserted_count = 0

        for row in reader:
            try:
                if special_handler:
                    special_handler(row)
                else:
                    obj_data = {field: row[field] for field in fields}
                    if 'age' in obj_data:
                        obj_data['age'] = int(obj_data['age'])
                    if 'date_join' in obj_data:
                        obj_data['date_join'] = datetime.strptime(obj_data['date_join'], '%Y-%m-%d').date()
                    model_class.objects.create(**obj_data)
                inserted_count += 1
            except Exception as e:
                print("Error:", e)
                continue
        message = f"{inserted_count} records inserted successfully!"
    return render(request, 'home.html', {'message': message})

# Export function
def export_csv(model_class, fields, filename):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{filename}.csv"'
    writer = csv.writer(response)
    writer.writerow(fields)
    for obj in model_class.objects.all().values_list(*fields):
        writer.writerow(obj)
    return response

# Customer
def upload_customer(request):
    return upload_csv(request, Customer, ['name', 'email', 'age', 'date_join'])

def export_customer(request):
    return export_csv(Customer, ['name', 'email', 'age', 'date_join'], 'customers')

# Book
def upload_book(request):
    return upload_csv(request, Book, ['title', 'edition', 'author', 'language', 'publisher'])

def export_book(request):
    return export_csv(Book, ['title', 'edition', 'author', 'language', 'publisher'], 'books')

# Bookshop
def upload_bookshop(request):
    return upload_csv(request, Bookshop, ['shop_name', 'location', 'shop_tel', 'shop_email'])

def export_bookshop(request):
    return export_csv(Bookshop, ['shop_name', 'location', 'shop_tel', 'shop_email'], 'bookshops')

# BookAvailability handler
def handle_availability(row):
    book = Book.objects.filter(title=row['book_title'], edition=row['edition']).first()
    shop = Bookshop.objects.filter(shop_name=row['available_shop']).first()
    if book and shop:
        BookAvailability.objects.create(
            book=book,
            shop=shop,
            available_copies=int(row.get('available_copies', 0))
        )

def upload_availability(request):
    return upload_csv(request, BookAvailability, [], special_handler=handle_availability)

def export_availability(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="availability.csv"'
    writer = csv.writer(response)
    writer.writerow(['book_title', 'edition', 'available_shop', 'available_copies'])
    for obj in BookAvailability.objects.select_related('book', 'shop'):
        writer.writerow([obj.book.title, obj.book.edition, obj.shop.shop_name, obj.available_copies])
    return response