# Pases Wallet (Django)

Web para crear pases de Apple Wallet (`.pkpass`, tipo *store card*): colores, logo, franja, campos y código QR.

## Arrancar

```
cd wallet_django
pip install -r requirements.txt
python manage.py migrate
python manage.py crear_pases      # crea los pases de ejemplo JR-0001 (Black) y JR-0002 (Platinum)
python manage.py runserver
```

Abre http://127.0.0.1:8000/ para ver los pases, crear uno nuevo y descargarlo.
Para abrirlo desde el iPhone en la misma red Wi-Fi: `python manage.py runserver 0.0.0.0:8000`,
añade la IP del PC a `ALLOWED_HOSTS` en `walletsite/settings.py` y entra a `http://IP-DEL-PC:8000/`.

## Firma

El iPhone solo acepta pases firmados con un certificado de Apple (Pass Type ID, requiere Apple Developer).

- **Sin certificado:** el `.pkpass` se descarga sin firmar (sirve para revisar el contenido). Usa
  «Descargar imágenes» y crea el pase en AddPass o WalletWallet con los datos de `datos.txt`.
- **Con certificado:** define estas variables de entorno y los `.pkpass` saldrán firmados:

  | Variable | Valor |
  |---|---|
  | `PASS_TYPE_IDENTIFIER` | p. ej. `pass.com.tunombre.mipase` |
  | `PASS_TEAM_IDENTIFIER` | tu Team ID de 10 caracteres |
  | `PASS_CERT_P12` | ruta al `.p12` del Pass Type ID |
  | `PASS_CERT_PASSWORD` | contraseña del `.p12` |
  | `PASS_WWDR_PEM` | ruta al certificado Apple WWDR G4 en PEM |

## Tests

```
python manage.py test passes
```
