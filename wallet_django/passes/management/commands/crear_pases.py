from django.core.management.base import BaseCommand

from passes.models import WalletPass

DEMO_PASSES = [
    {
        "logo_text": "JOHAN RIVERA",
        "member_name": "Johan Rivera",
        "level": "Black",
        "member_since": "2026",
        "member_id": "JR-0001",
        "back_info": "Pase personalizado.",
    },
    {
        "logo_text": "JOHAN RIVERA",
        "member_name": "Johan Rivera",
        "level": "Platinum",
        "member_since": "2026",
        "member_id": "JR-0002",
        "background_color": "#1C2A3A",
        "label_color": "#C0C7D1",
    },
]


class Command(BaseCommand):
    help = "Crea los pases de ejemplo (no duplica si ya existen)."

    def handle(self, *args, **options):
        for data in DEMO_PASSES:
            obj, created = WalletPass.objects.get_or_create(member_id=data["member_id"], defaults=data)
            self.stdout.write(f"{'Creado' if created else 'Ya existía'}: {obj} (id {obj.pk})")
