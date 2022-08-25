from django.shortcuts import render
from .models import Order, Product,Contact,OrderUpdate
from math import ceil
from django.http import HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt


# Create your views here.

def index(request):
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds':allProds}
    return render(request, 'shop/index.html', params)


def searchMatch(query, item):
    '''return true only if query matches the item'''
    if query in item.desc.lower() or query in item.product_name.lower() or query in item.category.lower():
        return True
    else:
        return False



 
#harry
def search(request):
    query = request.GET.get('search')
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prodtemp = Product.objects.filter(category=cat)
        prod = [item for item in prodtemp if searchMatch(query, item)]

        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        if len(prod) != 0:
            allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds': allProds, "msg": ""}
    if len(allProds) == 0 or len(query)<3:
        params = {'msg': "Please make sure to enter relevant search query"}
    return render(request, 'shop/search.html', params)








def about(request): 
    return render(request,"shop/about.html")


def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        desc = request.POST.get('desc')
        contact = Contact(name=name,email=email,phone=phone,desc=desc)
        contact.save()
        send = True
        return render(request,"shop/contact.html",{'send':send})
    return render(request,"shop/contact.html")



def tracker(request):
    if request.method == "POST":
        orderid = request.POST.get('orderid')
        email = request.POST.get('email')
        try:
            order = Order.objects.filter(order_id=orderid, email=email)
            if len(order)>0:
                update = OrderUpdate.objects.filter(order_id=orderid)
                updates= []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timestamp})
                    response = json.dumps({"status":"success", "updates":updates, "itemJson":order[0].items_json},default=str)
                return HttpResponse(response)

            else:
                return HttpResponse('{"status":"noitem"}')
        except Exception as e:
            return HttpResponse('{"status":"error"}')
    return render(request,"shop/tracker.html")






def productView(request,prodid):
    #fetch the prodduct using id
    product = Product.objects.filter(id=prodid)
    print(product)
    return render(request,"shop/productview.html", {'product':product[0]})



def checkout(request):
    if request.method == "POST":
        items_json = request.POST.get('itemsJson')
        name = request.POST.get('name')
        amount = request.POST.get('amount')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address1 = request.POST.get('address1')
        address2 = request.POST.get('address2')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip_code = request.POST.get('zip_code')
        order = Order(items_json=items_json,name=name,email=email,phone=phone,address1=address1,address2=address2,city=city,  state=state, zip_code=zip_code, amount=amount)
        order.save()
        update = OrderUpdate(order_id=order.order_id, update_desc="The Order Has Been Placed")
        update.save()
        thank = True
        id = order.order_id
        # return render(request,"shop/checkout.html", {'thank':thank, 'id':id})
        #request paytm to transfer the amount to your account after payment by user
    return render(request,"shop/checkout.html")

    

@csrf_exempt
def handlerequest(request):
    #paytm will send post request here
    pass