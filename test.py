from django.db import models
from django.core.exceptions import ValidationError


class Author(models.Model):
    name = models.CharField(max_length=100)
    email= model.EmailField(unique=true)
    created_at= models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.name

    def clean(self):
        if len(self.name.strip() < 3):
            raise ValidationError('Name must be greater than 3 characters')

class Book(models.Model):
    title = models.CharField(max_legnth=100)
    author = models.ForeignKey(Author, on_delete= models.CASCADE, related_name='books')
    published_date = model.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    isbn = models.CharField(max_length=13, unique=True)