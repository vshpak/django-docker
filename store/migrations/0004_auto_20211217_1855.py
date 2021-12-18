# Generated by Django 3.2.9 on 2021-12-17 18:55

from django.db import migrations, models
from helpers.write_articles import get_articles_data


def add_to_newmodel(apps, schema_editor):

    user_model = apps.get_model("store", "Author")
    article_model = apps.get_model("store", "Article")
    journal_model = apps.get_model("store", "Journal")
    publisher_model = apps.get_model("store", "Publisher")
    user_data, articles = get_articles_data()
    for category in articles.keys():
        for code in articles[category].keys():

            try:
                publisher = publisher_model.objects.get(name=articles[category][code]['publisher'])
            except publisher_model.DoesNotExist:
                publisher = None

            if publisher is None:
                publisher = publisher_model.objects.create(address=articles[category][code]['address'], name=articles[category][code]['publisher'])

            try:
                journal = journal_model.objects.get(name=articles[category][code]['booktitle'], publisher=publisher.pk)
            except journal_model.DoesNotExist:
                journal = None

            if journal is None:
                journal = journal_model.objects.create(name=articles[category][code]['booktitle'], publisher=publisher)

            created_article = article_model.objects.create(name=articles[category][code]['title'], journal=journal)
            articles[category][code]['model'] = created_article
            articles[category][code]['authors'] = []

    for number, user in user_data.iterrows():
        created_user = user_model.objects.create(
            username=user['username'],
            first_name=user['first_name'],
            last_name=user['last_name']
        )
        article_codes = user['articles'].split(',')
        for code in article_codes:
            category = code.split('-')[0]
            if category in articles.keys() and code in articles[category].keys() and articles[category][code]['model']:
                articles[category][code]['authors'].append(created_user)

    for category in articles.keys():
        for code in articles[category].keys():
            articles[category][code]['model'].authors.set(articles[category][code]['authors'])


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_auto_20211206_1804'),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=200, verbose_name='Логин')),
                ('first_name', models.CharField(max_length=200, verbose_name='Имя пользователя')),
                ('last_name', models.CharField(max_length=200, verbose_name='Фамилия')),
            ],
            options={
                'verbose_name': 'автор',
                'verbose_name_plural': 'авторы',
            },
        ),
        migrations.AddField(
            model_name='article',
            name='authors',
            field=models.ManyToManyField(to='store.Author'),
        ),
        migrations.AddField(
            model_name='book',
            name='authors',
            field=models.ManyToManyField(to='store.Author'),
        ),
        # Добавляем данные после создания модели NewModel
        migrations.RunPython(add_to_newmodel,
                             reverse_code=migrations.RunPython.noop)
    ]
