from django import forms

from .models import WalletPass


class WalletPassForm(forms.ModelForm):
    class Meta:
        model = WalletPass
        fields = [
            "logo_text",
            "organization_name",
            "description",
            "member_name",
            "level",
            "member_since",
            "member_id",
            "barcode_message",
            "back_info",
            "background_color",
            "foreground_color",
            "label_color",
            "logo",
            "strip",
        ]
        widgets = {
            "background_color": forms.TextInput(attrs={"type": "color"}),
            "foreground_color": forms.TextInput(attrs={"type": "color"}),
            "label_color": forms.TextInput(attrs={"type": "color"}),
            "back_info": forms.Textarea(attrs={"rows": 3}),
        }
