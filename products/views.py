from django.shortcuts import render
from django.http import JsonResponse
from .models import Product,IPhoneVariant,IPhoneModel,IPhoneSeries
from django.db.models import Q
# Create your views here.
def index(request):
    
    return render (request,"Home/index.html")
def ListProducts(request):
    obj = IPhoneVariant.objects.all()
    
    return render(request,"ProductList/list_layout.html",{"obj":obj})
def ProductDetail(request,id):
    obj = IPhoneVariant.objects.get(id=id)
    
    return render(request,"Products/product_page_layout.html",{"product":obj})
def ProductBySeries(request,series):
    series = IPhoneSeries.objects.get(name=series)
    models = IPhoneModel.objects.filter(series=series)
    obj = IPhoneVariant.objects.filter(model__in=models)
    return render(request,"ProductList/list_layout.html",{"obj":obj,"series":series})
def SearchProducts(request):
    query=request.GET.get("query")
    obj = IPhoneVariant.objects.filter(Q(model__name__icontains=query) | Q(model__series__name__icontains=query)).select_related("model", "storage", "color")

    results = [{"id": product.id, "title": product.model.name, "storage": product.storage.capacity, "color": product.color.color_name} for product in obj]
    return JsonResponse({"results":results})