from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from . models import *
from .forms import OrderForm, CreateUserForm
from . filters import OrderFilter

# Create your views here.
def register_page(request):
	form = CreateUserForm()
	if request.method=='POST':
		form = CreateUserForm(request.POST)
		if form.is_valid():
			form.save()
			user = form.cleaned_data.get('username')
			messages.success(request, 'account successfully created for: '+ user)
			return redirect('login')
	cntx = {'form':form}
	return render(request, 'accounts/register.html', cntx)


def login_page(request):

	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			return redirect('home')
		else:
			messages.info(request,'Either Password or Username is Incorrect')
	cntx = {}
	return render(request, 'accounts/login.html', cntx)


def logout_page(request):
	logout(request)
	return render(request, 'accounts/login.html')

@login_required(login_url='login')
def home(request):
	orders = Order.objects.all()
	customers = Customer.objects.all()
	order_count = orders.count()
	delivered = orders.filter(status='Delivered').count()
	pending = orders.filter(status = 'pending').count()

def userPage(request):
	context = {}
	return render(request, 'account/users.html', context)


	cntx = {'delivered':delivered, 'orders':orders,
	 'customers':customers, 'order_count':order_count,
	 'pending':pending,}

	return render(request, 'accounts/dashboard.html',cntx)

@login_required(login_url='login')
def products(request):
	product = Product.objects.all()
	cntx = {'products':product}
	return render(request, 'accounts/products.html',cntx)

@login_required(login_url='login')
def customer(request, pk):
	customer = Customer.objects.get(id=pk)
	orders = customer.order_set.all()
	total_orders = orders.count()
	myFilter = OrderFilter(request.GET, queryset=orders)
	orders=myFilter.qs
	cntx = {'customer':customer, 'orders':orders, 'total_orders':total_orders, 'myfilter':myFilter}
	return render(request, 'accounts/customer.html', cntx)

@login_required(login_url='login')
def create_order(request, pk):
	OrderFormSet = inlineformset_factory(Customer, Order, extra=5, fields=('product', 'status'))
	customer = Customer.objects.get(id=pk)
	formset = OrderFormSet(queryset=Order.objects.none(),instance=customer)
	if request.method=='POST':
		formset = OrderFormSet(request.POST, instance=customer)
		if formset.is_valid():
			formset.save()
			return redirect('/')
	cntx = {'formset':formset}
	return render(request, 'accounts/order_form.html', cntx)

@login_required(login_url='login')
def update_order(request, pk):
	order= Order.objects.get(id=pk)
	form = OrderForm(instance=order)
	if request.method=='POST':
		form = OrderForm(request.POST, instance=order)
		if form.is_valid():
			form.save()
			return redirect('/')

	cntx = {'form':form}
	return render(request, 'accounts/order_form.html', cntx)

@login_required(login_url='login')
def delete_order(request, pk):
	order= Order.objects.get(id=pk)
	cntx = {'order':order}
	if request.method=='POST':
		order.delete()
		return redirect("/")
	return render(request, 'accounts/delete_order_form.html',cntx)