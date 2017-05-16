from django.contrib import admin

# Register your models here.

from library.models import Book, Borrowing, Reader

admin.site.register(Book)
admin.site.register(Borrowing)
admin.site.register(Reader)
