from django.shortcuts import render, get_object_or_404,redirect
from django.http import JsonResponse
from shop.models import  Contact,Cart
from datetime import datetime
from django.contrib import messages
from django.contrib.auth import authenticate,login
from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json
from .forms import ContactForm
from django.utils.timezone import now

def home(request):
    if request.user.is_anonymous:
          return redirect('login/')
    messages.success(request, 'Welcome!')
    reviews = Contact.objects.all()
    return render(request, 'home.html' , {'reviews': reviews})

def homeret():
     return redirect("home")

def about(request):
     return render(request, 'about.html')

def search(request):
     return render(request,'serach_res.html')

def products(request):
    if request.user.is_anonymous:
         return redirect('login')
    return render(request, 'products.html')


def item_detail(request):
    item_name = request.GET.get('name')  # Get the item name from query parameters
    
    context = {
        'item_name': item_name,
    }
    return render(request, 'itemdes.html',context)

def mycart(request):
    return render(request, 'mycart.html')

def add(request, product_id):
    product = get_object_or_404(product, id=product_id)
    # Try to find if the product is already in the cart
    cart_item, created = Cart.objects.get_or_create(product=product) # type: ignore

    if not created:
        cart_item.quantity += 1  # Update the quantity if already exists
    cart_item.save()

    return redirect('cart_view')

def loginUser(request):
    if request.method=="POST":
        username=request.POST.get("username")
        password=request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user is not None:
                 # A backend authenticated the credentials
                 login(request,user)
                 
                 return redirect('home')
    
        else:
                  # No backend authenticated the credentials
                  messages.error(request, 'Invalid username or password')
                  return render(request,'login.html')

        


    return render(request,'login.html')

def logoutUser(request):
    logout(request)
    return redirect("login") 


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            # Automatically save the data to the model, including the rating
            contact = form.save(commit=False)
            contact.date = now()
            contact.save()
            messages.success(request, "Your message has been sent.")
            return redirect('about') 
        else:
            messages.error(request, "There was an error with your form submission.")
    else:
        form = ContactForm()
    
    # Pass the form to the template for rendering
    return render(request, 'about', {'form': form})

def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')  # Change this to your home page
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


@csrf_exempt
@require_http_methods(['POST'])
def checkout(request):
    data = request.body
    cart_items = json.loads(data)

    for item in cart_items:
        cart = Cart(
            name=item['name'],
            description='',  # You may want to add a description field to your cart items
            price=item['price']
        )
        cart.save()

    messages.success(request, 'Checkout Completed Successfully !') 

    return  JsonResponse({'success': True, 'message': 'Checkout completed successfully'})

   