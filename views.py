from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Product ,CartItem, Categories, Subcategories, Order
from django.db.models import Q
import random
import razorpay
# Create your views here.
def index(request):
    data = Product.objects.all()
    return render(request,"index.html",{'data':data})

def about(request):
    return render(request,"about.html")

def signup(request):
    if request.method == "POST":
        fname =  request.POST['fname']
        lname =  request.POST['lname']
        email =  request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        if pass1 == pass2:
            try:
                user = User.objects.create_user(username=email,first_name=fname,last_name=lname,email=email,password=pass1)
                user.save()
                return redirect('signin')
            except Exception:
                error= "User already exists"
                return render(request,"signup.html",{'error':error})
        else:
            error= "passwords does not match"
            return render(request,"signup.html",{'error':error})
    else:
        return render(request,"signup.html")

def signin(request):
    if request.method == "POST":
        uname= request.POST['uname']
        pass1 = request.POST['pass1']
        user =  authenticate(username = uname, password =pass1)
        if user is not None:
            login(request,user)
            return redirect('index')
        else:
            error = "Invalid username or password"
            return render(request,"signin.html",{'error':error})
    else:
        return render(request,"signin.html")
    
def signout(request):
    logout(request)
    return redirect('index')

def product_details(request,pid):
    data = Product.objects.get(id= pid)
    return render(request,"product_details.html",{'data':data})

def addCart(request,pid):
    data = Product.objects.get(id= pid)
    user = request.user if request.user.is_authenticated else None
    if user:
        cart_item , created = CartItem.objects.get_or_create(product = data,user = user)
    else:
        return redirect('signin')
    
    if not created:
        cart_item.quantity += 1
    else:
        cart_item.quantity = 1
    cart_item.save()
    return redirect('index')

def viewCart(request):
    if request.user.is_authenticated:
        cart_item = CartItem.objects.filter(user = request.user)
    else:
        cart_item = CartItem.objects.filter(user = None)

    context = {}
    context['items'] = cart_item

    total_price = 0
    for x in cart_item:
        total_price += (x.product.price * x.quantity)

    context['total']=total_price

    length = len(cart_item)
    context['total_product']=length
    return render(request,"cart.html",context)

def updateqty(request,val,pid):
    user = request.user
    c = CartItem.objects.filter(product_id = pid, user = user)
    if val == 0 :
        if c[0].quantity > 1:
            a = c[0].quantity-1
            c.update(quantity=a)
    else:
        a = c[0].quantity+1
        c.update(quantity=a)
    return redirect('viewCart')

def remove_product(request,pid):
    data =  CartItem.objects.filter(product_id = pid)
    data.delete()
    return redirect('viewCart')

def search_product(request):
    url = request.GET.get('product')
    if url == "electronics":
        subcategories = Subcategories.objects.filter(Q(name__iexact="printer") | Q(name__iexact="camera") | Q(name__iexact="tv"))
        categories = Categories.objects.get(name="electronics")
        data = Product.objects.filter(categories__exact=categories)
        return render(request,"index.html",{'data':data, 'sub':subcategories})
    
    elif url == "men":
        subcategories = Subcategories.objects.filter(Q(name__iexact="watch") | Q(name__iexact="shoes") | Q(name__iexact="clothes"))
        categories = Categories.objects.get(name="men")
        data = Product.objects.filter(categories__exact=categories)
        return render(request,"index.html",{'data':data,'sub':subcategories})
    
    elif url == "women":
        subcategories = Subcategories.objects.filter(Q(name__iexact="watch") | Q(name__iexact="shoes") | Q(name__iexact="clothes"))
        categories = Categories.objects.get(name="women")
        data = Product.objects.filter(categories__exact=categories)
        return render(request,"index.html",{'data':data,'sub':subcategories})

    elif url == "kids":
        subcategories = Subcategories.objects.filter(Q(name__iexact="watch") | Q(name__iexact="shoes") | Q(name__iexact="clothes"))
        categories = Categories.objects.get(name="kids")
        data = Product.objects.filter(categories__exact=categories)
        return render(request,"index.html",{'data':data,'sub':subcategories})

    elif url == "home_and_furniture":
        subcategories = Subcategories.objects.filter(Q(name__iexact="sofa") | Q(name__iexact="bed"))
        categories = Categories.objects.get(name="home_and_furniture")
        data = Product.objects.filter(categories__exact=categories)
        return render(request,"index.html",{'data':data,'sub':subcategories})

    elif url == "mobile_and_laptops":
        subcategories = Subcategories.objects.filter(Q(name__iexact="mobile") | Q(name__iexact="laptops"))
        categories = Categories.objects.get(name="mobile_and_laptops")
        data = Product.objects.filter(categories__exact=categories)
        return render(request,"index.html",{'data':data,'sub':subcategories})

def subcategories(request,name):
    sub = Subcategories.objects.get(name=name)
    data = Product.objects.filter(subcategories__exact=sub)
    return render(request,"index.html",{'data':data})

def viewOrder(request):
    cart_item =  CartItem.objects.filter(user=request.user)
    context = {}
    context['items'] = cart_item
    total_price = 0
    for x in cart_item:
        total_price += (x.product.price * x.quantity)

    context['total']=total_price

    length = len(cart_item)
    context['total_product']=length

    return render(request,"viewOrder.html",context)

def payment(request):
    c = CartItem.objects.filter(user=request.user)
    oid = random.randrange(1000,9999)
    for x in c:
        product_instance = Product.objects.get(id=x.product.id)
        Order.objects.create(order_id = oid,product=product_instance,quantity =x.quantity,user= request.user)
    orders = Order.objects.filter(user=request.user,is_completed= False)
    total_price = 0
    for x in orders:
        total_price += (x.product.price * x.quantity)
        oid = x.order_id
        pass

    client = razorpay.Client(auth=("rzp_test_YsNwmdCarqpkO3", "kPNiXLTlV03RqTHXYScrCZ5l"))

    data = { "amount": total_price*100, "currency": "INR", "receipt": "oid" }
    payment = client.order.create(data=data)
    context = {}
    context['data'] = payment
    context['amount'] = payment["amount"]
    c.delete()
    orders.update(is_completed = True)

    return render(request,"payment.html",context)