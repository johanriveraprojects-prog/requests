import io
import json
import zipfile

from django.test import TestCase
from django.urls import reverse

from .models import WalletPass


class WalletPassTests(TestCase):
    def setUp(self):
        self.p = WalletPass.objects.create(member_name="Johan Rivera", member_id="JR-0001")

    def test_pkpass_contents(self):
        resp = self.client.get(reverse("passes:download", args=[self.p.pk]))
        self.assertEqual(resp["Content-Type"], "application/vnd.apple.pkpass")
        zf = zipfile.ZipFile(io.BytesIO(resp.content))
        names = set(zf.namelist())
        for n in ("pass.json", "manifest.json", "icon.png", "icon@2x.png", "logo@3x.png", "strip@3x.png"):
            self.assertIn(n, names)
        data = json.loads(zf.read("pass.json"))
        self.assertEqual(data["storeCard"]["primaryFields"][0]["value"], "Johan Rivera")
        self.assertEqual(data["barcodes"][0]["message"], "JR-0001")
        manifest = json.loads(zf.read("manifest.json"))
        self.assertEqual(set(manifest), names - {"manifest.json"})
        self.assertNotIn("signature", names)

    def test_pages(self):
        for name, args in (("list", []), ("create", []), ("detail", [self.p.pk])):
            self.assertEqual(self.client.get(reverse(f"passes:{name}", args=args)).status_code, 200)
        self.assertEqual(self.client.get(reverse("passes:images", args=[self.p.pk])).status_code, 200)

    def test_create_via_form(self):
        resp = self.client.post(
            reverse("passes:create"),
            {
                "logo_text": "MI CLUB", "organization_name": "Grupo X", "description": "x",
                "member_name": "Ana", "member_id": "A-1", "background_color": "#000000",
                "foreground_color": "#FFFFFF", "label_color": "#FF0000",
            },
        )
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(WalletPass.objects.filter(member_id="A-1").exists())
