import psycopg2
import pandas as pd
from datetime import date

connection_row = "dbname=library user=user password=password"


books = pd.read_csv('book_data_final_1.csv', header=None,
                    names=['book_name','date','first_name', 'last_name'])

authors = pd.read_csv('author_data_final_1.csv', header=None,
                      names=['first_name', 'last_name','year'])


def many_maker(data, cursor):
    author_dict = {}
    for key_1, key_2, val in data:
        name = select_author_id(cursor, ' '.join([key_1, key_2]))
        if name in author_dict.keys():
            author_dict[name].append(select_book_id(cursor, val))
        else:
            author_dict[name] = [select_book_id(cursor, val)]
    return author_dict


def select_author_id(cursor, author):
    first_name, last_name = author.split()
    cursor.execute("SELECT author_id FROM author " +
                   "WHERE first_name=%s AND last_name=%s",
                   (first_name,last_name))
    return list(cursor)[0][0]


def select_book_id(cursor, book_name):
    cursor.execute("SELECT book_id FROM book " +
                   "WHERE book_name=%s", (book_name,))
    return list(cursor)[0][0]


with psycopg2.connect(connection_row) as connect:
        with connect.cursor() as cursor:
            authors_insert = set(zip(authors['first_name'], authors['last_name'],
                                 authors['year']))
            for first_name, last_name, year in authors_insert:
                print(first_name, last_name, year)
                cursor.execute("INSERT INTO author (first_name, last_name, "+
                               "born_date) VALUES (%s,%s,%s)",
                               (first_name,last_name,date(year,1,1)))

            print('authors data ... OK')

            books_insert = set(zip(books['book_name'],books['date']))
            for book_name, dat in books_insert:
                print(book_name, date, ' OK...')
                cursor.execute("INSERT INTO book (book_name, publication_date)" +
                               "VALUES (%s,%s)", (book_name, date(dat,1,1),))

            print('books data ... OK')

            ######## n:m insert ########
            many_insert = set(zip(books['first_name'], books['last_name'],
                                  books['book_name']))
            relation = many_maker(many_insert, cursor)

            for author_id, books_id in list(relation.items()):
                for book_id in books_id:
                    print(author_id, book_id)
                    cursor.execute("INSERT INTO book_entry (author_id, book_id)"+
                                   "VALUES (%s,%s)", (author_id, book_id))

            connect.commit()


