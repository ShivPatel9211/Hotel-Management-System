from django.shortcuts import render,render,redirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from .models import UserProfile,Room,Reservations
from django.contrib.auth import authenticate,logout,login
import datetime
from datetime import timedelta
# Create your views here.
def index(request):
    room=Room.objects.all()
    context={
        "room":room
    }
    return render(request,'index.html',context)

def user_signup(request):
    if request.method=="POST":
        username=request.POST['username']
        email=request.POST['email']
        firstname=request.POST['firstname']
        lastname=request.POST['lastname']
        password=request.POST['password']
        phone=request.POST['phone']
        address=request.POST['address']
        try:
            if User.objects.filter(username=username).first():
                messages.error(request,"User with this user name already exist")
                return redirect('user_signup')
            else:
                user= User(username=username,email=email,first_name=firstname,last_name=lastname)
                user.set_password(password)
                user.save()
                profile=UserProfile.objects.create(user=user,address=address,phone=phone)
                profile.save()
                messages.success(request, "Account created successfully")
                return redirect('user_login')
        except Exception as e:
            messages.error(request, e)
            return redirect('user_signup')

    return render(request,'user_signup.html')

def user_login(request):
    if request.method =="POST":
        username=request.POST['username']
        password=request.POST['password']
        try:
            user=authenticate(username=username,password=password)
            if user is None:
                messages.error(request,"Username or password is wrong, Please try again")
                return redirect('user_login')
            else:
                login(request, user)
                return redirect('index')
        except Exception as e:
            messages.error(request,e)
    return render(request,'user_signup.html')

def user_logout(request):
    logout(request)
    return redirect("index")

def user_profile(request):
    user=User.objects.filter(username=request.user).first()
    profile=UserProfile.objects.filter(user=user).first()
    if request.method=="POST":
        email=request.POST['email']
        firstname=request.POST['firstname']
        lastname=request.POST['lastname']
        phone=request.POST['phone']
        address=request.POST['address']
        try:
            user.first_name=firstname
            user.last_name=lastname
            user.email=email
            profile.address=address
            profile.phone=phone
            user.save()
            profile.save()
            messages.success(request,"User Profile Update successfully")
        except Exception as e:
            messages.error(request,e)

    context={
        "user":user,
        "profile":profile
    }
    return render(request,'user_profile.html',context)

def add_room(request):
    if request.user.is_superuser:
        if request.method =="POST":
            room_no=request.POST['room_no']
            no_of_bed=request.POST['no_of_bed']
            room_type=request.POST['room_type']
            room_rate=request.POST['room_rate']
            image=request.FILES['image']
            try:
                room=Room(room_no=room_no,no_of_bed=no_of_bed,room_type=room_type,room_rate=room_rate,image=image)
                room.save()
                messages.success(request,"New room is successfully added")
                return redirect('index')
            except Exception as e:
                messages.error(request,e)
                return redirect('add_room')
        return render(request, 'add_room.html')
def book_room(request,id):
    if request.user.is_authenticated:
        room=Room.objects.filter(id=id).first()
        x=datetime.datetime.now()
        x2=x+ timedelta(days=40)
        min_date=x.strftime("%Y"+"-"+"%m"+"-"+"%d")
        last_date=x2.strftime("%Y"+"-"+"%m"+"-"+"%d")
        if request.method=="POST":
            check_in_date=request.POST['check_in_date']
            check_out_date=request.POST['check_out_date']
            no_of_people=request.POST['no_of_people']
            res=Reservations.objects.filter(room=room).filter(check_in_date=check_in_date)
            if len(res)>0:
                messages.error(request, "Sorry, This room is already booked on the selected day")
                return redirect(f'/book_room/{room.id}')
            else:
                try:
                    reservation=Reservations(user=request.user,room=room,check_in_date=check_in_date,no_of_people=no_of_people,check_out_date=check_out_date)
                    reservation.save()
                    messages.success(request,"Your room booked successfully")
                except Exception as e:
                    messages.error(request,e)
                    return redirect(f'/book_room/{room.id}')
        context={
            "room":room,
            "min_date":min_date,
            "last_date":last_date
        }
        return render(request,'book_room.html',context)
    return redirect('user_login')


def user_booking(request,id):
    reservation=Reservations.objects.filter(user=id)
    context={
        "reservation":reservation
    }
    return render(request, 'user_booking.html',context)

def cancel_reservation(request,id):
    if request.user.is_authenticated:
        reservation=Reservations.objects.filter(id=id)
        userid=request.user.id
        try:
            reservation.delete()
            messages.error(request,"Your reservation is successfully canceled")
            return redirect(f'/user_booking/{userid}')
        except Exception as e:
            messages.error(request, e)
            return redirect(f'/user_booking/{userid}')

def delete_room(request,id):
    if request.user.is_superuser:
        room=Room.objects.filter(id=id)
        try:
            room.delete()
            messages.success(request,"Selected room is successfuly removed")
            return redirect('index')
        except Exception as e:
            messages.error(request,e)
            return redirect('index')
        
def update_room(request,id):
    if request.user.is_superuser:
        room = Room.objects.filter(id=id).first()
        if request.method=="POST":
            room_rate=request.POST['room_rate']
            try:
                room.room_rate=room_rate
                room.save()
                messages.success(request,"Room's rate updated successfully")
                return redirect('index')
            except Exception as e:
                messages.error(request,e)
                return redirect("update_room")
        context={
                "room":room
            }
        return render(request,'update_room.html',context)
    return redirect('user_login')


def view_user(request):
    if request.user.is_superuser:
        profile=UserProfile.objects.all()
        context={
            "profile":profile
        }
        return render(request,'view_user.html',context)
def view_reservation(request):
    reservation=Reservations.objects.all().order_by("booking_date")
    context={
        "reservation":reservation
    }
    return render(request,'view_reservation.html',context)

def manager_cancel_reservation(request,id):
    if request.user.is_superuser:
        reservation=Reservations.objects.filter(id=id)
        try:
            reservation.delete()
            messages.error(request,"Reservation is successfully canceled")
            return redirect("view_reservation")
        except Exception as e:
            messages.error(request, e)
            return redirect("view_reservation")

def delete_user(request,id):
    if request.user.is_superuser:
        user=User.objects.filter(id=id)
        try:
            user.delete()
            messages.success(request,"User deleted")
            return redirect("view_user")
        except Exception as e:
            messages.error(request,e)
            return redirect("view_user")
