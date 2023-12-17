from time import strftime
from django.db import IntegrityError
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from orders.models import OrderedFood

from orders.models import Order
from .forms import VendorForm, OpeningHoursForm
from menu.forms import CategoryForm, ProductFoodForm
from accounts.forms import UserProfileForm
from accounts.models import UserProfile
from .models import Vendor, OpeningHours
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.views import check_role_vendor
from menu.models import Category, ProductFood
from django.template.defaultfilters import slugify

def get_vendor(request):
    vendor = Vendor.objects.get(user=request.user)
    return vendor


# Create your views here.
@login_required(login_url = 'login')
@user_passes_test(check_role_vendor) 
def vendor_profile(request):

    profile = get_object_or_404(UserProfile, user=request.user)
    vendor = get_object_or_404(Vendor, user=request.user)

    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        vendor_form = VendorForm(request.POST, instance=vendor)

        if profile_form.is_valid() and vendor_form.is_valid():
            profile_form.save()
            vendor_form.save()
            messages.success(request, 'Restaurant Profile updated successfully')
            return redirect('vendor_profile')
        else:
            print(profile_form.errors)
            print(vendor_form.errors)

    else:

     profile_form = UserProfileForm(instance=profile)
     vendor_form = VendorForm(instance=vendor)

    context = {

        'profile_form': profile_form,
        'vendor_form': vendor_form,
        'profile': profile,
        'vendor': vendor
    }
    return render(request, 'vendor/vendorProfile.html', context)

@login_required(login_url = 'login')
@user_passes_test(check_role_vendor) 

def menu_builder(request):
    vendor = get_vendor(request)
    categories = Category.objects.filter(vendor=vendor).order_by('created_at')
    context = {
        'categories': categories
    }
    return render(request, 'vendor/menu_builder.html', context)


@login_required(login_url = 'login')
@user_passes_test(check_role_vendor)

def fooditems_by_category(request, pk=None):
    vendor = get_vendor(request)
    category = get_object_or_404(Category, pk=pk)
    fooditems = ProductFood.objects.filter(vendor=vendor, category=category)
    context = {
        'fooditems': fooditems,
        'category': category
    }
    return render(request, 'vendor/fooditems_by_category.html', context)

@login_required(login_url = 'login')
@user_passes_test(check_role_vendor) 

def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            category = form.save(commit=False)
            category.vendor = get_vendor(request)
            
            category.save() # here the category id will be generated
            category.slug = slugify(category_name)+ '-' +str(category.id) # chicken-15
            category.save()
            messages.success(request, 'Category added successfully!')
            return redirect('menu_builder')
        else:
            print(form.errors)

    else:
        form = CategoryForm()
    context = {
        'form': form,
    }
    return render(request, 'vendor/add_category.html', context)

@login_required(login_url = 'login')
@user_passes_test(check_role_vendor) 

def edit_category(request, pk=None):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
       form = CategoryForm(request.POST, instance=category)
       if form.is_valid():
          category_name = form.cleaned_data['category_name']
          category = form.save(commit=False)
          category.vendor = get_vendor(request)
          category.slug = slugify(category_name)
          form.save()
          messages.success(request, 'Category updated successfully')
          return redirect('menu_builder')
       
       else:
          print(form.errors)

    else:
     form = CategoryForm(instance=category)
     context = {
       
       'form': form,
       'category': category
    }
    return render(request, 'vendor/edit_category.html', context)

@login_required(login_url = 'login')
@user_passes_test(check_role_vendor) 

def delete_category(request, pk=None):
   category = get_object_or_404(Category, pk=pk)
   category.delete()
   messages.success(request, 'One Category deleted successfully')
   return redirect('menu_builder')


#FoodItem
@login_required(login_url = 'login')
@user_passes_test(check_role_vendor) 

