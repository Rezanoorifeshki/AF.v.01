from django.shortcuts import render,get_object_or_404,redirect,HttpResponse
from django.db.models import Q 
from django.utils.timezone import now
from django.db import IntegrityError
from django.contrib.auth import authenticate , login as lg , logout as lgo
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from .models import *
from .forms import CostomUserForm
import re
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

def register(request):
    send(request)
    categorys=Category.objects.all()
    addres=Addres.objects.all()

    if(request.method=='POST'):
        password1=request.POST.get("password1")
        password2=request.POST.get("password2")
        username=request.POST.get("username")
        username_regex = r'^[a-zA-Z0-9_-]{3,20}$'

        if not re.match(username_regex, username):
            error_message = 'نام کاربری باید بین 3 تا 20 کاراکتر باشد و فقط از حروف، اعداد، آندرلاین یا خط فاصله استفاده کند.'
            return render(request, 'afapp/register.html', context={'categorys': categorys, 'addres': addres, 'error_message': error_message})

        if CostomUser.objects.filter(username=username).exists():
            error_message = 'نام کاربری وارد شده قبلاً ثبت شده است.'
            return render(request, 'afapp/register.html', context={'categorys': categorys, 'addres': addres, 'error_message': error_message})

        if password1 != password2:
            error_message = 'رمز عبور شما با هم همخوانی ندارد.'
            return render(request, 'afapp/register.html', context={'categorys': categorys, 'addres': addres, 'error_message': error_message})

        password_regex = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@#$!%*?&])[A-Za-z\d@#$!%*?&]{8,}$'
        if not re.match(password_regex, password1):
            error_message = (
                'رمز عبور باید حداقل 8 کاراکتر باشد و شامل حداقل یک حرف کوچک، یک حرف بزرگ، یک عدد و یک کاراکتر خاص مانند @, #, $.')
            return render(request, 'afapp/register.html', context={'categorys': categorys, 'addres': addres, 'error_message': error_message})

        if (password1==password2):
            CostomUser.objects.create_user(username=username,password=password1)
            return redirect("/login")
        
    return render(request,'afapp/register.html',context={'categorys':categorys,'addres':addres})

def login(request):
    send(request)
    categorys=Category.objects.all()
    addres=Addres.objects.all()

    if(request.method=='POST'):
        password=request.POST.get("password")
        username=request.POST.get("username")
        che = authenticate(username=username, password=password)

        if che is not None:
                lg(request, che)
                return redirect("/account")
            
        else:
                error_message = "نام کاربری یا رمز عبور اشتباه است."
                return render(request, 'afapp/login.html', {'categorys': categorys, 'addres': addres, 'error_message': error_message})

    return render(request, 'afapp/login.html', {'categorys': categorys, 'addres': addres})

@login_required
def account(request):
    send(request)
    user =request.user
    categorys=Category.objects.all()
    addres=Addres.objects.all()
  
    if( request.method == 'POST'):
        
        form =CostomUserForm(request.POST, instance=user) 
        if form.is_valid():
            current_password = form.cleaned_data.get('current_password')

            if current_password and not user.check_password(current_password):
                form.add_error('current_password', 'رمز عبور فعلی اشتباه است.')
                return render(request,'afapp/account.html',context={'categorys':categorys,'addres':addres,'form':form})
            
            new_password = form.cleaned_data.get('new_password')

            if new_password:
                user.set_password(new_password) 

            form.save()  
            user.save() 
            update_session_auth_hash(request, user) 

            messages.success(request, 'اطلاعات با موفقیت ذخیره شد!')
            return render(request,'afapp/account.html',context={'categorys':categorys,'addres':addres,'form':form})

        else:
            messages.error(request, 'لطفاً تمام فیلدها را به درستی پر کنید.')
    else:
        form =CostomUserForm(instance=user) 

    return render(request,'afapp/account.html',context={'categorys':categorys,'addres':addres,'form':form})

def logout(request):
    lgo(request)
    return redirect('/login')
  

   
