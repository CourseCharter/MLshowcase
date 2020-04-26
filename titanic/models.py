from django.db import models

# Create your models here.
class titanic_guess(models.Model):

    class Gender(models.IntegerChoices):
        FEMALE = 0
        MALE = 1
    class Pclass(models.IntegerChoices):
        FIRST = 1
        SECOND = 2
        THIRD = 3


    passengerclass=models.IntegerField(choices=Pclass.choices)
    sex=models.IntegerField(choices=Gender.choices)
    age=models.IntegerField(default=0)
    relativesonboard=models.IntegerField(default=0)
    ticketprice=models.FloatField(default=0)

    def __str__(self):
        return super().__str__()