from django.contrib import admin
from user.models import User, UserAddress


# Register your models here.


class AddressAdmin(admin.TabularInline):
    model = UserAddress
    fields = ["street_address", "city", "postal_code", "country"]


class UserAdmin(admin.ModelAdmin):
    readonly_fields = ("id",)
    inlines = [AddressAdmin]


admin.site.register(User, UserAdmin)
