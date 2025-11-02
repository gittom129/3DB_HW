from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Customer, Book, Bookshop, BookAvailability
import csv
from io import TextIOWrapper

def home(request):
    return render(request, "home.html")

def upload_csv(request, model_name):
    model_map = {
        "customer": Customer,
        "book": Book,
        "bookshop": Bookshop,
        "availability": BookAvailability,
    }

    model_class = model_map.get(model_name)
    if not model_class:
        return HttpResponse("Invalid model name", status=400)

    if request.method == "POST":
        csv_file = request.FILES.get("csv_file")
        if not csv_file:
            return redirect("/?error=No+file+uploaded")

        file_data = TextIOWrapper(csv_file.file, encoding="utf-8-sig")
        reader = csv.DictReader(file_data)

        created, skipped = 0, 0

        for row in reader:
            if model_name == "customer":
                exists = model_class.objects.filter(
                    name=row["name"], email=row["email"]
                ).exists()
                if not exists:
                    model_class.objects.create(
                        name=row["name"],
                        email=row["email"],
                        age=row["age"],
                        date_join=row["date_join"]
                    )

            elif model_name == "book":
                exists = model_class.objects.filter(
                    title=row["title"], edition=row["edition"]
                ).exists()
                if not exists:
                    model_class.objects.create(
                        title=row["title"],
                        edition=row["edition"],
                        author=row["author"],
                        language=row["language"],
                        publisher=row["publisher"]
                    )

            elif model_name == "bookshop":
                exists = model_class.objects.filter(
                    shop_name=row["shop_name"], location=row["location"]
                ).exists()
                if not exists:
                    model_class.objects.create(
                        shop_name=row["shop_name"],
                        location=row["location"],
                        shop_tel=row["shop_tel"],
                        shop_email=row["shop_email"]
                    )

            elif model_name == "availability":
                book = Book.objects.get(title=row["book_title"], edition=row["edition"])
                shop = Bookshop.objects.get(shop_name=row["available_shop"])

                exists = model_class.objects.filter(
                    book=book,
                    edition=row["edition"],
                    shop=shop
                ).exists()

                if not exists:
                    model_class.objects.create(
                        book=book,
                        edition=row["edition"],
                        shop=shop,
                        available_copies=int(row.get("available_copies", 0))
                    )

            # Count records
            if not exists:
                created += 1
            else:
                skipped += 1

        # Render after the loop, not inside it
        return render(request,
                      "home.html",
                      {"message": f"{created} records inserted successfully, {skipped} duplicates skipped."})

    return redirect("/")

def export_customer(request):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="customers.csv"'
    writer = csv.writer(response)
    writer.writerow(["name", "email", "age", "date_join"])
    for c in Customer.objects.all():
        writer.writerow([c.name, c.email, c.age, c.date_join])
    return response

def export_book(request):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="books.csv"'
    writer = csv.writer(response)
    writer.writerow(["title", "edition", "author", "language", "publisher"])
    for b in Book.objects.all():
        writer.writerow([b.title, b.edition, b.author, b.language, b.publisher])
    return response

def export_bookshop(request):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="bookshops.csv"'
    writer = csv.writer(response)
    writer.writerow(["shop_name", "location", "shop_tel", "shop_email"])
    for s in Bookshop.objects.all():
        writer.writerow([s.shop_name, s.location, s.shop_tel, s.shop_email])
    return response

def export_availability(request):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="availability.csv"'
    writer = csv.writer(response)
    writer.writerow(["book_title", "edition", "available_shop","available_copies"])
    for a in BookAvailability.objects.all():
        writer.writerow([a.book, a.edition, a.shop, a.available_copies])
    return response