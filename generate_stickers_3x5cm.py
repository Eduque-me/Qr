"""
Generate simple QR codes for six recipients and print them as 3 x 5 cm stickers.
Names are intentionally not included: they can be written or attached by the user.
"""

import io
import os

import qrcode
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader


BASE_URL = "https://eduque-me.github.io/Qr"

RECIPIENTS = [
    {"id": 0, "filename": "pot_1_presidente_3x5cm.png"},
    {"id": 1, "filename": "pot_2_encadreur_ped_3x5cm.png"},
    {"id": 2, "filename": "pot_3_examinateur_3x5cm.png"},
    {"id": 3, "filename": "pot_4_encadreur_pro_ANDRIANAIVO_3x5cm.png"},
    {"id": 4, "filename": "pot_5_encadreur_pro_RALAMBOSOA_3x5cm.png"},
    {"id": 5, "filename": "pot_6_encadreur_pro_RANDRIAMANANTENA_3x5cm.png"},
]


def make_qr_image(recipient_id, pixel_size=1000):
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=4,
    )
    qr.add_data(f"{BASE_URL}/?prof={recipient_id}")
    qr.make(fit=True)
    image = qr.make_image(fill_color="black", back_color="white").convert("RGB")
    return image.resize((pixel_size, pixel_size), resample=3)


def generate_individual_pngs(out_dir):
    os.makedirs(out_dir, exist_ok=True)
    for recipient in RECIPIENTS:
        image = make_qr_image(recipient["id"])
        destination = os.path.join(out_dir, recipient["filename"])
        image.save(destination, dpi=(300, 300))
        print(f"QR code genere : {destination}")


def generate_pdf_a4(pdf_path):
    output = canvas.Canvas(pdf_path, pagesize=A4)
    page_width, page_height = A4

    sticker_width = 30 * mm
    sticker_height = 50 * mm
    gap_x = 12 * mm
    gap_y = 15 * mm
    columns = 4
    rows = 3

    grid_width = columns * sticker_width + (columns - 1) * gap_x
    grid_height = rows * sticker_height + (rows - 1) * gap_y
    start_x = (page_width - grid_width) / 2
    start_y = (page_height - grid_height) / 2
    ordered_recipients = RECIPIENTS * 2

    qr_images = {}
    for recipient in RECIPIENTS:
        image = make_qr_image(recipient["id"])
        buffer = io.BytesIO()
        image.save(buffer, format="PNG")
        buffer.seek(0)
        qr_images[recipient["id"]] = buffer

    for index, recipient in enumerate(ordered_recipients):
        row = index // columns
        column = index % columns
        x = start_x + column * (sticker_width + gap_x)
        y = start_y + (rows - 1 - row) * (sticker_height + gap_y)

        output.setStrokeColorRGB(0.65, 0.65, 0.65)
        output.setLineWidth(0.5)
        output.setDash(2, 2)
        output.rect(x, y, sticker_width, sticker_height, stroke=1, fill=0)
        output.setDash()

        qr_size = 24 * mm
        qr_x = x + (sticker_width - qr_size) / 2
        qr_y = y + (sticker_height - qr_size) / 2
        qr_images[recipient["id"]].seek(0)
        output.drawImage(
            ImageReader(qr_images[recipient["id"]]),
            qr_x,
            qr_y,
            width=qr_size,
            height=qr_size,
            preserveAspectRatio=True,
            mask=None,
        )

    output.save()
    print(f"PDF genere : {pdf_path}")


def generate_html_print_page(html_path):
    stickers = ""
    for recipient in RECIPIENTS * 2:
        stickers += (
            '<div class="sticker"><img src="stickers_3x5cm/'
            f'{recipient["filename"]}" alt="QR code destinataire"></div>\n'
        )

    html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Planche QR codes 3 x 5 cm</title>
<style>
@page {{ size: A4 portrait; margin: 0; }}
* {{ box-sizing: border-box; }}
body {{ margin: 0; background: #fff; font-family: Arial, sans-serif; }}
.toolbar {{ padding: 16px; text-align: center; }}
.toolbar button {{ padding: 10px 18px; font-weight: bold; cursor: pointer; }}
.sheet {{
  width: 210mm; min-height: 297mm; margin: 0 auto; padding: 33mm 18mm;
  display: grid; grid-template-columns: repeat(4, 30mm); grid-template-rows: repeat(3, 50mm);
  gap: 15mm 12mm; justify-content: center;
}}
.sticker {{
  width: 30mm; height: 50mm; border: 0.2mm dashed #999;
  display: flex; align-items: center; justify-content: center;
  page-break-inside: avoid;
}}
.sticker img {{ width: 24mm; height: 24mm; display: block; }}
@media print {{
  .toolbar {{ display: none; }}
  .sheet {{ width: 210mm; height: 297mm; min-height: 297mm; }}
}}
</style>
</head>
<body>
<div class="toolbar">
  <button onclick="window.print()">Imprimer la planche</button>
</div>
<div class="sheet">
{stickers}
</div>
</body>
</html>
"""
    with open(html_path, "w", encoding="utf-8") as file:
        file.write(html)
    print(f"HTML genere : {html_path}")


if __name__ == "__main__":
    current_dir = os.path.dirname(__file__)
    output_dir = os.path.join(current_dir, "stickers_3x5cm")
    generate_individual_pngs(output_dir)
    generate_pdf_a4(os.path.join(current_dir, "planche_stickers_3x5cm.pdf"))
    generate_html_print_page(os.path.join(current_dir, "stickers_3x5cm.html"))
