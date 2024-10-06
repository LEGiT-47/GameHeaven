from django.db import models
from django.contrib.auth.models import User

class Contact(models.Model):
    name=models.CharField(max_length=122)
    rating = models.FloatField(default=0.0)
    email=models.CharField(max_length=122)
    phone=models.CharField(max_length=12)
    desc=models.TextField()
    date=models.DateField()

    def __str__(self):
        return self.name + " "+self.phone    


class Cart(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    # image = models.ImageField(upload_to='gift_items')
    
    def __str__(self):
        return self.name

