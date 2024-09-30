from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
import smtplib, ssl
import random
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import  CartItem, Product,CustomerProfile,Orders
from .forms import ProductForm, UserForm, UserProfileInfoForm,CoustomerForm
from django.contrib.auth.models import User


from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages





def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            
            if user.is_superuser:
                return redirect("home")
            else:
                return HttpResponse("<script>alert('Username or Password is incorrect');window.location='../login';</script>")
          # Redirect to index upon successful login
        if CustomerProfile.objects.filter(username=username, password=password).exists():
            a =CustomerProfile.objects.filter(username = username , password = password ).values_list('username', flat=True)
            print(a)
            
            request.session['uid']=str(a[0])
            return redirect('index')
        elif CustomerProfile.objects.filter(email=username, password=password).exists():
            a =CustomerProfile.objects.filter(email = username , password = password ).values_list('username', flat=True)
            print(a)
            
            request.session['uid']=str(a[0])
            return redirect('index')
        elif CustomerProfile.objects.filter(phone=username, password=password).exists():
            a =CustomerProfile.objects.filter(phone = username , password = password ).values_list('username', flat=True)
            print(a)
        
            request.session['uid']=str(a[0])
            return redirect('index')
        else:
            return HttpResponse("<script>alert('Username or Password is incorrect');window.location='../login';</script>")
    return render(request, 'login.html')

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        if CustomerProfile.objects.filter(email=email).exists():
            a =CustomerProfile.objects.filter(email=email ).values_list('username', flat=True)
            b=CustomerProfile.objects.filter(email=email ).values_list('name', flat=True)
            username = a[0]
            name=b[0]
            random_number = random.randint(1000, 9999)
            request.session['otp']=random_number
            receiver_email = email
            EMAIL_HOST = 'smtp.gmail.com'
            EMAIL_HOST_USER = 'workmailworkmail.w@gmail.com'
            EMAIL_HOST_PASSWORD = 'wdhsywhbquqohtjp'
            EMAIL_PORT = 587
            EMAIL_USE_TLS = True

            password = EMAIL_HOST_PASSWORD
            smtp_server = EMAIL_HOST
            sender_email = EMAIL_HOST_USER

            message = """\
                                        Subject:   OTP for Password reset conformation..

                                        eEarrings: hello """+str(name)+""", Use OTP """+str(random_number)+""" to reset password and use our website and donot share this code with anyone. Reset your password and discover your dezired products from us.. """
            context = ssl.create_default_context()
            with smtplib.SMTP(smtp_server, EMAIL_PORT) as server:
                server.ehlo()  # Can be omitted
                server.starttls(context=context)
                server.ehlo()  # Can be omitted
                server.login(sender_email, password)
                server.sendmail(sender_email, receiver_email, message)
            return render(request, 'forgot1.html',{'un':username,'em':email})
        else:
            return HttpResponse("<script>alert('email not found');window.location='../login';</script>")


    return render(request, 'forgot.html')

def forgot1(request):
    if request.method=='POST':
        otp = request.POST['otp']
        un = request.POST['un']
        if str(request.session['otp'])==str(otp):
            # customer=CustomerProfile.objects.get(username=un)
            return render(request,'password_new.html',{'un':un})
        else:
            return HttpResponse("<script>alert('wrong otp');window.location='../login';</script>")
    return HttpResponse("<script>alert('technical error');window.location='../login';</script>")
def password_new(request):
    if request.method=='POST':
        un=request.POST['un']
        np = request.POST['password']
        cp = request.POST['cp']
        if str(np)==str(cp):
            customer = CustomerProfile.objects.get(username=un)
            customer.password = np
            customer.save()
            return HttpResponse("<script>alert('Updated New Password Successfully..');window.location='../login';</script>")
        else:
            request.session['un']=un
            return HttpResponse("<script>alert('Password not same');window.location='../password_new';</script>")
    un = request.session['un']
    return render(request,'password_new.html',{'un':un})

def myprofile(request):

    user_profile = CustomerProfile.objects.get(username=request.session['uid'])
    return render(request, 'profile.html', {'user_profile': user_profile})

