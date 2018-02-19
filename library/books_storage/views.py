from django.views.generic.list import ListView
from django.shortcuts import render_to_response
from django.db import connection
from .models import *


def index(request):
    return render_to_response('index.html', {})


class Search(ListView):

    model = BookEntry
    template_name = 'search.html'
    context_object_name = 'books'

    def get_queryset(self):
        q = self.request.GET.get("q", '')
        q = q.strip()
        if len(q) > 2:
            q = "%{}%".format(q)
            with connection.cursor() as cursor:
                cursor.execute("""SELECT * FROM (SELECT (SELECT CONCAT(book_name,', ', date_part('year', publication_date)) AS book_name
                                             FROM book
                                             WHERE book_entry.book_id = book.book_id),
                                             string_agg((SELECT CONCAT(first_name, ' ', last_name)
                                                         FROM author
                                                         WHERE author.author_id = book_entry.author_id), ',') AS full_name
                               FROM book_entry
                               GROUP BY book_entry.book_id)
                          AS result
                          WHERE LOWER(book_name) LIKE LOWER(%s) or
                                LOWER(full_name) LIKE LOWER(%s)""", (q, q,))
                queryset = cursor.fetchall()
            return queryset
        return []

    def get_context_data(self, **kwargs):
        context = super(Search, self).get_context_data(**kwargs)
        context['count'] = len(self.object_list)
        return context
