from django.db import models
from django.contrib.auth.models import user

# Create your models here.
class Nodes(models.Model):
  user= models.ForeignKey(user,on_delete=models.CASCADE)