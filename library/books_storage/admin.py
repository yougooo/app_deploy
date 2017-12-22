from django.contrib import admin
from .models import *


class AuthorManager(admin.ModelAdmin):
    list_display = ['author_id','first_name','last_name','born_date',
                    'country', 'update_date']


class BookManager(admin.ModelAdmin):
    list_display = ['book_id','book_name','publication_date',
                    'description', 'update_date']


class GenreManager(admin.ModelAdmin):
    list_display = ['genre_id','genre']


class BookEntryManager(admin.ModelAdmin):
    list_display = ['library_entry', 'author', 'book', 'genre', 'published']


admin.site.register(Author, AuthorManager)
admin.site.register(Book, BookManager)
admin.site.register(Genre, GenreManager)
admin.site.register(BookEntry, BookEntryManager)

