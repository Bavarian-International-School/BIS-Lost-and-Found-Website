from django.contrib import admin

from .models import Customer, LostItem


@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "name", "newsletter_signup"]


class LostItemModelAdmin(admin.ModelAdmin):
    list_display = ("id", "get_name", "category", "get_product_image")

    def get_name(self, obj: LostItem) -> str:
        return obj.name

    get_name.short_description = "Name"

    def get_product_image(self, obj: LostItem) -> str | None:
        return obj.image.url if obj.image else None

    get_product_image.short_description = "LostItem Image"


admin.site.register(LostItem, LostItemModelAdmin)
