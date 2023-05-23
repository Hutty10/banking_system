from django.contrib import admin
from transaction.models import Transactions


# Register your models here.
class TransactionAdmin(admin.ModelAdmin):
    readonly_fields = ["account", "id", "receiver_account"]


admin.site.register(Transactions, TransactionAdmin)
