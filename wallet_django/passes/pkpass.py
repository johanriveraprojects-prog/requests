"""Construcción de archivos .pkpass (Apple Wallet) a partir de un WalletPass."""

import hashlib
import io
import json
import math
import zipfile
from pathlib import Path

from django.conf import settings
from PIL import Image, ImageDraw, ImageFont

SCALES = ((1, ""), (2, "@2x"), (3, "@3x"))
ICON_SIZE = (29, 29)
LOGO_SIZE = (50, 50)
STRIP_SIZE = (375, 123)


def _rgb(hex_color):
    h = hex_color.lstrip("#")
    return tuple(int(h[i : i + 2], 16) for i in (0, 2, 4))


def _css_rgb(hex_color):
    return "rgb({}, {}, {})".format(*_rgb(hex_color))


def _font(size):
    for path in (
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf",
        "C:/Windows/Fonts/arialbd.ttf",
    ):
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    return ImageFont.load_default()


def _initials(text):
    words = [w for w in text.split() if w]
    return ("".join(w[0] for w in words[:2]) or "W").upper()


def _monogram(size, initials, accent, background):
    """Círculo con iniciales; fondo transparente si background es None."""
    w, h = size
    fill = (0, 0, 0, 0) if background is None else background + (255,)
    im = Image.new("RGBA", size, fill)
    d = ImageDraw.Draw(im)
    r = min(w, h) * 0.44
    cx, cy = w / 2, h / 2
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=accent, width=max(1, min(w, h) // 22))
    f = _font(int(min(w, h) * 0.38))
    b = d.textbbox((0, 0), initials, font=f)
    d.text((cx - (b[2] - b[0]) / 2 - b[0], cy - (b[3] - b[1]) / 2 - b[1]), initials, font=f, fill=accent)
    return im


def _default_strip(size, background, accent):
    w, h = size
    im = Image.new("RGB", size, background)
    px = im.load()
    for x in range(w):
        t = x / w
        for y in range(h):
            v = 0.5 + 0.5 * math.sin(t * 6 + y / h * 2)
            k = 0.25 * t * v
            px[x, y] = tuple(int(c + (a - c) * k) for c, a in zip(background, accent))
    d = ImageDraw.Draw(im)
    line = tuple(int(c + (a - c) * 0.35) for c, a in zip(background, accent))
    for i in range(6):
        o = i * w / 14
        d.line([(w * 0.35 + o, h), (w * 0.55 + o, 0)], fill=line, width=max(1, w // 250))
    return im


def _fit(source, size):
    """Recorta al centro y escala la imagen subida al tamaño exacto."""
    src = Image.open(source)
    src = src.convert("RGBA")
    tw, th = size
    scale = max(tw / src.width, th / src.height)
    resized = src.resize((math.ceil(src.width * scale), math.ceil(src.height * scale)), Image.LANCZOS)
    left = (resized.width - tw) // 2
    top = (resized.height - th) // 2
    return resized.crop((left, top, left + tw, top + th))


def _png(im):
    buf = io.BytesIO()
    im.save(buf, format="PNG")
    return buf.getvalue()


def build_images(wallet_pass):
    """Devuelve {nombre_archivo: bytes_png} con icon/logo/strip en @1x/@2x/@3x."""
    bg = _rgb(wallet_pass.background_color)
    accent = _rgb(wallet_pass.label_color)
    initials = _initials(wallet_pass.logo_text)
    images = {}
    for scale, suffix in SCALES:
        icon_size = (ICON_SIZE[0] * scale, ICON_SIZE[1] * scale)
        logo_size = (LOGO_SIZE[0] * scale, LOGO_SIZE[1] * scale)
        strip_size = (STRIP_SIZE[0] * scale, STRIP_SIZE[1] * scale)

        if wallet_pass.logo:
            wallet_pass.logo.open("rb")
            logo = _fit(wallet_pass.logo, logo_size)
            wallet_pass.logo.seek(0)
            icon = _fit(wallet_pass.logo, icon_size)
            wallet_pass.logo.close()
        else:
            logo = _monogram(logo_size, initials, accent, None)
            icon = _monogram(icon_size, initials, accent, bg)

        if wallet_pass.strip:
            wallet_pass.strip.open("rb")
            strip = _fit(wallet_pass.strip, strip_size).convert("RGB")
            wallet_pass.strip.close()
        else:
            strip = _default_strip(strip_size, bg, accent)

        images[f"icon{suffix}.png"] = _png(icon)
        images[f"logo{suffix}.png"] = _png(logo)
        images[f"strip{suffix}.png"] = _png(strip)
    return images


def build_pass_json(wallet_pass):
    secondary = []
    if wallet_pass.level:
        secondary.append({"key": "nivel", "label": "NIVEL", "value": wallet_pass.level})
    if wallet_pass.member_since:
        secondary.append({"key": "desde", "label": "MIEMBRO DESDE", "value": wallet_pass.member_since})
    back = []
    if wallet_pass.back_info:
        back.append({"key": "info", "label": "Info", "value": wallet_pass.back_info})

    return {
        "formatVersion": 1,
        "passTypeIdentifier": settings.PASS_TYPE_IDENTIFIER,
        "teamIdentifier": settings.PASS_TEAM_IDENTIFIER,
        "serialNumber": str(wallet_pass.serial_number),
        "organizationName": wallet_pass.organization_name,
        "description": wallet_pass.description,
        "logoText": wallet_pass.logo_text,
        "foregroundColor": _css_rgb(wallet_pass.foreground_color),
        "labelColor": _css_rgb(wallet_pass.label_color),
        "backgroundColor": _css_rgb(wallet_pass.background_color),
        "storeCard": {
            "primaryFields": [{"key": "nombre", "label": "MIEMBRO", "value": wallet_pass.member_name}],
            "secondaryFields": secondary,
            "auxiliaryFields": [{"key": "id", "label": "ID", "value": wallet_pass.member_id}],
            "backFields": back,
        },
        "barcodes": [
            {
                "format": "PKBarcodeFormatQR",
                "message": wallet_pass.qr_message,
                "messageEncoding": "iso-8859-1",
                "altText": wallet_pass.qr_message,
            }
        ],
    }


def signing_configured():
    return bool(settings.PASS_CERT_P12 and settings.PASS_WWDR_PEM)


def _sign(manifest_bytes):
    """Firma PKCS#7 separada del manifest con el certificado del Pass Type ID."""
    from cryptography import x509
    from cryptography.hazmat.primitives import hashes, serialization
    from cryptography.hazmat.primitives.serialization import pkcs7, pkcs12

    password = settings.PASS_CERT_PASSWORD.encode() or None
    key, cert, _ = pkcs12.load_key_and_certificates(Path(settings.PASS_CERT_P12).read_bytes(), password)
    wwdr = x509.load_pem_x509_certificate(Path(settings.PASS_WWDR_PEM).read_bytes())
    return (
        pkcs7.PKCS7SignatureBuilder()
        .set_data(manifest_bytes)
        .add_signer(cert, key, hashes.SHA256())
        .add_certificate(wwdr)
        .sign(serialization.Encoding.DER, [pkcs7.PKCS7Options.DetachedSignature, pkcs7.PKCS7Options.Binary])
    )


def build_pkpass(wallet_pass):
    """Devuelve (bytes_del_pkpass, firmado: bool)."""
    files = {"pass.json": json.dumps(build_pass_json(wallet_pass), ensure_ascii=False, indent=2).encode()}
    files.update(build_images(wallet_pass))
    manifest = json.dumps({name: hashlib.sha1(data).hexdigest() for name, data in files.items()}, indent=2).encode()
    files["manifest.json"] = manifest

    signed = signing_configured()
    if signed:
        files["signature"] = _sign(manifest)

    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        for name, data in files.items():
            zf.writestr(name, data)
    return buf.getvalue(), signed


def build_images_zip(wallet_pass):
    """Zip con las imágenes @3x y un txt con colores y campos, para webs como AddPass."""
    images = build_images(wallet_pass)
    p = wallet_pass
    guide = (
        f"Colores: fondo {p.background_color} · texto {p.foreground_color} · etiquetas {p.label_color}\n"
        f"Texto del logo: {p.logo_text}\n"
        f"MIEMBRO: {p.member_name}\nNIVEL: {p.level}\nMIEMBRO DESDE: {p.member_since}\n"
        f"ID: {p.member_id}\nQR: {p.qr_message}\n"
    )
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        for name in ("logo@3x.png", "icon@3x.png", "strip@3x.png"):
            zf.writestr(name, images[name])
        zf.writestr("datos.txt", guide)
    return buf.getvalue()
