import datetime
import simplejson as json

def generate_order_number(pk):
    current_datetime = datetime.datetime.now().strftime('%Y%m%d%H')
    order_number = current_datetime + str(pk)
    return order_number


def order_vendor_total(order, vendor_id):
    total_data = json.loads(order.total_data)
    data = total_data.get(str(vendor_id))

    subtotal = 0
    tax = 0
    tax_dict = {}

    for key, value in data.items():
        subtotal += float(key)
        value = value.replace("'", '"')
        value = json.loads(value)
        tax_dict.update(value)

        # Calculate tax
        for i in value:
            for j in value[i]:
                tax += float(value[i][j])
                total = float(subtotal) + float(tax)

                context = {

                    'subtotal': subtotal,
                    'tax_dict': tax_dict,
                    'total': total
                }

                return context