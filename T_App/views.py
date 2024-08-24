from django.shortcuts import render,redirect,HttpResponse
from T_App.models import *
from .forms import NewUserForm
from django.contrib import messages
from django.conf import settings
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm 
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as django_logout
from django.contrib.auth.decorators import login_required
from cart.cart import Cart
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.db.models import F, Sum


import razorpay

client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID,settings.RAZORPAY_KEY_SECRET))

# Create your views here.

def Master(request):
    return render(request, 'master.html')


def index(request):
	category=Category.objects.all()
	age = Age.objects.all()
	brand = Brand.objects.all()
	categoryID=request.GET.get('category')
	AgeID = request.GET.get('age')
	brandID = request.GET.get('brand')
	if categoryID:
		product = Product.objects.filter(sub_category=categoryID)
	elif AgeID:
		product=Product.objects.filter(age_no=AgeID)
	elif brandID:
		product=Product.objects.filter(brand=brandID)
	else:
		product = Product.objects.filter(is_featured=True)

	context ={
		'category' : category,
		'age'  : age,
		'brand' : brand,
		'product' : product,
	}
	return render(request, 'index.html', context)



def signup(request):
	if request.method == "POST":
		form = NewUserForm(request.POST,request.FILES)
		if form.is_valid():

			user = form.save(commit=True)
			user.save()
			auth_login(request, user)
			messages.success(request, "Registration successful." )
			return redirect('index')
			# return redirect("main:homepage")
		return render(request, template_name="registration/signup.html", context={"form":form})
		# messages.error(request, "Unsuccessful registration. Invalid information.")
	form = NewUserForm()
	return render (request=request, template_name="registration/signup.html", context={"form":form})
	



def login(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				auth_login(request, user)
				messages.info(request, f"You are now logged in as {username}.")
				return redirect('index')
			else:
				return render(request=request, template_name="registration/login.html", context={"form":form})
				# messages.error(request,"Invalid username or password.")
		else:
			return render(request=request, template_name="registration/login.html", context={"form":form})
			# messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request=request, template_name="registration/login.html", context={"form":form})

def logout(request):
    django_logout(request)
    return  redirect('index')


@login_required(login_url="login")
def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    if product.stock > 0:
        cart.add(product=product)
        product.stock -= 1 # reduce stock when item is added to cart
        product.save()
    return redirect("index")


@login_required(login_url="login")
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    product.stock += 1 # increase stock when item is removed from cart
    product.save()
    return redirect("cart_detail")


@login_required(login_url="login")
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    if product.stock > 0:
        cart.add(product=product)
        product.stock -= 1 # reduce stock when item is added to cart
        product.save()
    return redirect("cart_detail")


@login_required(login_url="login")
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    product.stock += 1 # increase stock when item is removed from cart
    product.save()
    return redirect("cart_detail")


@login_required(login_url="login")
def cart_clear(request):
    cart = Cart(request)
    for item in cart:
        product = item['product']
        product.stock += item['quantity'] # increase stock for each item in the cart
        product.save()
    cart.clear()
    return redirect("cart_detail")

@login_required(login_url="login")
def cart_detail(request):
    return render(request, 'cart/cart_detail.html')


def checkout(request):
	amount_str = request.POST.get('amount')
	amount_float = (float(amount_str))
	amount = int(amount_float)
	payment = client.order.create({
		"amount":amount*100,
		"currency":'INR',
		'payment_capture':'1'
	})

	print(payment)
	order_id = payment['id']
	context ={
		'amount': amount,
		'order_id': order_id,
		'payment': payment,
	}
	return render(request, 'cart/checkout.html',context)

def placeorder(request):
	if request.method == "POST":
		uid = request.session.get('_auth_user_id')
		user = User.objects.get(id=uid)
		
		order_id = request.POST.get('order_id')
		cart = request.session.get('cart')
		print(cart)
		email = request.POST.get('email')
		address = request.POST.get('address')
		pincode = request.POST.get('pincode')
		phone = request.POST.get('phone')
		amount = request.POST.get('amount')

		context = {
			'order_id' : order_id,
		}

		order = Order(
			user = user, 
			payment_id = order_id,
			email = email,
			address = address,
			pincode = pincode,
			phone = phone,
			amount = amount,
		)

		order.save()

		for i in cart:
			a=(int(cart[i]['price']))
			b=cart[i]['quantity']


			total= a * b
			

			item = OrderItem(
				order=order,
				product = cart[i]['name'],
				image=cart[i]['image'],
				quantity= cart[i]['quantity'],
				price= cart[i]['price'],
				total=total

			)

			item.save()

	
		return render(request, 'cart/placeorder.html', context)

@csrf_exempt
def success(request):
	if request.method == "POST":
		a = request.POST
		order_id = ""
		for key, val in a.items():
			if key == 'razorpay_order_id':
				order_id =val
				break
		user = Order.objects.filter(payment_id=order_id).first()
		user.paid=True
		user.save()
		request.session['cart'] = {}
	return render(request, 'cart/thankyou.html')

@login_required
def my_order(request):
    user = request.user
    orders = Order.objects.filter(user=user)
    order_items = OrderItem.objects.filter(order__in=orders)
    total_amount = order_items.aggregate(Sum('price'))['price__sum']

    context = {
        'orders': orders,
        'order_items': order_items,
        'total_amount': total_amount,
		
    }
    return render(request, 'cart/my_order.html', context)

def Product_page(request):
	category=Category.objects.all()
	age = Age.objects.all()
	brand = Brand.objects.all()

	categoryID=request.GET.get('category')
	AgeID = request.GET.get('age')
	brandID = request.GET.get('brand')
	if categoryID:
		product = Product.objects.filter(sub_category=categoryID)
	elif AgeID:
		product=Product.objects.filter(age_no=AgeID)
	elif brandID:
		product=Product.objects.filter(brand=brandID)
	else:
		product = Product.objects.all()

	context ={
		'category' : category,
		'age'  : age,
		'brand' : brand,
		'product' : product,
	}
	return render(request, 'product.html', context)

def product_detail(request,id):
	category=Category.objects.all()
	age = Age.objects.all()
	brand = Brand.objects.all()
	product = Product.objects.filter(id = id).first()
	context = {
		'category' : category,
		'age'  : age,
		'brand' : brand,
		'product': product,
	}
	return render(request, 'product_detail.html',context)

def Search(request):
	
	query = request.GET['query']
	product = Product.objects.filter(name__icontains = query)
	context ={
		'product':product,
	}
	return render(request, 'search.html',context)




