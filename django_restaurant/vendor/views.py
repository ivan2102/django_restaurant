from django.shortcuts import get_object_or_404, render, redirect
from .forms import VendorForm
from menu.forms import CategoryForm, ProductFoodForm
from accounts.forms import UserProfileForm
from accounts.models import UserProfile
from .models import Vendor
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
        category.slug = slugify(category_name)
        form.save()
        messages.success(request, 'Category added successfully')
        return redirect('menu_builder')
     
     else:
        print(form.errors)
    else:
        form = CategoryForm()
        context = {
           'form': form
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