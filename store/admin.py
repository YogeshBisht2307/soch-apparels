from django.contrib import admin
from store.models import Cloth, Brand, Color, Occasion, Category, Sub_Category, Size_Variant, Cart, Order, Payment, \
    Order_Item, Comment, Contact, WebsiteDetail, About
from django.utils.html import format_html


# Register your models here.
class Size_Variant_Configuration(admin.TabularInline):
    model = Size_Variant


class Order_Item_Configuration(admin.TabularInline):
    model = Order_Item


class Comment_Configurations(admin.TabularInline):
    model = Comment


# admin site configuration of Cloth

class Cloth_Configuration(admin.ModelAdmin):
    inlines = [Size_Variant_Configuration, Comment_Configurations]
    list_display = ['get_image', 'cloth_name', 'cloth_discount']
    list_editable = ['cloth_discount']
    sortable_by = ['cloth_discount']
    list_filter = ['cloth_discount']
    list_display_links = ['cloth_name']
    list_per_page = 6
    search_fields = ('cloth_name','cloth_discount')

    def get_image(self, obj):
        return format_html(f"""
            <a href='{obj.cloth_image.url}' target='_blank'><img height='60px' src='{obj.cloth_image.url}'/></a>
        """)


# admin site configuration of Cart

class Cart_Configuration(admin.ModelAdmin):
    model = Cart
    list_display = ['cloth', 'quantity', 'size', 'user']
    search_fields = ('cloth', 'size', 'user')

    fieldsets = (
        ("Cart Info", {"fields": ('user', 'get_cloth', 'get_sizeVariant', 'quantity')}),
    )
    readonly_fields = ('quantity', 'get_sizeVariant', 'user', 'get_cloth')

    def get_sizeVariant(self, obj):
        return obj.sizeVariant.size

    def get_cloth(self, obj):
        cloth = obj.sizeVariant.cloth
        cloth_id = cloth.id
        cloth_name = cloth.cloth_name
        return format_html(f'<a href="/admin/store/cloth/{cloth_id}/change/" target="_blank" >{cloth_name}</a>')

    get_cloth.short_description = 'Cloth'
    get_sizeVariant.short_description = "Size"
    # cloth information will be displayed by clicking on name
    list_display_links = ['cloth']
    # pagination in admin site
    list_per_page = 10

    def size(self, obj):
        return obj.sizeVariant.size

    def cloth(self, obj):
        return obj.sizeVariant.cloth.cloth_name


# admin site configuration of Orders
class Order_Configuration(admin.ModelAdmin):
    list_display = ['user', 'shipping_address', 'phone', 'date', 'total', 'order_status']
    list_editable = ['order_status']
    search_fields = ('id', 'user','phone','order_status')
    readonly_fields = (
    'user', 'shipping_address', 'phone', 'date', 'total', 'payment_method', 'payment', 'payment_request_id',
    'payment_id', 'payment_status')

    fieldsets = (
        ("Order Information", {"fields": ('order_status', 'shipping_address', 'phone', 'total', 'user',)}),
        ("Payment Information", {"fields": ('payment', 'payment_request_id', 'payment_id', 'payment_status')}),
    )

    inlines = [Order_Item_Configuration]

    # pagination in admin site
    list_per_page = 10

    def payment_request_id(self, obj):
        try:
            payment_request_id = obj.payment_set.all()[0].payment_request_id
        except:
            payment_request_id = None
        if (payment_request_id is None and payment_request_id == ""):
            return "Payment request Id is not available"
        else:
            return payment_request_id

    def payment_status(self, obj):
        try:
            status = obj.payment_set.all()[0].payment_status
        except:
            status = "Failed"
        return status

    def payment_id(self, obj):
        try:
            payment_id = obj.payment_set.all()[0].payment_id
        except:
            payment_id = None
        if (payment_id is None and payment_id == ""):
            return "Payment request Id is not available"
        else:
            return payment_id

    def payment(self, obj):
        try:
            payment_id = obj.payment_set.all()[0].id
        except:
            return "Payment associated with this Order does'nt exist, Payment may Failed"
        return format_html(
            f'<a href="/admin/store/payment/{payment_id}/change/" target="_blank" >Click for Payment Information</a>')

class WebsiteDetail_configurations(admin.ModelAdmin):
    model = WebsiteDetail
    def has_add_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False

class About_Configurations(admin.ModelAdmin):
    mdoel = About
    def has_add_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
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
