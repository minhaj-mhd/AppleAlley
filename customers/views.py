from queue import Full
from random import randint
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, render,redirect
from .models import Customer
from orders.models import Order,OrderItem
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .forms import AddressForm
from datetime import datetime, timedelta

# Create your views here.
def Account(request):
    context={}
    if request.POST and "register" in request.POST:
        context["register"] = True
        try:
            username= request.POST.get("username")
            email=request.POST.get("email")
            phone = request.POST.get("phone")
            password= request.POST.get("password")
            user = User.objects.create_user(username=username,
                                        email=email,
                                        password=password)
            user.save()
            customer = Customer.objects.create(name=username,user=user,phone=phone)
            customer.save()
            request.session["email"] = email

            return redirect("verify_email")

        except Exception as e:
            error_message = "Duplicate User or Invalid Credentials"
            messages.error(request,error_message)
        return render(request,"Account/account_layout.html",context)

    elif request.POST and "login" in request.POST:
        context["register"] = False

        try:
            username= request.POST.get("username")
            password= request.POST.get("password")
            user = authenticate(request,username=username,password=password)
            if user:
                login(request,user)
                return redirect("index")
            success_message="login successful"
            return render(request,"Account/account_layout.html",context)

        except Exception as e:
            error_message = "Invalid Credentials"
            messages.error(request,error_message)
            return render(request,"Account/account_layout.html",context)

        

    else:
        return render(request,"Account/account_layout.html")
def Logout(request):
    logout(request)
    return render(request,"Account/account_layout.html")

def verify_registration(request):
    if request.method == "POST":
        fetched_otp = request.POST.get("otp")
        otp = request.session.get("otp")
        if int(fetched_otp) == int(otp):
            storage = messages.get_messages(request)
            storage.used = True  # Mark all messages as used (cleared)
            messages.success(request, "Email verified successfully!")
            email = request.session.get("email")
            user = User.objects.get(email=email)
            if user:
                customer = user.customer
                customer.email_verified=True
                customer.save()
                login(request,user)
                return redirect("index")

        else:
            messages.success(request,"Incorrect otp")
    else:
        email = request.session.get("email")
        otp = send_otp(email)
        request.session["otp"] = otp
        return render(request,"Account/email/verify_registration.html")

def send_otp(email):
    otp = randint(100000, 999999)

    send_mail('AppleAlley - Email Verification',f'Your otp is {otp}','devswebcraft@gmail.com',[email],fail_silently=False)

    return (otp)

def Profile(request):
    if request.user:        
        user = request.user
        customer=user.customer
        orders=Order.objects.filter(owner=customer).order_by('-created_at')
        obj=[]
        for items in orders:
            order = items.cart.all()
            obj.append({"status":items.order_status,"orders":order,"date":items.created_at,"id":items.id})
        return render(request,"Account/Profile_layout.html",{"obj":obj,"customer":customer,"email" : user.email})
    else:
        return redirect("login")

def Address(request,procceed):
    user = request.user

    if user.is_authenticated:
        customer = user.customer

        if request.method=="POST":

            form = AddressForm(request.POST)
            phone = request.POST.get("phone")
            if phone:
                customer.phone = phone
                customer.save()
            if form.is_valid():
                address=form.save()
                address.save()
                customer.address = address
                customer.save()
                if procceed=='true':
                    return redirect("confirmorder")
                else:
                    return redirect("profile")
        if customer.address:
            form = AddressForm(instance=customer.address)
        else:
            form=AddressForm
        return render(request,"Account/edit_address_layout.html",{"form":form,"customer":customer,"email":request.user.email,"procceed":procceed})

def Verify(request):
        if request.method=="POST":
            email=request.POST.get("email")
            try:
                user = User.objects.get(email=email)
                otp = send_otp(email)
                request.session['email_otp'] = otp
                return redirect("verifyotp")
            except:
                messages.error(request,"Email Id doesn't exists.")
                return redirect("verify")



        else:
            return redirect("reset")
def VerifyOtp(request):
        if request.method=="POST":
            otp=request.POST.get("otp")
            sessionOtp=request.session.get("email_otp")
            if otp==str(sessionOtp):
                storage = messages.get_messages(request)
                storage.used = True  # Mark all messages as used (cleared)
                messages.success(request, "Email verified successfully!")
                email = request.session.get("email")
                user = User.objects.get(email=email)
                login(request,user)
                return redirect('index')
            else:
                storage = messages.get_messages(request)
                storage.used = True  # Mark all messages as used (cleared)
                messages.error(request, "Invalid OTP")
                return render(request,"Account/otp_verification_layout.html")
        else:
            storage = messages.get_messages(request)
            storage.used = True  # Mark all messages as used (cleared)
            messages.success(request, "Check your email for OTP")
            return render(request,"Account/otp_verification_layout.html")
def ForgotPassword(request):
        if request.method=="POST":
            email = request.POST.get('email')
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                messages.error(request, "User with this email does not exist.")
                return redirect('reset')
            request.session['email'] = email
            print("email session",request.session.get("email"))
            request.session['otp_expiry'] = (datetime.now() + timedelta(minutes=10)).isoformat()

            otp = randint(100000, 999999)

            send_mail('OTP-foneCom',f'Your otp is {otp}','fonecom@gmail.com',[email],fail_silently=False)
            request.session['email_otp'] = otp

            return redirect("verifyotp")


        else:
            return render(request,"Account/reset_password.html"
)
