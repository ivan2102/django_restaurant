from django.http import HttpResponse, JsonResponse
import simplejson as json
from django.shortcuts import redirect, render
from marketplace.models import Tax
from menu.models import ProductFood
from orders.models import OrderedFood
from orders.models import Payment
from orders.models import Order
from orders.forms import OrderForm
from .utils import generate_order_number
from accounts.utils import send_notification
from django.contrib.auth.decorators import login_required

from marketplace.models import FoodCart
from marketplace.context_processors import cart_total_amount

# Create your views here.

def place_order(request):

    cart_items = FoodCart.objects.filter(user=request.user).order_by('created_at')
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('marketplace')
    
    vendors_id = []
    for item in cart_items:
       if item.fooditem.vendor.id not in vendors_id:
        vendors_id.append(item.fooditem.vendor.id)
        
        subtotal = 0
        list = {}
        get_tax = Tax.objects.filter(is_active=True)
        total_data = {}
        

        for i in cart_items:
           fooditem = ProductFood.objects.get(pk=i.fooditem.id, vendor_id__in=vendors_id)
           vendor_id = fooditem.vendor.id
           if vendor_id in list:

            subtotal = list[vendor_id]
            subtotal += (fooditem.price * item.quantity)
            list[vendor_id] = subtotal
        else:
           subtotal = (fooditem.price * item.quantity)
           list[vendor_id] = subtotal

           # Calculate the tax_data
           tax_dict = {}
           for i in get_tax:
              tax_type = i.tax_type
              tax_percentage = i.tax_percentage

              tax_amount = round((tax_percentage * subtotal)/ 100, 2)
              tax_dict.update({tax_type: {str(tax_percentage) : str(tax_amount)}})

              total_data.update({fooditem.vendor.id: {str(subtotal): str(tax_dict)}})

             

    
        subtotal = cart_total_amount(request)['subtotal']
        tax = cart_total_amount(request)['tax']
        total = cart_total_amount(request)['total']
        tax_data = cart_total_amount(request)['tax_dict']
    
 
   

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = Order()
            order.first_name = form.cleaned_data['first_name']
            order.last_name = form.cleaned_data['last_name']
            order.email = form.cleaned_data['email']
            order.address = form.cleaned_data['address']
            order.country = form.cleaned_data['country']
            order.state = form.cleaned_data['state']
            order.pin_code = form.cleaned_data['pin_code']
            order.city = form.cleaned_data['city']
            order.user = request.user
            order.total = total
            order.tax = tax
            order.tax_data = json.dumps(tax_data)
            order.total_data = json.dumps(total_data)
            order.payment_method = request.POST['payment_method']
            order.save()
            order.order_number = generate_order_number(order.id)
            order.vendors.add(*vendors_id)
            order.save()
            context = {
                
                'order': order,
                'cart_items': cart_items
            }
            return render(request, 'orders/place_order.html', context)

        else:
            print(form.errors)
    return render(request, 'orders/place_order.html')


#Payments

def payments(request):
    # Check if the request is ajax
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == 'POST':
    # Store the payment details in the payment model
     order_number = request.POST.get('order_number')
     transaction_id = request.POST.get('transaction_id')
     status = request.POST.get('status')
     payment_method = request.POST.get('payment_method')

     order = Order.objects.get(user=request.user, order_number=order_number)
     payment = Payment(
         
         user = request.user,
         transaction_id = transaction_id,
         status = status,
         payment_method = payment_method,
         amount = order.total
     )
     payment.save()
    # Update the order model
    order.payment = payment
    order.is_ordered = True
    order.save()
  
    # Move the cart items to ordered food model
    cart_items = FoodCart.objects.filter(user=request.user)
    for item in cart_items:

        ordered_food = OrderedFood()

        ordered_food.order = order
        ordered_food.payment = payment
        ordered_food.user = request.user
        ordered_food.fooditem = item.fooditem
        ordered_food.quantity = item.quantity
        ordered_food.price = item.fooditem.price
        ordered_food.amount = item.fooditem.price * item.quantity # total amount
        ordered_food.save()
        


    # Send the order confirmation mail to the customer
    mail_subject = 'Order complete! Thank you so much for choosing us!'
    mail_template = 'orders/order_confirmation_email.html'
    context = {

        'user': request.user,
        'order': order,
        'to_email': order.email
    }
    send_notification(mail_subject, mail_template, context)
   
    
    # Send order received email to the vendor
    mail_subject = 'You have received a new order'
    mail_template = 'orders/order_received.html'
    to_emails = []
    for item in cart_items:
     if item.fooditem.vendor.user.email not in to_emails:
      to_emails.append(item.fooditem.vendor.user.email)
     context = {

       'order': order,
       'to_email': to_emails
     }
     send_notification(mail_subject, mail_template, context)
    
    # Clear the cart if the payment is success
   # cart_items.delete()
    # Return back to ajax with the status success or failure
     response = {
        'order_number': order_number,
        'transaction_id': transaction_id,
        }
     return JsonResponse(response)
    return HttpResponse('Payments view')


    

   
def order_complete(request):
    order_number = request.GET.get('order_number')
    transaction_id = request.GET.get('transaction_id')

    try:
       order = Order.objects.get(order_number=order_number, payment__transaction_id=transaction_id, is_ordered=True)
       ordered_food = OrderedFood.objects.filter(order=order)

       subtotal = 0
       for item in ordered_food:
          subtotal += (item.price * item.quantity)

          tax_data = json.loads(order.tax_data)


       context = {
          
          'order': order,
          'ordered_food': ordered_food,
          'subtotal': subtotal,
          'tax_data': tax_data
       }

       return render(request, 'orders/order_complete.html', context)
    except:
       return redirect('home')
    
   