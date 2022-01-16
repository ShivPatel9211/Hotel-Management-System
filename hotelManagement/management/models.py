from pyexpat import model
from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserProfile(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    phone=models.IntegerField()
    address=models.CharField(max_length=200 ,null=True)

    def __str__(self):
        return self.user.username

class Room(models.Model):
    class Type(models.TextChoices):

        AC="AC"
        Non_AC="Non AC"
    room_type=models.CharField(max_length=10,choices=Type.choices)
    room_no=models.IntegerField(unique=True) 
    room_rate=models.IntegerField()
    no_of_bed=models.IntegerField(null=True)
    image=models.ImageField(upload_to='room_pic',blank=True)
    def __str__(self):
        return str(self.room_no)

class Reservations(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    room=models.ForeignKey(Room,on_delete=models.CASCADE)
    booking_date=models.DateField(auto_now_add=True)
    check_in_date=models.DateField()
    check_out_date=models.DateField()
    no_of_people=models.IntegerField()
    def __str__(self):
        return str(self.room.room_no)