def edit_profile(request):
    username = request.session.get('uid')
    if not username:

        return redirect('login')
    
    try:
        user_profile = CustomerProfile.objects.get(username=username)
    except CustomerProfile.DoesNotExist:

        return redirect('login') 
    
    if request.method == 'POST':
        user_form = CoustomerForm(request.POST, instance=user_profile)
        if user_form.is_valid():
            user_form.save()
            user_profile.name = user_form.cleaned_data['name']
            user_profile.email = user_form.cleaned_data['email']
            user_profile.phone = user_form.cleaned_data['phone']
            user_profile.password = user_form.cleaned_data['password']
            user_profile.save()
            return redirect(myprofile)
    else:
        user_form = CoustomerForm(instance=user_profile)
    
    return render(request, 'edit_profile.html', {'user_form': user_form})
def first(request):
    query = request.GET.get('search', '')
    products = Product.objects.filter(name__icontains=query)
    return render(request, 'first.html', {'products': products})


def product_list(request):
    query = request.GET.get('search', '')
    category = request.GET.get('category', '')
    
    if category:
        products = Product.objects.filter(category=category)
    else:
        products = Product.objects.filter(name__icontains=query)
    
    return render(request, 'product_list.html', {'products': products, 'query': query, 'category': category})


# User Register




def register_request(request):
    if request.method == 'POST':
        user_form = CoustomerForm(request.POST)
        if user_form.is_valid():
            try:
                user_form.save()
                return redirect(login_view)
            except:
                pass
    else:
        user_form = CoustomerForm()
    return render(request, 'register.html', {'user_form': user_form})


# User Logout

def logout_view(request):
    return render(request,'logout.html')

def alogout_view(request):
    return render(request,'alogout.html')

def prediction(request):
    # You can add context data if needed
    return render(request, 'prediction.html')

def profile_view(request):
    # Your logic for the profile view
    return render(request, 'profile.html')

def visualization_view(request):
    # Your logic for the visualization view
    return render(request, 'visualization.html')

def report_view(request):
    # Your logic for the report view
    return render(request, 'report.html')
def profile_view(request):
    # Your code here
    return render(request, 'profile_settings.html')



# Home Page
@login_required
def home(request):
  products = Product.objects.all()
  return render(request, 'home.html', {'products': products})

# Add Product

@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product added successfully!')
            return redirect('home')
    else:
        form = ProductForm()
    return render(request, 'add_product.html', {'form': form})

# Edit Product
@login_required
def edit_product(request, id):
    product = get_object_or_404(Product, id=id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ProductForm(instance=product)
    return render(request, 'edit_product.html', {'form': form})


# Delete Product
@login_required
def delete_product(request, id):
    product = Product.objects.get(id=id)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted successfully!')
        return redirect('home')
    return render(request, 'delete_product.html', {'product': product})


def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})


def product_list(request):
    query = request.GET.get('search', '')
    products = Product.objects.filter(name__icontains=query)
    return render(request, 'product_list.html', {'products': products})

def orders(request):
    orders = Orders.objects.filter(user=request.session['uid'],status='paid')
    
    print(orders[0].total)
    return render(request, 'orders.html', {'orders': orders, })

def ordered_items(request,id):
    oitems=CartItem.objects.filter(user=request.session['uid'],orderid=id)
    total_price = sum(item.price * item.quantity for item in oitems)
    return render(request, 'ordered_items.html', {'cart_items': oitems,'total_price': total_price})
def aordered_items(request,id):
    oitems=CartItem.objects.filter(user=request.session['uid'],orderid=id)
    total_price = sum(item.price * item.quantity for item in oitems)
    return render(request, 'aordered_items.html', {'cart_items': oitems,'total_price': total_price})

def ship_order(request,id):
    order = Orders.objects.get(id=id)
    order.sstatus='shipped'
    order.save()
    return HttpResponse("<script>alert('shipped');window.location='../all_orders';</script>")

def deliver_order(request,id):
    order = Orders.objects.get(id=id)
    order.sstatus='delivered'
    order.save()
    return HttpResponse("<script>alert('delivered');window.location='../all_orders';</script>")

def all_orders(request):
    processing = Orders.objects.filter(status='paid',sstatus ='processing')
    shipped = Orders.objects.filter(status='paid',sstatus ='shipped')
    delivered = Orders.objects.filter(status='paid',sstatus ='delivered')
    return render(request, 'all_orders.html', {'processing': processing,'shipped':shipped,'delivered':delivered })


def view_cart(request):
    
    cart_items = CartItem.objects.filter(user=request.session['uid'], status='carted')
    for item in cart_items:
        if item.product.quantity <item.quantity:
            order = Orders.objects.get(id =item.orderid ,user=request.session['uid'],status='pending')
            print("order",order)
            amo = item.quantity * item.product.price
            order.total = order.total - amo
            print(amo,order.total)
            order.save()
            item.delete()
    cart_items = CartItem.objects.filter(user=request.session['uid'], status='carted')
    total_price = sum(item.product.price * item.quantity for item in cart_items)


    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})
 

