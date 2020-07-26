from django.shortcuts import render,redirect    
from django.http import HttpResponse
from .models import *
from django.contrib.auth.models import Group
from .forms import *
from django.contrib import messages
from django.forms import inlineformset_factory
from django.contrib.auth import authenticate,login,logout
from .filters import *
from django.contrib.auth.decorators import login_required
from .decoraters import *
# Create your views here.

@login_required(login_url='login')
@admin_only
def Home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()
    total_customers = customers.count()
    total_orders=orders.count() 

    delivered = orders.filter(status = 'Delivered').count()
    pending = orders.filter(status = 'Pending').count()
    context ={
        'orders':orders,
        'customers':customers,
        'delivered':delivered,
        'pending':pending,
        'total_customers':total_customers,        
        'total_orders':total_orders,
    }
    return render(request,'accounts/dashboard.html',context)
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def Products(request):
    products = Product.objects.all()
    return render(request,'accounts/Products.html',{'products':products})

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def Customers(request,pk_test):
    customer = Customer.objects.get(id=pk_test)
    orders = customer.order_set.all()
    order_count = orders.count()

    myFilter = OrderFilter(request.GET,queryset=orders)
    orders = myFilter.qs
    context = {'customer':customer,'orders':orders,'order_count':order_count,'myFilter':myFilter}
    return render(request,'accounts/customers.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def CreateOrder(request,pk):
    OrderFormSet = inlineformset_factory(Customer,Order,fields=('product','status'),extra=4)
    customer = Customer.objects.get(id=pk)
    formset = OrderFormSet(queryset=Order.objects.none(),instance=customer)
    if request.method == 'POST':
        formset = OrderFormSet(request.POST,instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')

    context={'form':formset}
    return render(request,'accounts/order_form.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def UpdateOrder(request,pk):
    order = Order.objects.get(id=pk)
    form = Order_form(instance=order)
    if request.method == 'POST':
        form = Order_form(request.POST,instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')

    context={'form':form}
    return render(request,'accounts/order_form.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def DeleteOrder(request,pk):
    item = Order.objects.get(id=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('/')
    context={'item':item}
    return render(request,'accounts/delete.html',context)


@unauthenticated_user
def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request,username=username,password=password)

        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.info(request,'Username or Password is Invalid')

    context = {}
    return render(request,"accounts/login.html",context)

@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    return redirect("login")

@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            messages.success(request,'Account was created for '+username)

            return redirect('login')
    context = {'form':form}
    return render(request,"accounts/register.html",context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userPage(request):
    orders = request.user.customer.order_set.all()
    delivered = orders.filter(status = 'Delivered').count()
    pending = orders.filter(status = 'Pending').count()
    total_orders = orders.count()
    context = { 'orders':orders,
                'delivered':delivered,
                'pending':pending,
                'total_orders':total_orders,
    }
    return render(request, 'accounts/user.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def accountSettings(request):
	customer = request.user.customer
	form = CustomerForm(instance=customer)

	if request.method == 'POST':
		form = CustomerForm(request.POST, request.FILES,instance=customer)
		if form.is_valid():
			form.save()


	context = {'form':form}
	return render(request, 'accounts/account_settings.html', context)
