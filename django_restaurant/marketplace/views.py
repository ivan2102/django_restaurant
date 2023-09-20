from datetime import date, datetime
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from accounts.models import UserProfile
from orders.forms import OrderForm
from marketplace.context_processors import cart_counter, cart_total_amount
from vendor.models import Vendor, OpeningHours
from menu.models import Category, ProductFood
from django.db.models import Prefetch
from marketplace.models import FoodCart
from django.contrib.auth.decorators import login_required
from django.db.models import Q

# Create your views here.
def marketplace(request):
    vendors = Vendor.objects.filter(is_approved=True, user__is_active=True)
    vendor_count = vendors.count()
    context = {

        'vendors': vendors,
        'vendor_count': vendor_count
    }
    return render(request, 'marketplace/vendor_list.html', context)


def vendor_details(request, vendor_slug):
    vendor = get_object_or_404(Vendor, vendor_slug=vendor_slug)
    categories = Category.objects.filter(vendor=vendor).prefetch_related(

        Prefetch(
        
        'productfoods',
        queryset= ProductFood.objects.filter(is_available=True)
        )
    )

    opening_hours = OpeningHours.objects.filter(vendor=vendor).order_by('day', '-from_hour')

    #Check today opening hours
    today_day = date.today()
    today = today_day.isoweekday()
    today_opening_hours = OpeningHours.objects.filter(vendor=vendor, day=today)

   

    if request.user.is_authenticated:
      cart_items = FoodCart.objects.filter(user=request.user)


    else:
      cart_items = None

    context = {

        'vendor': vendor,
        'categories': categories,
        'cart_items': cart_items,
        'opening_hours': opening_hours,
        'today_opening_hours': today_opening_hours,
        
    }
    return render(request, 'marketplace/vendor_details.html', context)


def add_to_cart(request, food_id):

    if request.user.is_authenticated:
     if request.headers.get('x-requested-with') == 'XMLHttpRequest':
      try:

        fooditem = ProductFood.objects.get(id=food_id)

        #Check if the user already added to the cart
        try:
          
          cart = FoodCart.objects.get(user=request.user, fooditem=fooditem)
          #Increase cart quantity
          cart.quantity += 1
          cart.save()
          return JsonResponse({'status': 'Success', 'message': 'Increased successfully', 'cart_counter': cart_counter(request), 'qty': cart.quantity, 'cart_amount': cart_total_amount(request)})
        
        except:
          
          cart = FoodCart.objects.create(user=request.user, fooditem=fooditem, quantity=1)
          return JsonResponse({'status': 'Success', 'message': 'Product food added successfully', 'cart_counter': cart_counter(request), 'qty': cart.quantity, 'cart_amount': cart_total_amount(request)})
        
      except:

         return JsonResponse({'status': 'Failed', 'message': 'This food item does not exist'})
     else:
      return JsonResponse({'status': 'Failed', 'message': 'Invalid request!'})
    
    else:
     return JsonResponse({'status': 'login_required', 'message': 'Please log in!'})
    

def decrease_cart(request, food_id):

    if request.user.is_authenticated:
     if request.headers.get('x-requested-with') == 'XMLHttpRequest':
      try:

        fooditem = ProductFood.objects.get(id=food_id)

        #Check if the user already added to the cart
        try:
          
          cart = FoodCart.objects.get(user=request.user, fooditem=fooditem)
          #Decrease cart quantity
          if cart.quantity > 1:
            cart.quantity -= 1
            cart.save()

          else:
            cart.delete()
            cart.quantity = 0
          return JsonResponse({'status': 'Success',  'cart_counter': cart_counter(request), 'qty': cart.quantity, 'cart_amount': cart_total_amount(request)})
        
        except:
          
          return JsonResponse({'status': 'Failed', 'message': 'You do not have this item in your cart'})
        
      except:

         return JsonResponse({'status': 'Failed', 'message': 'This food item does not exist'})
     else:
      return JsonResponse({'status': 'Failed', 'message': 'Invalid request!'})
    
    else:
      return JsonResponse({'status': 'login_required', 'message': 'Please log in!'})
    

@login_required(login_url = 'login')
def cart(request):
  cart_items = FoodCart.objects.filter(user=request.user).order_by('created_at')
  context = {

    'cart_items': cart_items
  }
  return render(request, 'marketplace/cart.html', context)


def delete_cart(request, cart_id):
  if request.user.is_authenticated:
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
      try:
        #Check if cart item exist
        cart_item = FoodCart.objects.get(user=request.user, id=cart_id)

        if cart_item:
          cart_item.delete()
          return JsonResponse({'status': 'Success', 'message': 'Cart Item has been deleted successfully!', 'cart_counter': cart_counter(request), 'cart_amount': cart_total_amount(request)})
        
      except:
        return JsonResponse({'status': 'Failed', 'message': 'Cart Item does not exist'})

    else:
      return JsonResponse({'status': 'Failed', 'message': 'Invalid request!'})
    


def search(request):
  keyword = request.GET['keyword']

  

  #vendor id with that food item
  food_items = ProductFood.objects.filter(food_title__icontains=keyword, is_available=True).values_list('vendor', flat=True)

  vendors = Vendor.objects.filter(Q(id__in=food_items) | Q(vendor_name__icontains=keyword, is_approved=True, user__is_active=True))
  vendor_count = vendors.count()


  context = {

    'vendors': vendors,
    'vendor_count': vendor_count
  }
  return render(request, 'marketplace/vendor_list.html', context)



#checkout
@login_required(login_url='login')
def checkout(request):

  cart_items = FoodCart.objects.filter(user=request.user).order_by('created_at')
  cart_count = cart_items.count()
  if cart_count <= 0:
    return redirect ('marketplace')

  user_profile = UserProfile.objects.get(user=request.user)
  default_values = {

    'first_name': request.user.first_name,
    'last_name': request.user.last_name,
    'email': request.user.email,
    'address': user_profile.address,
    'country': user_profile.country,
    'state': user_profile.state,
    'city': user_profile.city,
    'pin_code': user_profile.pin_code
  }
  form = OrderForm(initial=default_values)

  context = {

    'form': form,
    'cart_items': cart_items
  }
  return render(request, 'marketplace/checkout.html', context)

   
   
    
  

         
 