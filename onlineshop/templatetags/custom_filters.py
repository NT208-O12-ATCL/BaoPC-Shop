from django import template

register = template.Library()

@register.filter(name='multiply')
def multiply(value, arg):
    try:
        result = float(value) * float(arg)
        return int(result)
    except (ValueError, TypeError):
        return 0
    
@register.filter
def calculate_total(cart):
    total_price = sum(item['price'] * item['quantity'] for item in cart)
    return round(total_price, 2)
