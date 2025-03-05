from queue import Full
from random import randint
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, render,redirect
from customers.models import Customer
from orders.models import Order,OrderItem
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from customers.forms import AddressForm, CustomerForm
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
            # Validate phone number
            if not phone.isdigit() or len(phone) != 10:
                raise ValueError("Invalid phone number")
            password= request.POST.get("password")
            user = User.objects.create_user(username=username,
                                        email=email,
                                        password=password)
            user.save()
            customer = Customer.objects.create(name=username,user=user,phone=phone)
            customer.save()
            request.session["email"] = email

            return redirect("verify_email")

        except ValueError as e:
            messages.error(request, str(e))
            return render(request, "Account/account_layout.html", context)
        except Exception as e:
            error_message = "Duplicate User or Invalid Credentials"
            messages.error(request, error_message)
        return render(request, "Account/account_layout.html", context)

    elif request.POST and "login" in request.POST:
        context["register"] = False

        try:
            email= request.POST.get("email")
            password= request.POST.get("password")
            user = authenticate(request,email=email,password=password)
            print(user)
            if user:
                login(request,user)
                success_message="login successful"
                messages.success(request,success_message)
                return redirect("index")
            else:
                raise Exception
        

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
        customer = user.customer
        orders = Order.objects.filter(owner=customer).order_by('-created_at')
        obj = []
        for items in orders:
            order = items.cart.all()
            obj.append({"status": items.order_status, "orders": order, "date": items.created_at, "id": items.id})
        return render(request, "Account/Profile_layout.html", {"obj": obj, "customer": customer, "email": user.email})
    else:
        return redirect("login")

def Address(request, procceed):
    user = request.user

    if user.is_authenticated:
        customer = user.customer
        address_form = None  # Default to None if no address exists

        if request.method == "POST":
            customer_form = CustomerForm(request.POST, instance=customer)

            #  Check if customer has an address
            if customer.address:
                address_form = AddressForm(request.POST, instance=customer.address)
            else:
                address_form = AddressForm(request.POST)  # New address if needed

            if customer_form.is_valid() and (not address_form or address_form.is_valid()):
                customer_form.save()

                #  Save address only if form exists and is valid
                if address_form:
                    address = address_form.save(commit=False)  # Don't save yet
                    if not customer.address:
                        customer.address = address  # Link address to customer
                    address.save()
                    customer.save()  # Save customer with updated address

                return redirect("confirmorder" if procceed == 'true' else "profile")

        else:
            customer_form = CustomerForm(instance=customer)
            if customer.address:
                address_form = AddressForm(instance=customer.address)
            else:
                address_form = AddressForm()  # Empty form if no address

        return render(request, "Account/edit_address_layout.html", {
            "customer_form": customer_form,
            "address_form": address_form,
            "customer": customer,
            "email": request.user.email,
            "procceed": procceed
        })

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
                return render(request,"Account/email/otp_verification_layout.html")
        else:
            storage = messages.get_messages(request)
            storage.used = True  # Mark all messages as used (cleared)
            messages.success(request, "Check your email for OTP")
            return render(request,"Account/email/otp_verification_layout.html")
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

            send_mail('OTP-AppleAlley',f'Your otp is {otp}','devswebcraft@gmail.com',[email],fail_silently=False)
            request.session['email_otp'] = otp

            return redirect("verifyotp")


        else:
            return render(request,"Account/email/reset_password.html"
)
