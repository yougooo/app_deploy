# Generated by Django 2.0 on 2017-12-10 22:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Authors',
            fields=[
                ('author_id', models.AutoField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=25)),
                ('last_name', models.CharField(max_length=25)),
                ('born_date', models.DateField()),
                ('country', models.CharField(blank=True, max_length=30, null=True)),
            ],
            options={
                'db_table': 'authors',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Books',
            fields=[
                ('book_id', models.AutoField(primary_key=True, serialize=False)),
                ('book_name', models.CharField(max_length=100)),
                ('publication_date', models.DateField()),
                ('description', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'books',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('genre_id', models.AutoField(primary_key=True, serialize=False)),
                ('genre', models.CharField(max_length=30)),
            ],
            options={
                'db_table': 'genre',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Library',
            fields=[
                ('library_entry', models.AutoField(primary_key=True, serialize=False)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='books_storage.Authors')),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='books_storage.Books')),
                ('genre', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='books_storage.Genre')),
            ],
            options={
                'db_table': 'library',
                'managed': True,
            },
        ),
        migrations.AlterUniqueTogether(
            name='books',
            unique_together={('book_name', 'publication_date')},
        ),
        migrations.AlterUniqueTogether(
            name='authors',
            unique_together={('first_name', 'last_name', 'born_date')},
        ),
        migrations.AlterUniqueTogether(
            name='library',
            unique_together={('author', 'book')},
        ),
    ]