def add_to_cart(request, product_id): 
    import datetime
    time = datetime.datetime.now().strftime("%H:%M:%S")
    date =datetime.datetime.now().date()
    product = Product.objects.get(id=product_id) 
    # if request.user.is_authenticated:
    product = Product.objects.get(id=product_id) 
    if product.quantity > 0: 
        if Orders.objects.filter(user=request.session['uid'],status='pending').exists():
            ord=Orders.objects.filter(user=request.session['uid'],status='pending').values_list('pk', flat=True)
            cart_item, created = CartItem.objects.get_or_create(product=product, user=request.session['uid'],orderid=ord[0],date_added=date) 
            cart_item.quantity += 1 
            if product.quantity<cart_item.quantity:
                return HttpResponse("<script>alert('no more stocks right now');window.location='../../cart';</script>")

            order = Orders.objects.get(user=request.session['uid'],status='pending')
            order.total = order.total + product.price
            order.save()
            cart_item.save()

        else:
            order, created = Orders.objects.get_or_create(total=product.price,user=request.session['uid'],date=date,status='pending',time=time)
            cart_item, created = CartItem.objects.get_or_create(product=product, user=request.session['uid'],orderid=order.pk,date_added=date)
            cart_item.quantity += 1 
            order.save()
            cart_item.save()

    else:
        messages.error(request, 'Product is not available at the moment.')
    return redirect('view_cart')
    # else:
    #     messages.error(request, 'Please log in to add items to your cart.')
    #     return redirect('login')
 

def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    product = cart_item.product
    product.quantity += cart_item.quantity
    order = Orders.objects.get(user=request.session['uid'],status='pending',id= float(cart_item.orderid))
    order.total = float(order.total) - float(product.price)
    order.save()

    product.save()
    if cart_item.quantity == 1: # check if the quantity is 1, not 0
        cart_item.delete()
    else:
        cart_item.quantity -= 1 # decrease the quantity by 1
        cart_item.save()

    return redirect('view_cart')

# views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Product, CartItem
from .forms import CheckoutForm


# def checkout(request):
#     if request.method == 'POST':
#         form = CheckoutForm(request.POST, request=request)
#         cart_items = CartItem.objects.filter(user=user)
#         total_price = sum(item.product.price * item.quantity for item in cart_items)

        # return render(request, 'purchase_confirmation.html', {'user': user, 'cart_items': cart_items, 'total_price': total_price})
#     else:
#         form = CheckoutForm(request=request)
#     return render(request, 'checkout.html', {'form': form})

def checkout(request):
    username = request.session.get('uid')
    if not username:

        return redirect('login')
    
    try:
        order = Orders.objects.get(user=username,status='pending')
        order.total
        s="0.00"
        if str(order.total) == str(s):
            return HttpResponse("<script>alert('Cart is empty..');window.location='../index';</script>")
    except:
        return HttpResponse("<script>alert('Cart is empty..');window.location='../index';</script>")
         
    if request.method == 'POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        contact = request.POST['contact']
        address =request.POST['address']
        user=(fname,lname,contact,address)
        request.session['fn']=fname
        request.session['ln']=lname
        request.session['contact']=contact
        request.session['address']=address
        cart_items = CartItem.objects.filter(user=username,status='carted')
        order =Orders.objects.get(user=username,status ='pending')
        total=order.total
        return render(request, 'purchase_confirmation.html', {'user': user, 'cart_items': cart_items, 'total_price': total})
    else:
        check_form = CheckoutForm(instance=order)
    return render(request, 'checkout.html', {'check_form': check_form})


from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Category

def add_category(request):
    if request.method == 'POST':
        name = request.POST['name']
        new_category = Category(name=name)
        new_category.save()
        return HttpResponseRedirect(reverse('home'))
    else:
        return render(request, 'add_category.html')
from django.shortcuts import render, redirect
from .models import CartItem, Product
from django.contrib import messages

