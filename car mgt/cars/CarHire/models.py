from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class CarTypes(models.Model):
    Car_model = models.CharField(max_length=50) 

class Parking(models.Model):
    #h_id,h_name,owner ,location,cars
    car_type = models.ForeignKey(CarTypes, on_delete = models.CASCADE)
    name = models.CharField(max_length=30,default="carHire")
    owner = models.CharField(max_length=20)
    location = models.CharField(max_length=50)
    state = models.CharField(max_length=50,default="Kampala")
    country = models.CharField(max_length=50,default="Uganda")
    def __str__(self):
        return self.name


class Cars(models.Model):
    CAR_STATUS = ( 
    ("1", "available"), 
    ("2", "not available"),    
    ) 

    CAR_TYPE = ( 
     ("1", "Toyota Harrier"), 
     ("2", "Toyota Surf"),
     ("3","Subaru Forester"),
     ("4","Subaru Outback"),
     ("5","Subaru Cross"),
     ("6","Subaru Impreza"),
     ("7","Nissan X-Trail"),
     ("8","Mazda CX-5"),
     ("9","Toyota RAV4"),
     ("10","Mitsubishi Pajero"),
     ("11","Mitsubishi Montero"),
     ("12","Mitsubishi Montero Sport"),
     ("13","Toyota Land Cruiser Prado"),
     ("14","Toyota Fortuner"),
     ("15","Nissan Patro"),
     ("16","Toyota RAV4 Avensis"),
     ("17","Toyota Highlander"),
     ("18","Nissan Altima"),
     ("19","Nissan Rogue"),
     ("20","Honda Civic"),
     ("21","Honda CR-V"),
     ("22","Ford Fusion"),
     ("23","Ford Mustang"),
     ("24","Ford Explorer"),
     ("25","Ford Focus"),
     ("26","Ford Fiesta"),
     ("27","Ford Edge"),
     ("28","Ford C-Max Hybrid"),
     ("29","Ford Mustang GT"),
     ("30","Ford Escape"),
     
     ) 



    #type,no_of_cars,capacity,prices,Parking
    car_type = models.CharField(max_length=50,choices = CAR_TYPE)
    capacity = models.IntegerField()
    price = models.IntegerField()
    size = models.IntegerField()
    parking = models.ForeignKey(Parking, on_delete = models.CASCADE)
    status = models.CharField(choices =CAR_STATUS,max_length = 15)
    carnumber = models.IntegerField()
    def __str__(self):
        return f"{self.parking.name}{self.carnumber}"

class Reservation(models.Model):

    check_in = models.DateField(auto_now =False)
    check_out = models.DateField()
    car = models.ForeignKey(Cars, on_delete = models.CASCADE)
    customer = models.ForeignKey(User, on_delete= models.CASCADE)
    
    booking_id = models.CharField(max_length=100,default="null")
    def __str__(self):
        return self.guest.username
    
  
    

