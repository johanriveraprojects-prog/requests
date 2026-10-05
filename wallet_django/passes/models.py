import uuid

from django.core.validators import RegexValidator
from django.db import models
from django.urls import reverse

hex_color = RegexValidator(r"^#[0-9A-Fa-f]{6}$", "Usa un color hex como #121218.")


class WalletPass(models.Model):
    serial_number = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    organization_name = models.CharField("organización", max_length=60, default="Grupo X")
    description = models.CharField("descripción", max_length=120, default="Tarjeta personal")
    logo_text = models.CharField("texto del logo", max_length=30, default="GRUPO X")

    member_name = models.CharField("miembro", max_length=40)
    level = models.CharField("nivel", max_length=20, blank=True, default="Black")
    member_since = models.CharField("miembro desde", max_length=20, blank=True, default="2026")
    member_id = models.CharField("ID", max_length=30)
    barcode_message = models.CharField(
        "contenido del QR", max_length=200, blank=True, help_text="Vacío = usa el ID."
    )
    back_info = models.TextField("info del reverso", blank=True)

    background_color = models.CharField("fondo", max_length=7, default="#121218", validators=[hex_color])
    foreground_color = models.CharField("texto", max_length=7, default="#FFFFFF", validators=[hex_color])
    label_color = models.CharField("etiquetas", max_length=7, default="#D4AF37", validators=[hex_color])

    logo = models.ImageField("logo", upload_to="passes/logos/", blank=True)
    strip = models.ImageField("franja", upload_to="passes/strips/", blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "pase"

    def __str__(self):
        return f"{self.logo_text} — {self.member_name}"

    def get_absolute_url(self):
        return reverse("passes:detail", args=[self.pk])

    @property
    def qr_message(self):
        return self.barcode_message or self.member_id
