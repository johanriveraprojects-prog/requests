from django.contrib import admin

from .models import WalletPass


@admin.register(WalletPass)
class WalletPassAdmin(admin.ModelAdmin):
    list_display = ("logo_text", "member_name", "member_id", "created_at")
    search_fields = ("member_name", "member_id", "logo_text")
