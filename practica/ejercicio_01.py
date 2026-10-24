"""
Exercise 1 - Bill of quantities (Presupuesto por partidas)

Glossary / Glosario
  bill of quantities = presupuesto por partidas     quantity   = cantidad
  unit price         = precio unitario              subtotal   = subtotal
  VAT (tax)          = IVA                          round      = redondear

Your task / Tu tarea: complete the two functions below (replace `raise NotImplementedError`).
Run it with:  python practica/ejercicio_01.py
"""

items = [
    {"description": "Site clearing", "unit": "m3", "quantity": 1000.0, "unit_price": 15.00},
    {"description": "Compacted fill", "unit": "m3", "quantity": 2500.5, "unit_price": 5.00},
    {"description": "Reinforcing steel", "unit": "kg", "quantity": 12000.0, "unit_price": 1.75},
]


def line_total(item):
    """Return quantity * unit price for one item, rounded to 2 decimals."""
    raise NotImplementedError


def bill_total(items, vat_rate=0.13):
    """Return a dict with 'subtotal', 'vat' and 'total', each rounded to 2 decimals."""
    raise NotImplementedError


if __name__ == "__main__":
    # These checks tell you if your code is correct.
    assert line_total(items[0]) == 15000.0, "line_total is wrong"
    result = bill_total(items)
    assert result["subtotal"] == 15000.0 + 12502.5 + 21000.0, "subtotal is wrong"
    assert result["vat"] == round(result["subtotal"] * 0.13, 2), "vat is wrong"
    assert result["total"] == round(result["subtotal"] + result["vat"], 2), "total is wrong"
    print("All checks passed! / Todo correcto!")
    print(result)
