from django.http.response import HttpResponse
from django.shortcuts import render,redirect
from .models import *
import time
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from .forms import BusinessForm,ProductForm

# Create your views here.

def index(request):   
    carousel = Carousel.objects.all()
    brand = Brand.objects.all()[:6]
    category = Category.objects.all()
    childcategory = ChildCategory.objects.all()
    ad = Ad.objects.all()
    if Product.is_available == True:
        product = Product.objects.all()[:8]
    else:
        product = Product.objects.filter(is_available=True)[:8]    

    context = {
        'carousels' : carousel,
        'categories' : category,
        'childcategories' : childcategory,
        'ads' : ad,
        'products' : product,
        'brands' : brand,
    }

    return render(request,"index.html",context=context)

def brands(request):
    brand = Brand.objects.all()
    context = {
        'brands' : brand
    }
    return render(request,"brands.html",context=context)

def products(request):  
    if request.user.is_authenticated:
        user = request.user
        registers = Register.objects.filter(user=user)
        print(registers.values('city'))
    else:
        user = None
        registers = None              
    product = None
    category = Category.objects.all()
    childcategory = ChildCategory.objects.all()
    categoryid = request.GET.get('category')
    childcategoryid = request.GET.get('childcategory')
    if categoryid:
        product =  Product.product_by_categories(category_id=categoryid)
    elif childcategoryid:
        product = Product.product_by_childcategories(childcategory_id=childcategoryid)
    else:
        product = Product.objects.filter(is_available=True)

    context={
        'products' : product,
        'categories' : category,
        'childcategories' : childcategory
    }
    return render(request,"products.html",context=context)

def see(request,product_id):
    product = Product.objects.filter(id=product_id,is_available=True)
    context = {
        'products' : product
    }
    return render(request,"see.html",context=context)

def register(request):
    if request.method == "POST":
        firstname = request.POST.get('fname')
        lastname = request.POST.get('lname')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        city = request.POST.get('city')
        address = request.POST.get('address')
        state = request.POST.get('state')
        pincode = request.POST.get('pincode')
        mobile = request.POST.get('phone')

        if User.objects.filter(email=email).exists():
            messages.error(request,"Already have an Account")
        elif User.objects.filter(username=username).exists():
            messages.error(request,"Username not available")
        else:
            if password1 == password2:
                user = User.objects.create_user(first_name=firstname,last_name=lastname,username=username,email=email,password=password1)
                user.save()
                register = Register(user=user,name=user.first_name,city=city,address=address,pincode=pincode,state=state,mobile=mobile)
                register.save()
                messages.success(request,"You are Successfully registered")
            else:
                messages.error(request,"Passwords are not matching")              
    return render(request,"register.html")

def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username,password=password)

        if user is not None:
            auth.login(request,user)
            messages.success(request,"Loggedin Successfully")
            return redirect("/")
        else:
            messages.error(request,"Invalid Credentials")        
    return render(request,"login.html")

def logout(request):
    auth.logout(request)
    messages.success(request,"Logged out Successfully")
    return redirect("/")

def search(request):
    query = request.GET.get('search')
    if query:
        product = Product.objects.filter(name__icontains = query)
    else:
        return HttpResponse("nope")
    context = {
        'products' : product
    }        
    print(query)
    return render(request,"search.html",context=context)


import razorpay
client = razorpay.Client(auth=("rzp_test_FVgxuzBdJ9c4So", "4riLfbUSnTNTzkNFzoIqA7GD"))

