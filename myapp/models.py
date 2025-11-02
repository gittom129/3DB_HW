from django.db import models

class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    age = models.IntegerField()
    date_join = models.DateField()

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200)
    edition = models.CharField(max_length=50)
    author = models.CharField(max_length=100)
    language = models.CharField(max_length=50)
    publisher = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.title} ({self.edition})"


class Bookshop(models.Model):
    shop_name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    shop_tel = models.CharField(max_length=20)
    shop_email = models.EmailField()

    def __str__(self):
        return self.shop_name


class BookAvailability(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    edition = models.CharField(max_length=50,default="1st")  # keep track of the specific edition
    shop = models.ForeignKey(Bookshop, on_delete=models.CASCADE)
    available_copies = models.IntegerField(default=0)

    class Meta:
        unique_together = ('book', 'edition', 'shop')  # prevent duplicates

    def __str__(self):
        return f"{self.book.title} @ {self.shop.shop_name}"