def add_food(request):
   if request.method == 'POST':
      form = ProductFoodForm(request.POST, request.FILES)
      if form.is_valid():
         food_title = form.cleaned_data['food_title']
         food = form.save(commit=False)
         food.vendor = get_vendor(request)
         food.slug = slugify(food_title)
         form.save()
         messages.success(request, 'New Product Food added successfully')
         return redirect('fooditems_by_category', food.category.id)
      
      else:
         print(form.errors)

   else:
   
      form = ProductFoodForm()
      form.fields['category'].queryset = Category.objects.filter(vendor=get_vendor(request))

   context = {
      
      'form': form
   }
   return render(request, 'vendor/add_food.html', context)

@login_required(login_url = 'login')
@user_passes_test(check_role_vendor)

def edit_food(request, pk=None):
   food = get_object_or_404(ProductFood, pk=pk)
   if request.method == 'POST':
      form = ProductFoodForm(request.POST, request.FILES, instance=food)
      if form.is_valid():
         food_title = form.cleaned_data['food_title']
         food = form.save(commit=False)
         food.vendor = get_vendor(request)
         food.slug = slugify(food_title)
         form.save()
         messages.success(request, 'Food Item updated successfully')
         return redirect('fooditems_by_category', food.category.id)
      
      else:
         print(form.errors)
      

   else:
    form = ProductFoodForm(instance=food)
    form.fields['category'].queryset = Category.objects.filter(vendor=get_vendor(request))
    context = {
       
       'form': form,
       'food': food,
    }
         
   return render(request, 'vendor/edit_food.html', context)

@login_required(login_url = 'login')
@user_passes_test(check_role_vendor) 

def delete_food(request, pk=None):
   food = get_object_or_404(ProductFood, pk=pk)
   food.delete()
   messages.success(request, 'Your Food Item deleted successfully')
   return redirect('fooditems_by_category', food.category.id)



#opening hours
def opening_hours(request):
   opening_hours = OpeningHours.objects.filter(vendor=get_vendor(request))
   form = OpeningHoursForm()

   context = {

      'form': form,
      'opening_hours': opening_hours
   }
   return render(request, 'vendor/opening_hours.html', context)


def add_opening_hours(request):
   #send data and save to the database
   if request.user.is_authenticated:
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == 'POST':
       day = request.POST.get('day')
       from_hour = request.POST.get('from_hour')
       to_hour = request.POST.get('to_hour')
       is_closed = request.POST.get('is_closed')

       try:
          
          hour = OpeningHours.objects.create(vendor=get_vendor(request), day=day, from_hour=from_hour, to_hour=to_hour, is_closed=is_closed)
          if hour:
             day = OpeningHours.objects.get(id=hour.id)
             
             if day.is_closed:
                response = {'status': 'success', 'id': hour.id, 'day': day.get_day_display(), 'is_closed': 'Closed'}
             else:
                response = {'status': 'success', 'id': hour.id, 'day': day.get_day_display(), 'from_hour': hour.from_hour, 'to_hour': hour.to_hour}
          
          return JsonResponse(response)
       except IntegrityError as error:
          response = {'status': 'failed', 'message': from_hour + '-' + to_hour + 'already exists for this day'}
          return JsonResponse(response)
          
    else:
       HttpResponse('Invalid request')


def delete_opening_hours(request, pk=None):

   if request.user.is_authenticated:
      if request.headers.get('x-requested-with') == 'XMLHttpRequest':
         hour = get_object_or_404(OpeningHours, pk=pk)
         hour.delete()
   return JsonResponse({'status': 'success', 'id': pk})


# Order Details
def order_details(request, order_number):
   order = Order.objects.get(order_number=order_number, is_ordered=True)
   ordered_food = OrderedFood.objects.filter(order=order, fooditem__vendor=get_vendor(request))

   context = {

      'order': order,
      'ordered_food': ordered_food,
      'subtotal': order.vendor_total()['subtotal'],
      'tax_data': order.vendor_total()['tax_dict'],
      'grand_total': order.vendor_total()['grand_total']
   }
   return render(request, 'vendor/order_details.html', context)


def vendor_orders(request):
   vendor = Vendor.objects.get(user=request.user)
   orders = Order.objects.filter(vendors__in=[vendor.id], is_ordered=True).order_by('created_at')

   context = {

      'orders': orders,
   }
   return render(request, 'vendor/vendor_orders.html', context)
   

   