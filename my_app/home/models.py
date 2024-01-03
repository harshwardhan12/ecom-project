from django.db import models

# Create your models here.

class Customer(models.Model):
    name=models.CharField(max_length=50)
    email=models.EmailField(unique=True)
    mobile=models.IntegerField()
    password=models.CharField(max_length=500)
    
    def __str__(self):
        return self.name
    
    
class ProductManager(models.Manager):
    def search_products(self, query):
        return self.filter(models.Q(name__icontains=query) | models.Q(description__icontains=query))
    
class Product(models.Model):
    name=models.CharField(max_length=50)
    price=models.DecimalField(max_digits=10, decimal_places=2)
    description=models.CharField(max_length=200)
    image=models.ImageField(upload_to='images/')    
    
    #to get product from database
    @staticmethod
    def get_all_products():
        return Product.objects.all()  #to get all the products

    def __str__(self):
        return self.name    