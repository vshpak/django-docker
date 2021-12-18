from django.db import models


class Publisher(models.Model):
    class Meta:
        verbose_name = "издательство"
        verbose_name_plural = "издательства"

    name = models.CharField("Название", max_length=200)
    address = models.CharField("Адрес", max_length=200)

    def __str__(self):
        return f"{self.name}"


class Author(models.Model):
    class Meta:
        verbose_name = "автор"
        verbose_name_plural = "авторы"

    username = models.CharField("Логин", max_length=200)
    first_name = models.CharField("Имя пользователя", max_length=200)
    last_name = models.CharField("Фамилия", max_length=200)

    def __str__(self):
        return f"{self.username}"


# class PublicationType(models.Model):
#     name = models.CharField(max_length=200)


class Journal(models.Model):
    class Meta:
        verbose_name = "журнал"
        verbose_name_plural = "журналы"

    name = models.CharField("Название", max_length=200)
    publisher = models.ForeignKey(
        Publisher, on_delete=models.CASCADE, verbose_name="Издательство"
    )

    def __str__(self):
        return f"{self.name}"


class Article(models.Model):
    class Meta:
        verbose_name = "статья"
        verbose_name_plural = "статьи"

    name = models.CharField("Название", max_length=200)
    journal = models.ForeignKey(
        Journal, on_delete=models.CASCADE, verbose_name="Журнал"
    )
    authors = models.ManyToManyField(Author, null=True)

    def __str__(self):
        return f"{self.name}"


class Book(models.Model):
    class Meta:
        verbose_name = "книга"
        verbose_name_plural = "книги"

    name = models.CharField("Название", max_length=200)
    publisher = models.ForeignKey(
        Publisher, on_delete=models.CASCADE, verbose_name="Издательство"
    )
    authors = models.ManyToManyField(Author, null=True)

    def __str__(self):
        return f"{self.name}"
