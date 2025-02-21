from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path("orders",views.Orders,name="orders"),
    path("cart/",views.Cart,name="cart"),
    path("addtocart",views.AddToCart,name="addtocart"),
    path("removeproduct",views.removeProduct,name="removeproduct"),
    path("confirmorder",views.confirmOrder,name="confirmorder"),
    path("payment/",views.payment,name="payment"),
    path("checkout",views.checkout,name="checkout"),
    path("cancelorder/<int:id>",views.cancelOrder,name="cancel"),
    path('confirmcancelorder/<int:id>',views.confirmCancelOrder,name="confirmcancel"),
    path('payment-success/', views.payment_success, name='payment-success'),
    
]