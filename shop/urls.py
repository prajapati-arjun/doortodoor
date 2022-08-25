from django.urls import path
from shop import views

urlpatterns = [
    path("", views.index,name = "ShopHome"),
    path("about/", views.about,name = "About"),
    path("contact/", views.contact,name = "Contact"),
    path("tracker/", views.tracker,name = "Tracker"),
    path("search/", views.search,name = "Search"),
    path("productview/<int:prodid>", views.productView,name = "ProductView"),
    path("checkout/", views.checkout,name = "Checkout"),
    path("handlerequest/", views.handlerequest,name = "HandleRequest"),
]