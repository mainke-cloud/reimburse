from django.contrib import admin
from .models import Reimburse, ReimburseLine, ReimburseHistory

class Inline(admin.TabularInline):
    model = ReimburseLine
    extra = 0
    readonly_fields = ['subtotal',]

class HistoryInline(admin.TabularInline):
    model = ReimburseHistory
    extra = 0

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Reimburse)
class ReimburseAdmin(admin.ModelAdmin):
    readonly_fields = ['total',]
    inlines = [
        HistoryInline,
        Inline,
    ]
