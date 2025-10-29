from django.contrib import admin
from .models import Customer, Book, Bookshop, BookAvailability

# ----------------- Customer -----------------
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'age', 'date_join')  # Columns shown in admin list
    search_fields = ('name', 'email')                    # Add search box
    list_filter = ('date_join',)                         # Filter by date_join
    ordering = ('name',)                                 # Default ordering

# ----------------- Book -----------------
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'edition', 'author', 'language', 'publisher')
    search_fields = ('title', 'author', 'publisher')
    list_filter = ('language', 'publisher')
    ordering = ('title', 'edition')

# ----------------- Bookshop -----------------
@admin.register(Bookshop)
class BookshopAdmin(admin.ModelAdmin):
    list_display = ('shop_name', 'location', 'shop_tel', 'shop_email')
    search_fields = ('shop_name', 'location')
    list_filter = ('location',)
    ordering = ('shop_name',)

# ----------------- BookAvailability -----------------
@admin.register(BookAvailability)
class BookAvailabilityAdmin(admin.ModelAdmin):
    list_display = ('book', 'shop', 'available_copies')  # Display related fields
    search_fields = ('book__title', 'shop__shop_name')   # Search across related models
    list_filter = ('shop',)
    ordering = ('book',)
