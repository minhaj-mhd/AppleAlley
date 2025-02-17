import razorpay
import hmac
import hashlib
from django.conf import settings
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from .models import Order,OrderItem
from products.models import Product
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def Cart(request):
    user = request.user
    if user:
        customer=user.customer
        cart_obj,create=Order.objects.get_or_create(owner=customer,
                                             order_status=Order.CART_STAGE)
        email_verified=customer.email_verified
        context={"cart":cart_obj,"verified":email_verified}
        print(cart_obj.cart.all())
        return render(request,"Cart/cart_layout.html",context)



    return render(request,"Cart/cart_layout.html")
def AddToCart(request):
    if request.POST:
        user=request.user
        if user.is_authenticated:
            print(user)
            customer = user.customer
            product_id = request.POST.get("product_id")
            quantity = int(request.POST.get("quantity"))
            cart_obj,created=Order.objects.get_or_create(
                owner=customer,
                order_status=Order.CART_STAGE
            )
            cart_obj.save()
            ordered_item,created = OrderItem.objects.get_or_create(
            product=Product.objects.get(id=product_id),
            order=cart_obj
            )
            if created:
                ordered_item.quantity=quantity
            else:
                ordered_item.quantity=ordered_item.quantity+quantity
            ordered_item.save()
            return redirect("cart")
        else:
            return redirect("account")
def removeProduct(request):
    if request.POST:
        obj=request.POST.get("obj_id")
        orderItem=OrderItem.objects.get(id=obj)
        orderItem.delete()
    return redirect("cart")
def checkout(request):
    return render(request,"Cart/confirmation_page.html")

def cancelOrder(request,id):
    item = Order.objects.get(id=id)
    if request.user == item.owner.user:
        item.order_status=4
        item.save()
    return redirect("profile")

def confirmCancelOrder(request,id):
    order = Order.objects.get(id=id)
    items = order.cart.all()
    print("cancelitems:",items)
    return render(request,"account/confirm_cancel.html",{"obj":items,"id":id})
              

def confirmOrder(request):
    if request.user:
        user = request.user
        customer=user.customer
        address = customer.address
        print(address)
        cart_obj=Order.objects.get(owner=customer,order_status=Order.CART_STAGE)
        print(cart_obj)
        orders=cart_obj.cart.all()
        print(orders)
        total = 0
        for obj in orders:
            product = obj.product
            print(product.price)
            total = total+int(product.price)*int(obj.quantity)

        total=total+total*0.18
        context={
            "address":address,
            "total":total,
            "customer":customer
        }

        return render(request,"Cart/confirm_order.html",context)
def payment(request):
    if request.method == "POST":
        amount_str = request.POST.get("amount").strip("/")
        amount = int(float(amount_str) * 100)  # Convert to paise
        print("amount",amount)
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        print(client)
        order = client.order.create({
            "amount": amount,
            "currency": "INR",
            "payment_capture": 1,  # Auto-capture payment
        })

        context = {
            "razorpay_key_id": settings.RAZORPAY_KEY_ID,
            "order_id": order["id"],
            "amount": amount,
        }
        return render(request, "cart/payment.html", context)

    return render(request, "cart/payment.html")
    
@csrf_exempt
def payment_success(request):
    if request.method == "POST":
        import json
        payload = json.loads(request.body)
        razorpay_order_id = payload.get('razorpay_order_id')
        razorpay_payment_id = payload.get('razorpay_payment_id')
        razorpay_signature = payload.get('razorpay_signature')

        generated_signature = hmac.new(
            settings.RAZORPAY_KEY_SECRET.encode('utf-8'),
            (razorpay_order_id + "|" + razorpay_payment_id).encode('utf-8'),
            hashlib.sha256
        ).hexdigest()

        if generated_signature == razorpay_signature:
            # Payment is successful
            user=request.user
            customer=user.customer
            order=Order.objects.get(owner=customer,order_status=Order.CART_STAGE)
            if order:
                order.order_status=Order.ORDER_CONFIRMED
                order.save()
            return JsonResponse({"message": "Payment verified successfully!"})
            
        else:
            return JsonResponse({"message": "Payment verification failed!"}, status=400)

