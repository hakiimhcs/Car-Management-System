from django.shortcuts import render ,redirect
from django.http import HttpResponse , HttpResponseRedirect
from .models import Parking,Cars,Reservation
from django.contrib import messages
from django.contrib.auth import *
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import datetime
# Create your views here.

#homepage
def homepage(request):
    all_location = Parking.objects.values_list('location','id').distinct().order_by()
    if request.method =="POST":
        try:
            print(request.POST)
            parking = Parking.objects.all().get(id=int(request.POST['search_location']))
            rr = []
            
            #for finding the reserved cars on this time period for excluding from the query set
            for each_reservation in Reservation.objects.all():
                if str(each_reservation.check_in) < str(request.POST['cin']) and str(each_reservation.check_out) < str(request.POST['cout']):
                    pass
                elif str(each_reservation.check_in) > str(request.POST['cin']) and str(each_reservation.check_out) > str(request.POST['cout']):
                    pass
                else:
                    rr.append(each_reservation.car.id)
                
            car = Cars.objects.all().filter(parking=parking,capacity__exact = int(request.POST['capacity'])).exclude(id__in=rr)
            if len(car) == 0:
                messages.warning(request,"Sorry No Cars Are Available on this time period")
            data = {'cars':car,'all_location':all_location,'flag':True}
            response = render(request,'index.html',data)
        except Exception as e:
            messages.error(request,e)
            response = render(request,'index.html',{'all_location':all_location})


    else:
        
        
        data = {'all_location':all_location}
        response = render(request,'index.html',data)
    return HttpResponse(response)

#about
def aboutpage(request):
    return HttpResponse(render(request,'about.html'))

def newview(request):
    return HttpResponse(render(request,'new.html'))

#contact page
def contactpage(request):
    return HttpResponse(render(request,'contact.html'))

#user sign up
def user_sign_up(request):
    if request.method =="POST":
        user_name = request.POST['username']
        
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            messages.warning(request,"Password didn't matched")
            return redirect('userloginpage')
        
        try:
            if User.objects.all().get(username=user_name):
                messages.warning(request,"Username Not Available")
                return redirect('userloginpage')
        except:
            pass
            

        new_user = User.objects.create_user(username=user_name,password=password1)
        new_user.is_superuser=False
        new_user.is_staff=False
        new_user.save()
        messages.success(request,"Registration Successfull")
        return redirect("userloginpage")
    return HttpResponse('Access Denied')
#staff sign up
def staff_sign_up(request):
    if request.method =="POST":
        user_name = request.POST['username']
        
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            messages.success(request,"Password didn't Matched")
            return redirect('staffloginpage')
        try:
            if User.objects.all().get(username=user_name):
                messages.warning(request,"Username Already Exist")
                return redirect("staffloginpage")
        except:
            pass
        
        new_user = User.objects.create_user(username=user_name,password=password1)
        new_user.is_superuser=False
        new_user.is_staff=True
        new_user.save()
        messages.success(request," Staff Registration Successfull")
        return redirect("staffloginpage")
    else:

        return HttpResponse('Access Denied')
