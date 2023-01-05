from store.models import *
from django.contrib import admin
from django.utils.html import format_html
from typing import Dict, List, Any, Optional, Tuple


class Size_Variant_Configuration(admin.TabularInline):
    model = Size_Variant

class Order_Item_Configuration(admin.TabularInline):
    model = Order_Item

class Comment_Configurations(admin.TabularInline):
    model = Comment


# Admin site configuration of Cloth
class Cloth_Configuration(admin.ModelAdmin):
    inlines: List = [Size_Variant_Configuration, Comment_Configurations]
    list_per_page: int = 6
    list_editable: List[str] = ['cloth_discount']
    sortable_by: List[str] = ['cloth_discount']
    list_filter: List[str] = ['cloth_discount']
    list_display_links: List[str] = ['cloth_name']
    search_fields: Tuple = ('cloth_name','cloth_discount')
    list_display: List[str] = ['get_image', 'cloth_name', 'cloth_discount']


    def get_image(self, obj: Cloth) -> str:
        return format_html(f"""
            <a href='{obj.cloth_image.url}' target='_blank'><img height='60px' src='{obj.cloth_image.url}'/></a>
        """)


# admin site configuration of Cart
class Cart_Configuration(admin.ModelAdmin):
    model = Cart
    list_per_page = 10
    list_display_links = ['cloth']
    list_display: List = ['cloth', 'quantity', 'size', 'user']
    search_fields: Tuple = ('cloth', 'size', 'user')

    fieldsets: Tuple = (
        ("Cart Info", {"fields": ('user', 'get_cloth', 'get_sizeVariant', 'quantity')}),
    )
    readonly_fields = ('quantity', 'get_sizeVariant', 'user', 'get_cloth')

    def get_sizeVariant(self, obj: Cart) -> str:
        return obj.sizeVariant.size

    def get_cloth(self, obj: Cart) -> str:
        cloth = obj.sizeVariant.cloth
        cloth_id = cloth.id
        cloth_name = cloth.cloth_name
        return format_html(f'<a href="/admin/store/cloth/{cloth_id}/change/" target="_blank" >{cloth_name}</a>')

    get_cloth.short_description = 'Cloth'
    get_sizeVariant.short_description = "Size"

    def size(self, obj: Cart) -> str:
        return obj.sizeVariant.size

    def cloth(self, obj: Cart) -> str:
        return obj.sizeVariant.cloth.cloth_name


# Admin site configuration of Orders
class Order_Configuration(admin.ModelAdmin):
    list_per_page = 10
    inlines: List = [Order_Item_Configuration]
    list_editable: List[str] = ['order_status']
    search_fields: Tuple = ('id', 'user','phone','order_status')
    list_display: List[str] = ['user', 'shipping_address', 'phone', 'date', 'total', 'order_status']
    readonly_fields: Tuple = (
    'user', 'shipping_address', 'phone', 'date', 'total', 'payment_method', 'payment', 'payment_request_id',
    'payment_id', 'payment_status')

    fieldsets: Tuple = (
        ("Order Information", {"fields": ('order_status', 'shipping_address', 'phone', 'total', 'user',)}),
        ("Payment Information", {"fields": ('payment', 'payment_request_id', 'payment_id', 'payment_status')}),
    )

    def payment_request_id(self, obj: Order) -> Optional[str]:
        try:
            payment_request_id = obj.payment_set.all()[0].payment_request_id
        except:
            payment_request_id = None

        if (payment_request_id is None and payment_request_id == ""):
            return "Payment request Id is not available"
        else:
            return payment_request_id

    def payment_status(self, obj: Order) -> str:
        try:
            status = obj.payment_set.all()[0].payment_status
        except:
            status = "Failed"
        return status

    def payment_id(self, obj: Order) -> Optional[str]:
        try:
            payment_id = obj.payment_set.all()[0].payment_id
        except:
            payment_id = None
        if (payment_id is None and payment_id == ""):
            return "Payment request Id is not available"
        else:
            return payment_id

    def payment(self, obj: Order) -> str:
        try:
            payment_id = obj.payment_set.all()[0].id
        except:
            return "Payment associated with this Order does'nt exist, Payment may Failed"
        return format_html(
            f'<a href="/admin/store/payment/{payment_id}/change/" target="_blank" >Click for Payment Information</a>')

class WebsiteDetail_configurations(admin.ModelAdmin):
    model = WebsiteDetail
    def has_add_permission(self, request, obj: Optional[WebsiteDetail]=None) -> bool:
        return False
    def has_delete_permission(self, request, obj: Optional[WebsiteDetail]=None):
        return False

class About_Configurations(admin.ModelAdmin):
    mdoel = About
    def has_add_permission(self, request, obj: Optional[About]=None) -> bool:
        return False
    def has_delete_permission(self, request, obj: Optional[About]=None) -> bool:
        return False


admin.site.register(About, About_Configurations)
admin.site.register(WebsiteDetail, WebsiteDetail_configurations)
admin.site.register(Cloth, Cloth_Configuration)
admin.site.register(Brand)
admin.site.register(Color)
admin.site.register(Occasion)
admin.site.register(Category)
admin.site.register(Sub_Category)
admin.site.register(Cart, Cart_Configuration)
admin.site.register(Order, Order_Configuration)
admin.site.register(Payment)
admin.site.register(Order_Item)
admin.site.register(Contact)
