from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path("",views.index, name = "index"),
    path("products/",views.ListProducts, name = "products"),
    path("product/<int:id>",views.ProductDetail,name="productdetails"),
    path("product/<str:series>",views.ProductBySeries,name="productbyseries"),
    path("search/",views.SearchProducts,name="search")
]
