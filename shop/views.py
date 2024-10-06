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

def home(request):
    if request.user.is_anonymous:
          return redirect('login/')
    messages.success(request, 'Welcome!')
    return render(request, 'home.html')

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
        name=request.POST.get('name')
        email=request.POST.get('email')
        phone=request.POST.get('phone')
        desc=request.POST.get('desc')
        contact=Contact(name=name,email=email,phone=phone,desc=desc,date=datetime.today())
        contact.save()
        messages.success(request, "YOUR MESSAGE HAS BEEN SENT.")
    return redirect(about)

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

    return JsonResponse({'message': 'Cart items saved successfully'})

   