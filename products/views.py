from django.shortcuts import render
from django.http import JsonResponse
from .models import Product
from django.db.models import Q
# Create your views here.
def index(request):
    
    return render (request,"Home/index.html")
def ListProducts(request):
    obj = Product.objects.all()
    
    return render(request,"ProductList/list_layout.html",{"obj":obj})
def ProductDetail(request,id):
    obj = Product.objects.get(id=id)
    
    return render(request,"Products/product_page_layout.html",{"product":obj})
def ProductByBrands(request,brand):
    obj = Product.objects.filter(brand=brand)
    return render(request,"ProductList/list_layout.html",{"obj":obj,"brand":brand})
def SearchProducts(request):
    query=request.GET.get("query")
    obj = Product.objects.filter(Q(title__icontains=query) | Q(brand__icontains=query))
    results=[{"id":product.id,"title":product.brand+" "+product.title} for product in obj]
    return JsonResponse({"results":results})