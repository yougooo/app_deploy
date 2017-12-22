from django.db import models


class Author(models.Model):
    author_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    born_date = models.DateField()
    country = models.CharField(max_length=30, blank=True, null=True)
    update_date = models.DateField()

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)

    class Meta:
        managed = True
        db_table = 'author'
        unique_together = (('first_name', 'last_name', 'born_date'),)


class Book(models.Model):
    book_id = models.AutoField(primary_key=True)
    book_name = models.CharField(max_length=100)
    publication_date = models.DateField()
    description = models.TextField(blank=True, null=True)
    update_date = models.DateField()

    def __str__(self):
        return self.book_name

    class Meta:
        managed = True
        db_table = 'book'
        unique_together = (('book_name', 'publication_date'),)


class Genre(models.Model):
    genre_id = models.AutoField(primary_key=True)
    genre = models.CharField(max_length=30)

    def __str__(self):
        return self.genre

    class Meta:
        managed = True
        db_table = 'genre'


class BookEntry(models.Model):
    library_entry = models.AutoField(primary_key=True)
    author = models.ForeignKey(Author, models.CASCADE)
    book = models.ForeignKey(Book, models.CASCADE)
    genre = models.ForeignKey(Genre, models.CASCADE, blank=True, null=True)
    published = models.BooleanField()

    def __str__(self):
        return str(self.book) + ", " + str(self.author)

    class Meta:
        managed = True
        db_table = 'book_entry'
        unique_together = (('author', 'book'),)