#user login and signup page
def user_log_sign_page(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['pswd']

        user = authenticate(username=email,password=password)
        try:
            if user.is_staff:
                
                messages.error(request,"Incorrect username or Password")
                return redirect('staffloginpage')
        except:
            pass
        
        if user is not None:
            login(request,user)
            messages.success(request,"successful logged in")
            print("Login successfull")
            return redirect('homepage')
        else:
            messages.warning(request,"Incorrect username or password")
            return redirect('userloginpage')

    response = render(request,'user/userlogsign.html')
    return HttpResponse(response)

#logout for admin and user 
def log(request):    
    logout(request)
    return redirect('homepage')


# Paymeny 



#  Change Password 
@login_required(login_url='/home')
def change_password(request):    

    context = {}

    if request.method=="POST":
        current = request.POST["cpwd"]
        newpass = request.POST["npwd"]

        user = User.objects.get(id=request.user.id)
        check = user.check_password(current)

        un = user.username
        
        # password = newpass

        # print(check)
        if check == True:
            user.set_password(newpass)
            user.save()

            context["msz"] = "Password Changed Successfully  !!"
            context["col"] = "alert-success"

            # login after saving password 
            user = User.objects.get(username=un)
            # user = authenticate(username=,password=newpass)
            login(request,user)
            
        else:
            context["msz"] = "Incorrecr Current Password"
            context["col"] = "alert-danger"
            
    return render(request, 'passwordchange.html', context)



#staff login and signup page
def staff_log_sign_page(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username,password=password)
        
        if user.is_staff:
            login(request,user)
            return redirect('staffpanel')
        
        else:
            messages.success(request,"Incorrect username or password")
            return redirect('staffloginpage')
    response = render(request,'staff/stafflogsign.html')
    return HttpResponse(response)

#staff panel page
@login_required(login_url='/staff')
def panel(request):
    
    if request.user.is_staff == False:
        return HttpResponse('Access Denied')
    
    cars = Cars.objects.all()
    total_cars = len(cars)
    available_cars = len(Cars.objects.all().filter(status='1'))
    unavailable_cars = len(Cars.objects.all().filter(status='2'))
    reserved = len(Reservation.objects.all())

    parking = Parking.objects.values_list('location','id').distinct().order_by()

    response = render(request,'staff/panel.html',{'location':parking,'reserved':reserved,'cars':cars,'total_cars':total_cars,'available':available_cars,'unavailable':unavailable_cars})
    return HttpResponse(response)

#for editing car information
@login_required(login_url='/staff')
def edit_car(request):
    if request.user.is_staff == False:   
        return HttpResponse('Access Denied')
    if request.method == 'POST' and request.user.is_staff:
        print(request.POST)
        old_car = Cars.objects.all().get(id= int(request.POST['carid']))
        parking = Parking.objects.all().get(id=int(request.POST['parking']))
        old_car.car_type  = request.POST['cartype']
        old_car.capacity   =int(request.POST['capacity'])
        old_car.price      = int(request.POST['price'])
        old_car.size       = int(request.POST['size'])
        old_car.parking      = parking
        old_car.status     = request.POST['status']
        old_car.car_number=int(request.POST['carnumber'])

        old_car.save()
        messages.success(request,"Car Details Updated Successfully")
        return redirect('staffpanel')
    else:
    
        car_id = request.GET['carid']
        car = Cars.objects.all().get(id=car_id)
        response = render(request,'staff/editcar.html',{'car':car})
        return HttpResponse(response)

#for adding car
@login_required(login_url='/staff')
def add_new_car(request):
    if request.user.is_staff == False:
        return HttpResponse('Access Denied')
    if request.method == "POST":
        total_cars = len(Cars.objects.all())
        new_car = Cars()
        parking = Parking.objects.all().get(id = int(request.POST['parking']))
        print(f"id={parking.id}")
        print(f"name={parking.name}")


        new_car.carnumber = total_cars + 1
        new_car.car_type  = request.POST['cartype']
        new_car.capacity   = int(request.POST['capacity'])
        new_car.size       = int(request.POST['size'])
        new_car.capacity   = int(request.POST['capacity'])
        new_car.parking      = parking
        new_car.status     = request.POST['status']
        new_car.price      = request.POST['price']

        new_car.save()
        messages.success(request,"New Car Added Successfully")
    
    return redirect('staffpanel')

#booking car page
@login_required(login_url='/user')
def book_car_page(request):
    car = Cars.objects.all().get(id=int(request.GET['carid']))
    return HttpResponse(render(request,'user/bookcar.html',{'car':car}))

#For booking the car
@login_required(login_url='/user')
def book_car(request):
    
    if request.method =="POST":

        car_id = request.POST['car_id']
        
        car = Cars.objects.all().get(id=car_id)
        #for finding the reserved cars on this time period for excluding from the query set
        for each_reservation in Reservation.objects.all().filter(car = car):
            if str(each_reservation.check_in) < str(request.POST['check_in']) and str(each_reservation.check_out) < str(request.POST['check_out']):
                pass
            elif str(each_reservation.check_in) > str(request.POST['check_in']) and str(each_reservation.check_out) > str(request.POST['check_out']):
                pass
            else:
                messages.warning(request,"Sorry This Car is unavailable for Booking")
                return redirect("homepage")
            
        current_user = request.user
        total_person = int( request.POST['person'])
        booking_id = str(car_id) + str(datetime.datetime.now())

        reservation = Reservation()
        car_object = Cars.objects.all().get(id=car_id)
        car_object.status = '2'
        
        user_object = User.objects.all().get(username=current_user)

        reservation.customer = user_object
        reservation.car = car_object
        person = total_person
        reservation.check_in = request.POST['check_in']
        reservation.check_out = request.POST['check_out']

        reservation.save()

        messages.success(request,"Congratulations! Booking Successfull -please contact us on 0756368003 to confirm your order")

        return redirect("homepage")
    else:
        return HttpResponse('Access Denied')

def handler404(request):
    return render(request, '404.html', status=404)

@login_required(login_url='/staff')   
def view_car(request):
    car_id = request.GET['carid']
    car = Cars.objects.all().get(id=car_id)

    reservation = Reservation.objects.all().filter(car=car)
    return HttpResponse(render(request,'staff/viewcar.html',{'car':car,'reservations':reservation}))

@login_required(login_url='/user')
def user_bookings(request):
    if request.user.is_authenticated == False:
        return redirect('userloginpage')
    user = User.objects.all().get(id=request.user.id)
    print(f"request user id ={request.user.id}")
    bookings = Reservation.objects.all().filter(customer=user)
    totalamount = 0.0

    for b in bookings:
        totalamount += b.car.price * (b.check_out - b.check_in).days
        
    if not bookings:
        messages.warning(request,"No Bookings Found")
    return HttpResponse(render(request,'user/mybookings.html',{'bookings':bookings,'totalamount':totalamount}))


@login_required(login_url='/staff')
def add_new_location(request):
    if request.method == "POST" and request.user.is_staff:
        hname = request.POST['new_parking']
        owner = request.POST['new_owner']
        location = request.POST['new_city']
        state = request.POST['new_state']
        country = request.POST['new_country']
        
        parking = Parking.objects.all().filter(location = location , state = state)
        if parking:
            messages.warning(request,"Sorry City at this Location already exist")
            return redirect("staffpanel")
        else:
            new_parking = Parking()
            new_parking.name = hname
            new_parking.owner = owner
            new_parking.location = location
            new_parking.state = state
            new_parking.country = country
            new_parking.save()
            messages.success(request,"New Location Has been Added Successfully")
            return redirect("staffpanel")

    else:
        return HttpResponse("Not Allowed")
    
#for showing all bookings to staff
@login_required(login_url='/staff')
def all_bookings(request):
   
    bookings = Reservation.objects.all()
    if not bookings:
        messages.warning(request,"No Bookings Found")
    return HttpResponse(render(request,'staff/allbookings.html',{'bookings':bookings}))
    


        