from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.http import JsonResponse
from .models import *
import json
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .forms import ReviewForm
# Create your views here.

def detail(request):
    categories = Category.objects.filter(is_sub = False)
    if request.user.is_authenticated:
        customer = request.user
        order, create = Order.objects.get_or_create(customer = customer, complete=False)
        items=order.orderitem_set.all()
        cartItems = order.get_cart_items
        user_not_login = "hidden"
        user_login = 'show'
    else:
        items =[]
        order={'get_cart_items':0, 'get_cart_total':0}
        cartItems = order['get_cart_items']
        user_not_login = "show"
        user_login = 'hidden'
    id = request.GET.get('id','')
    products = Product.objects.filter(id=id)
    reviews = ReviewRating.objects.filter(product_id__in=products.values_list('id', flat=True), status=True)
    context={'products':products,'items':items,'order':order,'cartItems':cartItems,'user_not_login':user_not_login,'user_login': user_login,'categories': categories,'reviews': reviews,}
    return render(request, 'app/detail.html',context)
def category(request):
    categories = Category.objects.filter(is_sub = False)
    active_category = request.GET.get('category','')
    if active_category:
        products = Product.objects.filter(category__slug = active_category)
    if request.user.is_authenticated:
        user_not_login = "hidden"
        user_login = 'show'
    else:
        user_not_login = "show"
        user_login = 'hidden'
    context = {'categories': categories, 'products': products,'active_category': active_category,'user_not_login':user_not_login,'user_login': user_login}
    return render(request, 'app/category.html',context)
def search(request):
    if request.method == "POST":
        searched = request.POST["searched"]
        keys = Product.objects.filter(name__contains = searched)
    if request.user.is_authenticated:
        customer = request.user
        order, create = Order.objects.get_or_create(customer = customer, complete=False)
        items=order.orderitem_set.all()
        cartItems = order.get_cart_items
        user_not_login = "hidden"
        user_login = 'show'
    else:
        items =[]
        order={'get_cart_items':0, 'get_cart_total':0}
        cartItems = order['get_cart_items']
        user_not_login = "show"
        user_login = 'hidden'
    products = Product.objects.all()
    context={'products': products,'cartItems':cartItems}
    return render(request, 'app/search.html',{"searched": searched,"keys": keys,'products': products,'cartItems':cartItems,'user_not_login':user_not_login,'user_login': user_login})
def register(request):
    
    form = CreateUserForm()
    user_not_login = "show"
    user_login = 'hidden'
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('login')
    
    context= {'form':form,'user_not_login':user_not_login,'user_login': user_login}
    return render(request, 'app/register.html',context)
def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        user_not_login = "show"
        user_login = 'hidden'
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username =username, password =password)
        
        if user is not None:
            login(request,user)
            return redirect('home')
        else: messages.info(request, 'user or password are not correct!')
    context= {'user_not_login':user_not_login,'user_login': user_login}
    return render(request, 'app/login.html',context)
def logoutPage(request):
    logout(request)
    return redirect('login')
def home(request):
    if request.user.is_authenticated:
        customer = request.user
        order, create = Order.objects.get_or_create(customer = customer, complete=False)
        items=order.orderitem_set.all()
        cartItems = order.get_cart_items
        user_not_login = "hidden"
        user_login = 'show'
    else:
        items =[]
        order={'get_cart_items':0, 'get_cart_total':0}
        cartItems = order['get_cart_items']
        user_not_login = "show"
        user_login = 'hidden'
    categories = Category.objects.filter(is_sub = False)
    products = Product.objects.all()
    
    context={'categories': categories,'products': products,'cartItems':cartItems,'user_not_login':user_not_login,'user_login': user_login}
    return render(request, 'app/home.html',context)
def cart(request):
    categories = Category.objects.filter(is_sub = False)
    if request.user.is_authenticated:
        customer = request.user
        order, create = Order.objects.get_or_create(customer = customer, complete=False)
        items=order.orderitem_set.all()
        cartItems = order.get_cart_items
        user_not_login = "hidden"
        user_login = 'show'
    else:
        items =[]
        order={'get_cart_items':0, 'get_cart_total':0}
        cartItems = order['get_cart_items']
        user_not_login = "show"
        user_login = 'hidden'
    context={'items':items,'order':order,'cartItems':cartItems,'user_not_login':user_not_login,'user_login': user_login,'categories': categories}
    return render(request, 'app/cart.html',context)
def checkout(request):
    categories = Category.objects.filter(is_sub = False)
    if request.user.is_authenticated:
        customer = request.user
        order, create = Order.objects.get_or_create(customer = customer, complete=False)
        items=order.orderitem_set.all()
        cartItems = order.get_cart_items
        user_not_login = "hidden"
        user_login = 'show'
    else:
        items =[]
        order={'get_cart_items':0, 'get_cart_total':0}
        cartItems = order['get_cart_items']
        user_not_login = "show"
        user_login = 'hidden'
    context={'items':items,'order':order,'cartItems':cartItems,'user_not_login':user_not_login,'user_login': user_login,'categories': categories}
    return render(request, 'app/checkout.html',context)
def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    customer = request.user
    product = Product.objects.get(id = productId)
    order, create = Order.objects.get_or_create(customer = customer, complete=False)
    orderItem, create = OrderItem.objects.get_or_create(order = order,product = product)
    if action == 'add':
        orderItem.quantity +=1
    elif action == 'remove':
        orderItem.quantity -=1
    orderItem.save()
    if orderItem.quantity<=0:
        orderItem.delete()
    
    return JsonResponse('added',safe=False)

def submit_review(request, product_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        try:
            reviews = ReviewRating.objects.get(user__id=request.user.id, product__id=product_id)
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            messages.success(request, 'Thank you! Your review has been updated.')
            return redirect(url)
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                messages.success(request, 'Thank you! Your review has been submitted.')
                return redirect(url)