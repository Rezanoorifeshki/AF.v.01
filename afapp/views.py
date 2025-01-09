from django.shortcuts import render,get_object_or_404,redirect,HttpResponse
from django.db.models import Q 
from django.utils.timezone import now
from django.db import IntegrityError
from .models import *
# Create your views here.
def update_discounts(products):
    for item in products:
        if item.discount and item.discountutil and item.discountutil < now():
            item.discount = False
            item.discountpercentage = 0
            item.discountprice = item.price
            item.save()

def search_products(query):
    if query:
       return Product.objects.filter(
            Q(name__icontains=query) | 
            Q(power__icontains=query) | 
            Q(faz__icontains=query) | 
            Q(zirname__icontains=query) | 
            Q(brand__icontains=query) | 
            Q(flux__icontains=query) |
            Q(pol__icontains=query)
       )
    return Product.objects.all() 

def send(request):
    if request.method == "POST":
        phone = request.POST.get("phone")  
        if phone:
            try:
                Subscriber.objects.create(phone=phone)
            except IntegrityError:
                pass  

def home(request):
    send(request)
    categorys=Category.objects.all()
    products=Product.objects.all()
    addres=Addres.objects.all()
    update_discounts(products)
    best_seller=Product.objects.order_by('-sold_count').first()
    if not best_seller or best_seller.sold_count == 0:
        best_seller = None 
    ser = request.GET.get("search")
    if ser:
        filtered_products = search_products(ser)  
        if not filtered_products.exists():
            filtered_products = products  
    else:
        filtered_products = products
    return render(request,'afapp/index.html',context={'categorys':categorys,'products':filtered_products,'best_seller':best_seller,'addres':addres})

def shop(request):
    send(request)
    categorys=Category.objects.all()
    products=Product.objects.all()
    addres=Addres.objects.all()
    update_discounts(products)
    ser = request.GET.get("search")
    if ser:
        filtered_products = search_products(ser)  
        if not filtered_products.exists():
            filtered_products = products  
    else:
        filtered_products = products
    return render(request,'afapp/shop.html',context={'categorys':categorys,'products':filtered_products,'addres':addres})

def shopcat(request,add):
    send(request)
    categorys=Category.objects.all()
    products=Product.objects.filter(category_id=add)
    addres=Addres.objects.all()
    update_discounts(products)
    ser = request.GET.get("search")
    if ser:
        filtered_products = search_products(ser)  
        if not filtered_products.exists():
            filtered_products = products  
    else:
        filtered_products = products
    return render(request,'afapp/shop.html',context={'categorys':categorys,'products':filtered_products,'addres':addres})

def shopproduct(request,add):
    send(request)
    categorys=Category.objects.all()
    addres=Addres.objects.all()
    product=get_object_or_404(Product,id=add)
    ex=product.get_related_products()
    update_discounts([product])
    ser = request.GET.get("search")
    if ser:
        filtered_products = search_products(ser)  
        if not filtered_products.exists():
            filtered_products = Product.objects.all()  
            return render(request,'afapp/shop.html', context={'categorys': categorys, 'products': filtered_products,'addres':addres})
    return render(request,'afapp/shopproduct.html',context={'categorys':categorys,'product':product,'ex':ex,'addres':addres})

def thanks(request):
    send(request)
    categorys=Category.objects.all()
    addres=Addres.objects.all()
    return render(request,'afapp/thanks.html',context={'categorys':categorys,'addres':addres})

def contactus(request):
    send(request)
    categorys=Category.objects.all()
    addres=Addres.objects.all()
    if (request.method=="POST"):
        te=request.POST.get('ttext')
        fl=request.POST.get('flnname')
        em=request.POST.get('eemail')
        if (te and fl and em):
            Contactus.objects.create(text=te,flname=fl,email=em)
            return redirect('/thanks')
    return render(request,'afapp/contactus.html',context={'categorys':categorys,'addres':addres})

def aboutus(request):
    send(request)
    categorys=Category.objects.all()
    about=Aboutus.objects.all()
    addres=Addres.objects.all()
    return render(request,'afapp/aboutus.html',context={'categorys':categorys,'about':about,'addres':addres})

def login(request):
    send(request)
    categorys=Category.objects.all()
    addres=Addres.objects.all()
    error_message =None
    if(request.method=='POST'):
        user=request.POST.get('singin-email')
        password=request.POST.get('singin-password')
        if (password and user):
            if(user=='reza' and password=='123'):
                request.session['issing']=1
                return redirect('/account')
            else:
                error_message = 'نام کاربری یا رمز عبور اشتباه است.' 
                return render(request, 'afapp/login.html', {'categorys': categorys,'addres': addres,'error':error_message})
    return render(request, 'afapp/login.html', {'categorys': categorys,'addres': addres})

def account(request):
    send(request)
    categorys=Category.objects.all()
    addres=Addres.objects.all()
    x=request.session.get('issing')
    if (x):
         return render(request,'afapp/account.html',context={'categorys':categorys,'addres':addres})
    else:
        return redirect('/login')
   
