from .models import FoodCart
from menu.models import ProductFood


def cart_counter(request):
    cart_count = 0
    if request.user.is_authenticated:
    
      try:
        cart_items = FoodCart.objects.filter(user=request.user)
        if cart_items:
            for cart_item in cart_items:
             cart_count  += cart_item.quantity

        else:
            cart_count = 0

      except:
        cart_count = 0

    return dict(cart_count=cart_count)


def cart_total_amount(request):
   subtotal = 0
   tax = 0
   total = 0

   if request.user.is_authenticated:
      cart_items = FoodCart.objects.filter(user=request.user)
      for cart_item in cart_items:
         fooditem = ProductFood.objects.get(pk=cart_item.fooditem.id)
         subtotal += (fooditem.price * cart_item.quantity)
         total = subtotal + tax
         print(subtotal)
         print(total)
   return dict(subtotal=subtotal, tax=tax, total=total)