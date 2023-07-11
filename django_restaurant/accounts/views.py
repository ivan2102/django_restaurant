from django.shortcuts import redirect, render
from .forms import UserForm
from vendor.forms import VendorForm
from .models import User, UserProfile
from django.contrib import messages, auth
from .utils import detectUser, send_verification_email
from base64 import urlsafe_b64decode
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied

# Restrict the vendor from accessing the customer page
def check_role_vendor(user):
  if user.role == 1:
    return True
  else:
    raise PermissionDenied
  
# Restrict the customer from accessing the vendor page
def check_role_customer(user):
  if user.role == 2:
    return True
  else:
    raise PermissionDenied
  



#Register user
def registerUser(request):

  if request.user.is_authenticated:
    messages.warning(request, 'You are already logged in.')
    return redirect('myAccount')

  elif request.method == 'POST':

    form = UserForm(request.POST)
    if form.is_valid():

      first_name = form.cleaned_data['first_name']
      last_name = form.cleaned_data['last_name']
      username = form.cleaned_data['username']
      email = form.cleaned_data['email']
      password = form.cleaned_data['password']
      user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
      user.role = User.CUSTOMER
      user.save()

      send_verification_email(request, user)
      messages.success(request, 'User created successfully.')
      return redirect('registerUser')
    
    else:
      print('Invalid form data')
      print(form.errors)

  else:
     form = UserForm()
  context = {
       'form': form,
    }

  return render(request, 'accounts/registerUser.html', context)

def registerVendor(request):
     
     if request.user.is_authenticated:
       messages.warning(request, 'You are already registered')
       return redirect('dashboard')
     
     elif request.method == 'POST':

      form = UserForm(request.POST)
      vendor_form = VendorForm(request.POST, request.FILES)

      if form.is_valid() and vendor_form.is_valid():
       first_name = form.cleaned_data['first_name']
       last_name = form.cleaned_data['last_name']
       username = form.cleaned_data['username']
       email = form.cleaned_data['email']
       password = form.cleaned_data['password']
       user = User.objects.create_user(first_name, last_name=last_name, username=username, email=email, password=password)
       user.role = User.VENDOR
       user.save()
       vendor = vendor_form.save(commit=False)
       vendor.user = user
       user_profile = UserProfile.objects.get(user=user)
       vendor.user_profile = user_profile
       vendor.save()

       # Send verification email
       send_verification_email(request, user)
       messages.success(request, 'Your vendor has been registered successfully')
       return redirect('registerVendor')


      else:
       print('Invalid form data')
       print(form.errors)

     else:
       form = UserForm()
       vendor_form = VendorForm()

       context = {

         'form': form,
         'vendor_form': vendor_form
       }

       return render(request, 'accounts/registerVendor.html', context)
     

def activate(request, uidb64, token):
  
  try:
    uid = urlsafe_b64decode(uidb64).decode()
    user = User._default_manager.get(pk=uid)

  except(TypeError, ValueError, OverflowError, User.DoesNotExist):
    user = None

    if user is not None and default_token_generator.check_token(user, token):
      user.is_active = True
      user.save()
      messages.success(request, 'Congrats you have activated your account')
      return redirect('myAccount')
    else:
      messages.error(request, 'Invalid activation link')
      return redirect('myAccount')


     
def login(request):
  if request.user.is_authenticated:
    messages.warning(request, 'You are already logged in')
    return redirect('myAccount')
  
  elif request.method == 'POST':
    email = request.POST['email']
    password = request.POST['password']

    user = auth.authenticate(email=email, password=password)
    if user is not None:
      auth.login(request, user)
      messages.success(request, 'You are logged in successfully')
      return redirect('myAccount')
    else:
      messages.error(request, 'Invalid email or password')
      return redirect('login')
  return render(request, 'accounts/login.html')

def logout(request):
  auth.logout(request)
  messages.info(request, 'You are logged out successfully')
  return redirect('login')

@login_required(login_url = 'login')
def myAccount(request):
  user = request.user
  redirectUrl = detectUser(user)
  return redirect(redirectUrl)

@login_required(login_url = 'login')
@user_passes_test(check_role_customer)    
def customerDashboard(request):
  return render(request, 'accounts/customerDashboard.html')

@login_required(login_url = 'login')
@user_passes_test(check_role_vendor)
def vendorDashboard(request):
  return render(request, 'accounts/vendorDashboard.html')
