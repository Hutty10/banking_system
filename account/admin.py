from django.contrib import admin
from account.models import Account, AccountType


# Register your models here.
class AccountAdmin(admin.ModelAdmin):
    readonly_fields = ("account_no",)


admin.site.register(AccountType)
admin.site.register(Account, AccountAdmin)
