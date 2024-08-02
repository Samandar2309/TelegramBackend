from django.db import models


# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=212)
    author = models.CharField(max_length=212)
    description = models.TextField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.title
