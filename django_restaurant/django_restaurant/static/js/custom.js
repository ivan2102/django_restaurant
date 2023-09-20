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
                    
                    total_amount(

                        response.cart_amount['subtotal'],
                        response.cart_amount['tax_dict'],
                        response.cart_amount['total']
                        
                        )

                    

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
                        response.cart_amount['tax_dict'],
                        response.cart_amount['total']
                    )

                    
                
                    
                    if(window.location.pathname == '/cart/'){
                    removeCartItem(response.qty, cart_id)
                    checkEmptyCart()
                    window.location.reload()

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
                    response.cart_amount['tax_dict'],
                    response.cart_amount['total']
                )

             

                removeCartItem(0, cart_id)
                checkEmptyCart()
                window.location.reload()

             
            }
        }

      })

    })

    //delete cart if the qty is 0
    function removeCartItem(cartItemQty, cart_id){
        
        if(cartItemQty <= 0) {
          //remove the cart utem
          document.getElementById("cart-item-" + cart_id).remove()

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
        $('#total').html(total)

        for(key1 in tax_dict){
            console.log(tax_dict[key1])
            for(key2 in tax_dict[key1]){
                // console.log(tax_dict[key1][key2])
                $('#tax-'+key1).html(tax_dict[key1][key2])
            }
        }
        

        }

        
          window.location.reload()
    }


    //add hours
    $('.add_hour').on('click', function(e) {

        e.preventDefault()
        var day = document.getElementById('id_day').value
        var from_hour = document.getElementById('id_from_hour').value
        var to_hour = document.getElementById('id_to_hour').value
        var is_closed = document.getElementById('id_is_closed').checked
        var csrf_token = $('input[name=csrfmiddlewaretoken]').val()
        var url = document.getElementById('add_hour_url').value

        
        
        if(is_closed) {

            is_closed = 'True'
            condition = "day != ''"

        }else {

            is_closed = 'False'
            condition = "day != '' && from_hour != '' && to_hour != ''"
        }


        if(eval(condition) ) {

            $.ajax({

                type: 'POST',
                url: url,
                data: {

                    'day': day,
                    'from_hour': from_hour,
                    'to_hour': to_hour,
                    'is_closed': is_closed,
                    'csrfmiddlewaretoken': csrf_token
                },

                success: function(response) {

                    if(response.status == 'success'){

                        if(response.is_closed == 'Closed') {

                            html = '<tr id="hour- '+ response.id +'"><td><b>'+ response.day +'</b></td><td>Closed</td><td><a href="#" class="remove_hour" data-url="/accounts/vendor/opening-hours/delete/'+ response.id +'/"><i class="fa fa-trash-alt text-danger"></i></a></td></tr>'

                        }else {

                            html = '<tr id="hour- '+ response.id +'"><td><b>'+ response.day +'</b></td><td>'+ response.from_hour +' - '+ response.to_hour +'</td><td><a href="#" class="remove_hour" data-url="/accounts/vendor/opening-hours/delete/'+ response.id +'/"><i class="fa fa-trash-alt text-danger"></i></a></td></tr>'
                        }

                     
                      $('.opening_hours').append(html)
                      document.getElementById("opening_hours").reset()

                    }else {

                        Swal.fire(response.message, '', 'error')
                    }
                }
            })

        }else {

            Swal.fire('Please add all fields', '', 'secondary')
        }


    })

    //remove hour
    $(document).on('click', '.remove_hour', function(e){

        e.preventDefault()
        url = $(this).attr('data-url')

        $.ajax({

            type: 'GET',
            url: url,

            success: function(response) {

                console.log(response);

                if(response.status == 'success' || response.status != 0) {

                    document.getElementById('hour-' + response.id).remove()
                }
            }
        })
    })

});