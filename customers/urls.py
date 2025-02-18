from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [

    path("account",views.Account,name="account"),
    path("logout",views.Logout,name="logout"),
    path("profile",views.Profile,name="profile"),
    path("address/<str:procceed>",views.Address,name="address"),
    path("verify_email",views.verify_registration, name="verify_email"),
    path("verify",views.Verify, name="verify"),
    path("verifyotp",views.VerifyOtp, name="verifyotp"),
    path("forgotpassword",views.ForgotPassword, name="reset")

]