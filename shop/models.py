from django.db import models
import datetime
import os
from django.contrib.auth.models import User


def getfilename(request, filename):
    now_time = datetime.datetime.now().strftime("%y%m%d%H%M%S")  # removed slashes from date
    new_filename = "%s_%s" % (now_time, filename)
    return os.path.join('uploads/', new_filename)

class Catagory(models.Model):
    name = models.CharField(max_length=150, null=False, blank=False)
    image = models.ImageField(upload_to=getfilename, null=False, blank=False)
    description = models.TextField(max_length=500, null=False, blank=False)
    status = models.BooleanField(default=False, help_text='0-show,1-hidden')
    trending = models.BooleanField(default=False, help_text='0-default,1-trending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    catagory = models.ForeignKey(Catagory, on_delete=models.CASCADE)  # lowercase field name
    name = models.CharField(max_length=150, null=False, blank=False)
    vendor = models.CharField(max_length=150, null=False, blank=False)
    product_image = models.ImageField(upload_to=getfilename, null=False, blank=False)
    quantity = models.IntegerField(null=False, blank=False)
    original_price = models.IntegerField(null=False, blank=True)
    selling_price = models.IntegerField(null=False, blank=True)
    description = models.TextField(max_length=500, null=False, blank=False)
    status = models.BooleanField(default=False, help_text='0-show,1-hidden')
    trending = models.BooleanField(default=False, help_text='0-default,1-trending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Cart(models.Model):   # Class name should start with Capital letter
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_qty = models.IntegerField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
class Favourite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)   
    created_at = models.DateTimeField(auto_now_add=True)