from advisornet.settings import DATABASES
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100, unique= True)
    password = models.CharField(max_length=15)
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

class Advisor(models.Model):
    name = models.CharField(max_length = 100, default='adminTest')
    emp_id = models.AutoField(primary_key=True)
    picture_url = models.URLField(max_length=255)

    def __str__(self):
        return self.name


class Booking(models.Model):
    # advName = models.CharField(max_length=100)
    # advPic = models.URLField(max_length=255)
    bookingId = models.AutoField(primary_key=True)
    userId = models.IntegerField()
    advId = models.IntegerField()
    bookingDateTime = models.DateTimeField()

class BookingView(models.Model):
    advisorName = models.CharField(max_length=100, default='adminTest')
    advisorProfilePic = models.URLField(max_length=255)
    advisorId = models.IntegerField()
    bookingTime = models.TimeField()
    bookingId = models.IntegerField()






# test DATA
# {
#     "name":"kanishk sharma",
#     "picture_url" : "https://static.coindesk.com/wp-content/uploads/2021/04/dogecoin-345x222.jpg"
# }