from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Product, Category, Customers
from django.utils.html import format_html
from adminsortable2.admin import SortableAdminMixin


@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('title', 'category', 'price', 'discount', 'shipping_cost', 'stock', 'created_at', 'updated_at', 'image_tag')
    search_fields = ('title', 'information')
    list_filter = ('category', 'stock', 'created_at')
    autocomplete_fields = ('category',)

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" />', obj.image.url)
        return "-"

    image_tag.short_description = "Image"


class ProductInline(admin.TabularInline):
    model = Product
    extra = 0

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'product_count')
    search_fields = ('name',)
    inlines = [ProductInline]

    def product_count(self, obj):
        return obj.product_set.count()
    product_count.short_description = 'Product Count'



@admin.register(Customers)
class CustomersAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'billing_address', 'joined')
    search_fields = ('name', 'email')
    ordering = ('-joined',)


admin.site.site_header = "Apelsin Admin"
admin.site.site_title = "Apelsin Admin"
admin.site.index_title = "Welcome to Apelsin Researcher Portal"
