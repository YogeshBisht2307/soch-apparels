from math import floor
from django import template
from store.models import WebsiteDetail

register = template.Library()
website = WebsiteDetail.objects.first()

@register.simple_tag
def faviconIcon() -> str:
    favicon = website.favicon_icon.url
    return favicon

@register.simple_tag
def web_logo() -> str:
    logo = website.website_logo.url
    return logo

@register.simple_tag
def web_name() -> str:
    return website.website_name

@register.simple_tag
def get_address() -> str:
    return website.location


@register.simple_tag
def get_email_1() -> str:
    return website.email_1


@register.simple_tag
def get_mobile_1() -> str:
    return website.mobile_1


@register.simple_tag
def get_city() -> str:
    return website.city

@register.simple_tag
def get_name() -> str:
    return website.website_name

# simple tags
@register.simple_tag
def counter(loop_Counter: int) -> int:
    return loop_Counter - 1


@register.simple_tag
def min_price(cloth) -> int:
    size = cloth.size_variant_set.all().order_by('price').first()
    return size.price


@register.simple_tag
def calculate_sale_price(price: int, discount: int) -> int:
    return floor(price - (price * discount / 100))


@register.simple_tag
def discount_price(cloth) -> int:
    size_price = min_price(cloth)
    after_discount = size_price - (size_price * cloth.cloth_discount / 100)
    after_discount = floor(after_discount)
    return after_discount


@register.simple_tag
def active_size_class(active_size: str, size: str) -> str:
    if active_size == size:
        return "active"

    return ""


@register.simple_tag
def get_order_status(order_status: str) -> str:
    if order_status == "COMPLETE":
        return "success"
    elif order_status == "CANCELED":
        return "danger"
    else:
        return "warning"


@register.simple_tag
def disable_cancel_order_button(order_status: str) -> str:
    if order_status == "COMPLETE" and order_status == "CANCELED":
        return "disable"
    return ""


@register.simple_tag
def multiply(a: int, b: int) -> int:
    try:
        return a * b
    except:
        a, b = 0, 0
        return a * b


@register.simple_tag
def selected_attr(request_slug: str, slug: str) -> str:
    if request_slug == slug:
        return "selected"
    return ""


@register.filter
def rupee(number: int) -> str:
    return f'₹ {number}'


@register.filter
def total_payable_amount(cart) -> int:
    total = 0
    for c in cart:
        discount = c.get("cloth").cloth_discount
        price = c.get('size').price
        sale_price = calculate_sale_price(price, discount)
        total_of_single_product = sale_price * c['quantity']
        total = total + total_of_single_product
    return total

