from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
from django.http import JsonResponse
from shop.form import CustomUserForm
from django.contrib.auth import authenticate, login, logout
import json


# Home page
def home(request):
    products = Product.objects.filter(trending=1)
    return render(request, "shop/index.html", {'products': products})

#favviewimage
def favviewimage(request):
     if request.user.is_authenticated:
         fav=Favourite.objects.filter(user=request.user)
         return render(request,'shop/fav.html',{'fav':fav})
     else:
      return redirect("/")
 
def reomve_cart(request,cid):
    item=Favourite.objects.get(id=cid)
    item.delete()
    return redirect("/favviewpage")
      

def fav_page(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        if request.user.is_authenticated:
            try:
                data = json.loads(request.body)
                product_id = data.get('pid')
                product_status = Product.objects.filter(id=product_id).first()
                
                if product_status:
                    if Favourite.objects.filter(user=request.user, product_id=product_id).exists():
                        return JsonResponse({'status': 'Product Already in favourite'}, status=200)
                    else:
                        Favourite.objects.create(user=request.user, product_id=product_id)
                        return JsonResponse({'status': 'Product added to favourite'}, status=200)
                else:
                    return JsonResponse({'status': 'Product not found'}, status=404)
            except Exception as e:
                return JsonResponse({'status': f'Error: {str(e)}'}, status=500)
        else:
            return JsonResponse({'status': 'Login to Add favourite'}, status=200)
    else:
        return JsonResponse({'status': 'Invalid Access'}, status=400)



# cart
def add_to_cart(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        if request.user.is_authenticated:
            try:
                data = json.loads(request.body)  
                product_qty = data['product_qty']
                product_id = data['pid']
                
                product_status = Product.objects.get(id=product_id)
                if product_status:
                    if Cart.objects.filter(user=request.user, product_id=product_id).exists():
                        return JsonResponse({'status': 'Product Already in Cart'}, status=200)
                    else:
                        Cart.objects.create(
                            user=request.user,
                            product_id=product_id,
                            product_qty=product_qty
                        )
                        return JsonResponse({'status': 'Product Added to Cart'}, status=200)
            except Exception as e:
                return JsonResponse({'status': f'Error: {str(e)}'}, status=500)
        else:
            return JsonResponse({'status': 'Login to Add Cart'}, status=200)
    return JsonResponse({'status': 'Invalid Access'}, status=400)

def delete_cart_item(request):
    if request.method == "POST" and request.user.is_authenticated:
        data = json.loads(request.body)
        product_id = data.get('pid')

        Cart.objects.filter(user=request.user, product_id=product_id).delete()

        return JsonResponse({'status': 'Deleted'})
    return JsonResponse({'status': 'Error'}, status=400)


# cart page
def cart_page(request):
     if request.user.is_authenticated:
         cart=Cart.objects.filter(user=request.user)
         return render(request,'shop/cart.html',{'cart':cart})
     else:
      return redirect("/")

# Logout Page
def logout_page(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "Logged out Successfully")
    return redirect("/")


# Login Page
def login_page(request):
    if request.user.is_authenticated:
        return redirect("/")
    else:
        if request.method == "POST":
            name = request.POST.get('username')
            pwd = request.POST.get('password')
            user = authenticate(request, username=name, password=pwd)

            if user is not None:
                login(request, user)
                messages.success(request, "Logged in Successfully")
                return redirect("/")
            else:
                messages.error(request, "Invalid User Name or Password")
                return redirect("/login")

        return render(request, "shop/login.html")


# Register page
def register(request):
    if request.method == "POST":   # ✅ must be uppercase POST
        form = CustomUserForm(request.POST)   # ✅ request.POST not request.post
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful! You can login now.")
            return redirect("login")   # ✅ use URL name instead of hardcoding
    else:
        form = CustomUserForm()   # ✅ show empty form on GET
    return render(request, "shop/register.html", {"form": form})


# Category list
def collections(request):
    catagory = Catagory.objects.filter(status=0)
    return render(request, 'shop/collection.html', {'catagory': catagory})


# Products under a category
def collectionsview(request, name):
    if Catagory.objects.filter(name=name, status=0).exists():
        products = Product.objects.filter(catagory__name=name, status=0)
        return render(request, 'shop/products/index.html', {'products': products, 'catagory_name': name})
    else:
        messages.warning(request, "No such category found")
        return redirect('collections')


# Product details page
def product_details(request, cname, pname):
    if Catagory.objects.filter(name=cname, status=0).exists():
        if Product.objects.filter(name=pname, catagory__name=cname, status=0).exists():
            product = Product.objects.get(name=pname, catagory__name=cname, status=0)
            return render(request, 'shop/products/product_details.html', {'product': product})
        else:
            messages.error(request, 'No such product found')
            return redirect('collections')
    else:
        messages.error(request, 'No such category found')
        return redirect('collections')
