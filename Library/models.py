from django.db import models


class Reader(models.Model):
    ID = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=16, unique=True)
    phone = models.IntegerField()
    max_borrowing = models.IntegerField(default=5)
    balance = models.FloatField(default=0.0)

    STATUS_CHOICES = (
        (0, 'normal'),
        (-1, 'overdue')
    )
    status = models.IntegerField(
        choices=STATUS_CHOICES,
        default=-1,
    )

    def __str__(self):
        return self.username

    def __unicode__(self):
        return unicode(self.__str__())


class BookInfo(models.Model):
    ISBN = models.CharField(max_length=13, primary_key=True)

    description = models.CharField(max_length=1024)
    price = models.FloatField()

    category = models.CharField(max_length=64)
    cover = models.ImageField()
    index = models.CharField(max_length=16)
    location = models.CharField(max_length=64)
    quantity = models.IntegerField(default=1)


class Book(models.Model):
    ISBN = models.CharField(max_length=13, primary_key=True)
    title = models.CharField(max_length=128)
    author = models.CharField(max_length=32)
    press = models.CharField(max_length=64)

    info = models.OneToOneField(BookInfo)


class Borrowing(models.Model):
    reader_id = models.ForeignKey(Reader)
    ISBN = models.ForeignKey(Book)
    date_issued = models.DateField()
    date_due_to_returned = models.DateField()
    date_returned = models.DateField()
    amount_of_fine = models.FloatField(default=0.0)