def confirm_purchase(request):
    order = Orders.objects.get(user=request.session['uid'],status='pending')
    print(order.pk)
    cart_items = CartItem.objects.filter(user=request.session['uid'],status ='carted')
    print(cart_items)

    for item in cart_items:
        print(item)
        product = item.product
        product.quantity -= item.quantity
        product.save()
        item.status='ordered'
        item.price =item.product.price
        item.save()
    total = order.total 
    order.status ='paid'
    order.address=request.session['address']
    order.lname = request.session['ln']
    order.fname = request.session['fn']
    order.contact = request.session['contact']
    import datetime
    time = datetime.datetime.now().strftime("%H:%M:%S")
    date =datetime.datetime.now().date()
    order.date =date
    order.time =time
    order.sstatus ='processing'
    order.save()
    a = total
    total = float(total) * 100
    import razorpay
    client = razorpay.Client(auth=("rzp_test_SROSnyInFv81S4", "WIWYANkTTLg7iGbFgEbwj4BM"))
    payment = client.order.create({'amount': total, 'currency': 'INR', 'payment_capture': '1'})
    return render(request,'activitypayment.html',{'payment':payment, 'amount':total, 'a':a})


    return redirect('thank_you_page')
def thank_you_page(request):
    return render(request, 'thank_you.html')
def product_detail(request, product_id): 
    product = Product.objects.get(id=product_id) 
    return render(request, 'product_detail.html', {'product': product})

# def index_home(request):
#     products = Product.objects.all()
#     return render(request, 'index.html', {'products': products})

def first(request):
    products = Product.objects.all()
    return render(request, 'first.html', {'products': products})

# def index_home(request):
#     query = request.GET.get('search', '')
#     products = Product.objects.filter(name__icontains=query)
#     return render(request, 'index.html', {'products': products})

def index_home(request):
    query = request.GET.get('search', '')
    category = request.GET.get('category', '')
    
    if category:
        products = Product.objects.filter(category=category)
    elif query:
        products = Product.objects.filter(name__icontains=query)
    else:
        products = Product.objects.all()
    
    return render(request, 'index.html', {'products': products, 'query': query, 'category': category})



from django.shortcuts import render
from decimal import Decimal
from .models import Product, Orders

def visualization_view(request):
    # Fetch product data from the database
    product_data = Product.objects.values('name', 'price', 'quantity')
    order_data = Orders.objects.values('status', 'total', 'date')

    # Prepare data for charts (Products)
    product_names = [product['name'] for product in product_data]
    product_prices = [float(product['price']) for product in product_data]
    product_quantities = [product['quantity'] for product in product_data]

    # Prepare data for charts (Orders)
    order_totals = [float(order['total']) for order in order_data]
    order_dates = [order['date'] for order in order_data]
    order_statuses = [order['status'] for order in order_data]

    # Count order statuses
    status_counts = {status: order_statuses.count(status) for status in set(order_statuses)}

    context = {
        'product_names': product_names,
        'product_prices': product_prices,
        'product_quantities': product_quantities,
        'order_totals': order_totals,
        'order_dates': order_dates,
        'status_counts': status_counts
    }
    return render(request, 'visualization.html', context)


import csv
from django.http import HttpResponse
from .models import Product, Orders

def download_report(request):
    # Create the HttpResponse object with the appropriate CSV header
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="report.csv"'

    writer = csv.writer(response)
    writer.writerow(['Product Name', 'Price', 'Quantity', 'Order Status', 'Total', 'Date'])

    # Fetch data from the database
    products = Product.objects.all()
    orders = Orders.objects.all()

    for product in products:
        writer.writerow([product.name, product.price, product.quantity, '', '', ''])  # Add product details

    for order in orders:
        writer.writerow(['', '', '', order.status, order.total, order.date])  # Add order details

    return response

def report_view(request):
    return render(request, 'report.html')

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages

@login_required
def user_management(request):
    users = User.objects.all()  # Get all users
    return render(request, 'user_management.html', {'users': users})

# Optional: Add view for deleting a user
@login_required
def delete_user(request, user_id):
    user = User.objects.get(id=user_id)
    if request.method == 'POST':
        user.delete()
        messages.success(request, 'User deleted successfully!')
        return redirect('user_management')  # Redirect to user management page
    return render(request, 'confirm_delete_user.html', {'user': user})

import google.generativeai as genai
from django.conf import settings
from django.http import JsonResponse


# Initialize the Gemini API
genai.configure(api_key=settings.GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

# Add this new view to your views.py file
def chatbot(request):
    if request.method == 'POST':
        user_input = request.POST.get('user_input', '')
        
        # Generate a response using Gemini
        response = model.generate_content(user_input)
        
        return JsonResponse({'response': response.text})
    
    return render(request, 'chatbot.html')