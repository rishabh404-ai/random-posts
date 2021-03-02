from django.db import models
from authentication.models import User

# Create your models here.

class RandomPosts(models.Model):
    user_id = models.ForeignKey(to=User,on_delete=models.DO_NOTHING)
    title   = models.CharField(max_length=500, null=False, blank=False)
    body    = models.TextField(null=False,blank=False)