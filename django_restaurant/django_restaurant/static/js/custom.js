$(document).ready(function() {

    $('.add_to_cart').on('click', function(e) {

        e.preventDefault();
        food_id = $(this).attr('data-id')
        url = $(this).attr('data-url')
        data = {

            food_id: food_id
        }

        $.ajax({

            type: 'GET',
            url: url,
            data: data,
            success: function(response){

                if(response.status == 'login_required') {

                    Swal.fire(response.message, '', 'error').then(function() {

                        window.location = '/login';
                    })

                }if(response.status == 'Failed'){

                    Swal.fire(response.message, '', 'error')

                }else {

                    $('#cart-counter').html(response.cart_counter['cart_count'])
                    $('#qty-' +food_id).html(response.qty)

                    // cart total amount
                    if(window.location.pathname == '/cart/'){
                    total_amount(

                        response.cart_amount['subtotal'],
                        response.cart_amount['tax'],
                        response.cart_amount['total']
                        
                        )

                    }

                }

            }
        })
    })


    

    //cart item quantity
    $('.item_qty').each(function() {

        var id = $(this).attr('id')
        var qty= $(this).attr('data-qty')
        $('#'+id).html(qty)
    })

    
    //decrease cart
    $('.decrease_cart').on('click', function(e) {

        e.preventDefault()
        food_id = $(this).attr('data-id')
        url = $(this).attr('data-url')
        cart_id = $(this).attr('id')


        data = {

            food_id: food_id
        }

        $.ajax({

            type: 'GET',
            url: url,
            data: data,
            success: function(response) {

                if(response.status == 'login_required') {

                    Swal.fire(response.message, '', 'error').then(function() {

                        window.location = '/login';
                    })

                }else if(response.status == 'Failed') {

                    Swal.fire(response.message, '', 'error')

                  
                   }else {

                    $('#cart-counter').html(response.cart_counter['cart_count'])
                    $('#qty-' +food_id).html(response.qty)

                    total_amount(

                        response.cart_amount['subtotal'],
                        response.cart_amount['tax'],
                        response.cart_amount['total']
                    )
                
                    
                    if(window.location.pathname == '/cart/'){
                    removeCartItem(response.qty, cart_id)
                    checkEmptyCart()

                    }

                  
                }

                
             }
        })
    })


    //delete cart item
    $('.delete_cart').on('click', function(e) {

      e.preventDefault()
      cart_id = $(this).attr('data-id')
      url = $(this).attr('data-url')

      $.ajax({

        type: 'GET',
        url: url,
        success: function(response){

            console.log(response);

            if(response.status == 'Failed'){

                Swal.fire(response.message, '', 'error')

   
            }else {

                $('#cart_counter').html(response.cart_counter['cart_count'])
                Swal.fire(response.status, response.message, 'success')


                total_amount(

                    response.cart_amount['subtotal'],
                    response.cart_amount['tax'],
                    response.cart_amount['total']
                )

             

                removeCartItem(0, cart_id)
                checkEmptyCart()

             
            }
        }

      })

    })

    //delete cart if the qty is 0
    function removeCartItem(cartItemQty, cart_id){
        
        if(cartItemQty <= 0) {
          //remove the cart utem
          document.getElementById("cart-item-" +cart_id).remove()

        }

    

    }


    //check if cart is empty
    function checkEmptyCart(){

        var cart_counter = document.getElementById('cart_counter').innerHTML
        if(cart_counter == 0) {

            document.getElementById('empty-cart').style.display = 'block';
        }
    }

    //cart total
    function total_amount(subtotal, tax, total){
        
        if(window.location.pathname == '/cart/') {

        $('#subtotal').html(subtotal)
        $('#tax').html(tax)
        $('#total').html(total)

        }
    }

});