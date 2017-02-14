from django.contrib import admin

# Register your models here.

from models import Book, BookInfo, Borrowing, Reader

admin.site.register(Book)
admin.site.register(BookInfo)
admin.site.register(Borrowing)
admin.site.register(Reader)
