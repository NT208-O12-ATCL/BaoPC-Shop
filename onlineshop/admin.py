from django.contrib import admin
from .models import Product
from .models import EmailAddress
from django.urls import reverse
from django.http import HttpResponseRedirect
from .models import Order
from .models import Review

admin.site.site_header = "BaoPC Shop"
admin.site.site_title = "BaoPC Shop"
admin.site.index_title = "Welcome to BaoPC Shop"

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price','description', 'image', 'purchase_count']
    readonly_fields = ('purchase_count',)
    list_filter = ['price']
    search_fields = ['name']
    
admin.site.register(Product, ProductAdmin)

@admin.register(EmailAddress)
class EmailAddressAdmin(admin.ModelAdmin):
    list_display = ('email',)
    actions = ['custom_send_email']

    def custom_send_email(self, request, queryset):
        selected_ids = queryset.values_list('id', flat=True)
        selected_ids_str = ','.join(str(id) for id in selected_ids)
        url = reverse('send_email', args=[selected_ids_str])
        return HttpResponseRedirect(url)
    custom_send_email.short_description = "Send Email"
    
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone_number', 'address', 'total', 'create_at']
    list_filter = ['name', 'phone_number', 'address', 'total', 'create_at']
    search_fields = ['name', 'phone_number', 'address']
    
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['name', 'review_text', 'created_at']
    list_filter = ['name']
    search_fields = ['name']