def buy(request,product_id):
    if request.user.is_authenticated:
        user = request.user
        product = Product.objects.get(id=product_id)
        quantity = int(request.GET.get('quantity'))
        if quantity < product.minimumquantity :
            return render(request,"criteria.html")
        else:
            quantityproduct = float(quantity)    
        print(quantity)
    else:
        return redirect('/login')    
    
    
    productprice = (product.price - (product.price*product.discount/100))
    order_amount = productprice * quantityproduct * 100
    order_currency = 'INR'
    order_receipt = 'order_rcptid_{{product.id}}_{{user.id}}'
    data = {
        'amount' : order_amount,
        'currency' : order_currency,
        'receipt' : order_receipt
    }
    order = client.order.create(data=data)
    payment = Payment(user=user,product=product,status='fail',orderid=order.get('id'),quantity=quantityproduct)
    payment.save()
    print(order)
    context={
        'product':product,
        'order': order
    }

    return render(request,"buy.html",context) 
            
        
@csrf_exempt
def verifypayment(request):
    if request.method == "POST":
        print(request.POST)
        razorpay_payment_id = request.POST.get('razorpay_payment_id')
        razorpay_order_id = request.POST.get('razorpay_order_id')
        razorpay_signature = request.POST.get('razorpay_signature')
        params_dict = {
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': razorpay_payment_id,
            'razorpay_signature': razorpay_signature
        }
        client.utility.verify_payment_signature(params_dict)
        payment = Payment.objects.get(orderid = razorpay_order_id)
        payment.status = "success"
        payment.paymentid = razorpay_payment_id
        payment.save()

        user_product = Userproduct(user = payment.user, name=payment.user.first_name,payment=payment,product=payment.product,quantity=payment.quantity,orderid=payment.orderid,paymentid=payment.paymentid,totalprice=payment.product.price*payment.quantity)
        user_product.save()
        return redirect ('/orders')

def orders(request):
    if request.user.is_authenticated:
        user = request.user
    else:
        user = None

    userproduct = Userproduct.objects.filter(user=user)

    context = {
        'userproducts' : userproduct
    }        
    return render(request,"order.html",context=context)

def business(request):
    forms = BusinessForm()
    context = {
        'form' : forms
    }
    if request.method == "POST":
        form = BusinessForm(request.POST,request.FILES)
        if form.is_valid():
            form.save() 
            messages.success(request,"We are verifying your business after verifiying your business you can login and add products")
            return redirect("/businesslogin")
        else:
            messages.error(request,"Put a unique gstin")          
    return render(request,"business.html",context=context)

def businesslogin(request):
    if request.method == "POST":
        firmname = request.POST.get('firmname')
        gstin = request.POST.get('gstin')
    try:
        reg = Business.objects.get(gstin=gstin,firmname=firmname,verified=True)
        # print(reg)
        if reg:
            temp = {}
            temp['gstin'] = reg.gstin 
            temp['id'] = reg.id
            temp['firmname'] = reg.firmname
            request.session['reg'] = temp
            return redirect("/")
        else:
            messages.error(request,"Register yourself")
    except:
        messages.error(request,"hi")
        return render(request,"businesslogin.html")    

def addproduct(request):    
    forms = ProductForm() 
    context = {
        'form' : forms 
    }
    if request.method == "POST":
        form = ProductForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            time.sleep(2)
            messages.success(request,"We are verifiying your products if all ok then will be onboarded on website in 24 hours, Thanks")
            return redirect("/myproducts")
    return render(request,"addproduct.html",context=context)

def myproducts(request):
    sessionid = request.session["reg"]
    gstin = sessionid['gstin']
    firmname = sessionid['firmname']
    product = Product.objects.filter(gstin=gstin)
    context = {
        'product' : product,
        'firmname' : firmname,
        'gstin' : gstin
    }
    return render(request,"myproducts.html",context=context)

def businesslogout(request):
    request.session.clear()
    return redirect("/")

def orderslist(request):
    sessionid = request.session["reg"]
    gstin = sessionid['gstin']
    firmname = sessionid['firmname']
    product = Product.objects.filter(gstin=gstin)
    userproduct = Userproduct.objects.filter(product__in=product)
    register = Register.objects.filter(user__in=userproduct.values('user'))
    print(register)

    context = {
        'userproduct' : userproduct,
        'register' : register
    }

    return render(request,"orderslist.html",context=context)
