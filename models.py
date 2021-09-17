from django.db import models

# Create your models here.
from django.db import models

class data3(models.Model):
    Name = models.CharField(max_length=100)
    filepath = models.FileField(upload_to='', null=True)
    Age = models.IntegerField()
    experience = models.CharField(max_length=50)
    twitter_id= models.CharField(max_length=50)
    Gender = models.CharField(max_length=50)
    Qualification = models.CharField(max_length=100)
    mobile = models.CharField(max_length=100)
    post = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=50)
    invitation=models.CharField(max_length=10000)


    def __str__(self):
        return self.Name

class data6(models.Model):
    CName = models.CharField(max_length=100)
    place = models.CharField(max_length=50)
    regno = models.IntegerField()
    type = models.CharField(max_length=100)
    about = models.CharField(max_length=1000,default="")
    mobile = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=50)

    def __str__(self):
        return self.CName

