
# python 3

import psycopg2


connection_row = "dbname=library user=alex password=95qaz26plm"


with psycopg2.connect(connection_row) as connect:
    with connect.cursor() as cursor:
        cursor.execute("DROP TABLE IF EXISTS book_entry")
        cursor.execute("DROP TABLE IF EXISTS author")
        cursor.execute("DROP TABLE IF EXISTS genre")
        cursor.execute("DROP TABLE IF EXISTS book")

        # Create authors table for e-library app
        cursor.execute("CREATE TABLE author(" +
                       "author_id SERIAL PRIMARY KEY," +
                       "first_name VARCHAR(25) NOT NULL," +
                       "last_name VARCHAR(25) NOT NULL," +
                       "born_date DATE NOT NULL," +
                       "country VARCHAR(30)," +
                       "update_date DATE NOT NULL default CURRENT_DATE,"+
                       "UNIQUE(first_name, last_name, born_date))")

        print('Table author... OK')

        cursor.execute("CREATE TABLE genre(" +
                        "genre_id SERIAL PRIMARY KEY," +
                        "genre VARCHAR(30) NOT NULL)")

        print('Table genre... OK')

        cursor.execute("CREATE TABLE book(" +
                       "book_id SERIAL PRIMARY KEY," +
                       "book_name VARCHAR(256) NOT NULL," +
                       "publication_date DATE NOT NULL," +
                       "description TEXT," +
                       "update_date DATE NOT NULL default CURRENT_DATE,"+
                       "UNIQUE(book_name, publication_date))")

        print('Table book... OK')

        cursor.execute("CREATE TABLE book_entry(" +
                       "library_entry SERIAL," +
                       "author_id int4 REFERENCES author (author_id) " +
                       "ON UPDATE CASCADE ON DELETE CASCADE," +
                       "book_id int4 REFERENCES book (book_id) " +
                       "ON UPDATE CASCADE ON DELETE CASCADE," +
                       "genre_id int4 REFERENCES genre (genre_id) " +
                       "ON UPDATE CASCADE ON DELETE CASCADE," +
                       "CONSTRAINT list_id PRIMARY KEY (author_id, book_id),"+
                       "published BOOLEAN NOT NULL default FALSE)")

        print('Table book_entry... OK')

        connect.commit()
        cursor.close()

    print('All changes were successfully saved.')

