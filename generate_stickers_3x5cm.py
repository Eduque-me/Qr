"""
Générateur d'étiquettes 3 cm x 5 cm (30 mm x 50 mm)
pour cadeaux de soutenance - RAKOTONDRAIBE Manitra Harivony
Supporte les 6 destinataires :
- 3 membres du Jury universitaire (Présidente, Encadreur Pédagogique, Examinateur)
- 3 Encadreurs Professionnels chez SNOVIBOX SARL (M. ANDRIANAIVO, M. RALAMBOSOA, M. RANDRIAMANANTENA)
"""

import os
import io
import base64
import qrcode
from PIL import Image, ImageDraw, ImageFont
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

BASE_URL = "https://eduque-me.github.io/Qr"

RECIPIENTS = [
    {
        "id": 0,
        "role": "Présidente du Jury",
        "name_line1": "Mme RANDRIAMANANTANY",
        "name_line2": "Zely Arivelo",
        "full_name": "Mme RANDRIAMANANTANY Zely Arivelo",
        "filename": "pot_1_presidente_3x5cm.png"
    },
    {
        "id": 1,
        "role": "Encadreur Pédagogique",
        "name_line1": "M. RAKOTOARIMANANA",
        "name_line2": "Liva Graffin",
        "full_name": "M. RAKOTOARIMANANA Liva Graffin",
        "filename": "pot_2_encadreur_ped_3x5cm.png"
    },
    {
        "id": 2,
        "role": "Examinateur du Jury",
        "name_line1": "M. RANDRIANJAFINIARIVO",
        "name_line2": "Clerc",
        "full_name": "M. RANDRIANJAFINIARIVO Clerc",
        "filename": "pot_3_examinateur_3x5cm.png"
    },
    {
        "id": 3,
        "role": "Encadreur Professionnel",
        "name_line1": "M. ANDRIANAIVO",
        "name_line2": "Rivo Nirina (Gérant)",
        "full_name": "M. ANDRIANAIVO Rivo Nirina",
        "filename": "pot_4_encadreur_pro_ANDRIANAIVO_3x5cm.png"
    },
    {
        "id": 4,
        "role": "Encadreur Professionnel",
        "name_line1": "M. RALAMBOSOA",
        "name_line2": "Toavina",
        "full_name": "M. RALAMBOSOA Toavina",
        "filename": "pot_5_encadreur_pro_RALAMBOSOA_3x5cm.png"
    },
    {
        "id": 5,
        "role": "Encadreur Professionnel",
        "name_line1": "M. RANDRIAMANANTENA",
        "name_line2": "Herman",
        "full_name": "M. RANDRIAMANANTENA Herman",
        "filename": "pot_6_encadreur_pro_RANDRIAMANANTENA_3x5cm.png"
    }
]

def generate_individual_pngs(out_dir):
    os.makedirs(out_dir, exist_ok=True)
    w_px = int(30 * 11.811)  # 354 px
    h_px = int(50 * 11.811)  # 590 px

    for r in RECIPIENTS:
        img = Image.new("RGB", (w_px, h_px), "#faf7f2")
        draw = ImageDraw.Draw(img)

        # Cadre intérieur or
        draw.rounded_rectangle([(8, 8), (w_px - 9, h_px - 9)], radius=12, outline="#c5a045", width=2)
        # Pointillés de découpe
        draw.rectangle([(0, 0), (w_px - 1, h_px - 1)], outline="#b8cebf", width=1)

        # Générer QR code
        url = f"{BASE_URL}/?prof={r['id']}"
        qr = qrcode.QRCode(
            version=None,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=6,
            border=1,
        )
        qr.add_data(url)
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="#1b2d21", back_color="#faf7f2").convert("RGB")
        qr_size = int(22 * 11.811)
        qr_img = qr_img.resize((qr_size, qr_size), Image.Resampling.LANCZOS)

        qr_x = (w_px - qr_size) // 2
        qr_y = 155
        img.paste(qr_img, (qr_x, qr_y))

        try:
            f_role = ImageFont.truetype("arialbd.ttf", 17)
            f_name1 = ImageFont.truetype("arialbd.ttf", 19)
            f_name2 = ImageFont.truetype("arial.ttf", 17)
            f_scan = ImageFont.truetype("arialbd.ttf", 16)
            f_sub = ImageFont.truetype("arial.ttf", 14)
            f_author = ImageFont.truetype("arialbd.ttf", 16)
        except:
            f_role = ImageFont.load_default()
            f_name1 = ImageFont.load_default()
            f_name2 = ImageFont.load_default()
            f_scan = ImageFont.load_default()
            f_sub = ImageFont.load_default()
            f_author = ImageFont.load_default()

        # En-tête
        draw.text((w_px // 2, 28), r['role'].upper(), fill="#876226", font=f_role, anchor="mm")
        draw.text((w_px // 2, 60), r['name_line1'], fill="#1b2d21", font=f_name1, anchor="mm")
        draw.text((w_px // 2, 90), r['name_line2'], fill="#2c422e", font=f_name2, anchor="mm")

        # Séparateur
        draw.line([(35, 120), (w_px - 35, 120)], fill="#dfcf89", width=1)
        draw.text((w_px // 2, 138), "• SCANNEZ-MOI •", fill="#568058", font=f_scan, anchor="mm")

        # Bas
        draw.line([(35, qr_y + qr_size + 16), (w_px - 35, qr_y + qr_size + 16)], fill="#dfcf89", width=1)
        draw.text((w_px // 2, h_px - 65), "Soutenance Master MISEI 2026", fill="#568058", font=f_sub, anchor="mm")
        draw.text((w_px // 2, h_px - 35), "Manitra RAKOTONDRAIBE", fill="#1b2d21", font=f_author, anchor="mm")

        dest = os.path.join(out_dir, r['filename'])
        img.save(dest, dpi=(300, 300))
        print(f"Image 3x5cm générée : {dest}")

def generate_pdf_a4(pdf_path):
    c = canvas.Canvas(pdf_path, pagesize=A4)
    page_w, page_h = A4  # 210mm x 297mm

    tag_w = 30 * mm
    tag_h = 50 * mm

    # Disposition sur A4 : 4 colonnes x 3 rangées = 12 étiquettes (2 exemplaires complets des 6 destinataires)
    # 2 sets ordonnés :
    # Set 1 : [0, 1, 2, 3, 4, 5]
    # Set 2 : [0, 1, 2, 3, 4, 5]
    ordered_items = RECIPIENTS * 2  # 12 items

    cols = 4
    rows = 3
    gap_x = 12 * mm
    gap_y = 15 * mm

    total_grid_w = cols * tag_w + (cols - 1) * gap_x
    total_grid_h = rows * tag_h + (rows - 1) * gap_y

    start_x = (page_w - total_grid_w) / 2
    start_y = (page_h - total_grid_h) / 2 - 5 * mm

    # En-tête A4
    c.setFont("Helvetica-Bold", 13)
    c.setFillColor(colors.HexColor("#1b2d21"))
    c.drawCentredString(page_w / 2, page_h - 20 * mm, "Planche d'Étiquettes 3 cm × 5 cm (30 mm × 50 mm) — 6 Destinataires")
    
    c.setFont("Helvetica", 8.5)
    c.setFillColor(colors.HexColor("#568058"))
    c.drawCentredString(page_w / 2, page_h - 26 * mm, "Jury & Encadrants SNOVIBOX • Soutenance Master MISEI 2026 • RAKOTONDRAIBE Manitra H.")

    c.setFont("Helvetica-Oblique", 7.8)
    c.setFillColor(colors.HexColor("#876226"))
    c.drawCentredString(page_w / 2, page_h - 31 * mm, "⚠️ IMPRESSION : Choisir 'Taille réelle' ou 100% (Ne PAS cocher 'Ajuster à la page') pour avoir 3×5 cm exacts.")

    # Pré-générer les QR codes
    qr_images = {}
    for r in RECIPIENTS:
        url = f"{BASE_URL}/?prof={r['id']}"
        qr = qrcode.QRCode(
            version=None,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=6,
            border=1
        )
        qr.add_data(url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="#1b2d21", back_color="#faf7f2")
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        buf.seek(0)
        qr_images[r['id']] = buf

    # Dessiner les 12 cartes
    for idx, r in enumerate(ordered_items):
        row_idx = idx // cols
        col_idx = idx % cols

        x = start_x + col_idx * (tag_w + gap_x)
        y = start_y + (rows - 1 - row_idx) * (tag_h + gap_y)
        qr_buf = qr_images[r['id']]

        # Fond crème
        c.setFillColor(colors.HexColor("#faf7f2"))
        c.roundRect(x, y, tag_w, tag_h, 2.5 * mm, fill=1, stroke=0)

        # Repères de découpe pointillés (exactement 30 x 50 mm)
        c.setStrokeColor(colors.HexColor("#8fae98"))
        c.setLineWidth(0.5)
        c.setDash(2.5, 2)
        c.rect(x, y, tag_w, tag_h, fill=0, stroke=1)
        c.setDash()

        # Cadre intérieur doré
        pad = 1.8 * mm
        c.setStrokeColor(colors.HexColor("#c5a045"))
        c.setLineWidth(0.6)
        c.roundRect(x + pad, y + pad, tag_w - 2 * pad, tag_h - 2 * pad, 2 * mm, fill=0, stroke=1)

        center_x = x + tag_w / 2

        # Rôle
        c.setFont("Helvetica-Bold", 4.7)
        c.setFillColor(colors.HexColor("#876226"))
        c.drawCentredString(center_x, y + tag_h - 4.5 * mm, r["role"].upper())

        # Nom Ligne 1
        c.setFont("Helvetica-Bold", 5.5)
        c.setFillColor(colors.HexColor("#1b2d21"))
        c.drawCentredString(center_x, y + tag_h - 7.5 * mm, r["name_line1"])

        # Nom Ligne 2
        c.setFont("Helvetica", 5.1)
        c.setFillColor(colors.HexColor("#2c422e"))
        c.drawCentredString(center_x, y + tag_h - 10.2 * mm, r["name_line2"])

        # Ligne fine dorée
        c.setStrokeColor(colors.HexColor("#dfcf89"))
        c.setLineWidth(0.4)
        c.line(x + 4 * mm, y + tag_h - 11.5 * mm, x + tag_w - 4 * mm, y + tag_h - 11.5 * mm)

        # Texte Scannez-moi
        c.setFont("Helvetica-Bold", 4.4)
        c.setFillColor(colors.HexColor("#416543"))
        c.drawCentredString(center_x, y + tag_h - 13.8 * mm, "• SCANNEZ-MOI 🌱 •")

        # QR Code (21.5 mm x 21.5 mm)
        qr_size = 21.5 * mm
        qr_x = center_x - qr_size / 2
        qr_y = y + 10 * mm
        qr_buf.seek(0)
        c.drawImage(ImageReader(qr_buf), qr_x, qr_y, width=qr_size, height=qr_size)

        # Ligne sous QR
        c.line(x + 4 * mm, y + 8.8 * mm, x + tag_w - 4 * mm, y + 8.8 * mm)

        # Bas de carte
        c.setFont("Helvetica", 4.2)
        c.setFillColor(colors.HexColor("#568058"))
        c.drawCentredString(center_x, y + 6.2 * mm, "Master MISEI • 2026")

        c.setFont("Helvetica-Bold", 4.4)
        c.setFillColor(colors.HexColor("#1b2d21"))
        c.drawCentredString(center_x, y + 3.8 * mm, "M. RAKOTONDRAIBE")

    c.save()
    print(f"PDF 3x5cm A4 généré avec succès : {pdf_path}")

def generate_html_a4(html_path):
    all_cards = []
    
    b64_map = {}
    for r in RECIPIENTS:
        url = f"{BASE_URL}/?prof={r['id']}"
        qr = qrcode.QRCode(version=None, error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=6, border=1)
        qr.add_data(url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="#1b2d21", back_color="#faf7f2")
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        b64_map[r['id']] = base64.b64encode(buf.getvalue()).decode()

    ordered_items = RECIPIENTS * 2  # 12 stickers (2 exemplaires chacun)

    for r in ordered_items:
        all_cards.append(f"""        <div class="sticker">
            <div class="inner-frame">
                <div class="role">{r['role']}</div>
                <div class="name-1">{r['name_line1']}</div>
                <div class="name-2">{r['name_line2']}</div>
                <div class="divider"></div>
                <div class="scan-label">• SCANNEZ-MOI 🌱 •</div>
                <div class="qr-wrapper">
                    <img src="data:image/png;base64,{b64_map[r['id']]}" alt="QR Code" />
                </div>
                <div class="divider-bottom"></div>
                <div class="univ">Master MISEI • 2026</div>
                <div class="author">M. RAKOTONDRAIBE</div>
            </div>
        </div>""")

    joined_cards = "\n".join(all_cards)

    content = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Planche d'Étiquettes 3 cm x 5 cm (30 mm x 50 mm) — 6 Destinataires</title>
    <style>
        @page {{
            size: A4 portrait;
            margin: 10mm 10mm;
        }}
        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
            background: #eef2ef;
            color: #1b2d21;
            padding: 20px;
            display: flex;
            flex-direction: column;
            align-items: center;
        }}
        .no-print {{
            background: white;
            padding: 16px 24px;
            border-radius: 12px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.08);
            margin-bottom: 25px;
            max-width: 780px;
            width: 100%;
            text-align: center;
        }}
        .no-print h1 {{
            font-size: 18px;
            color: #1b2d21;
            margin-bottom: 6px;
        }}
        .no-print p {{
            font-size: 13px;
            color: #568058;
            margin-bottom: 12px;
        }}
        .btn-print {{
            background: #2a4031;
            color: white;
            border: none;
            padding: 10px 22px;
            font-size: 14px;
            font-weight: 600;
            border-radius: 8px;
            cursor: pointer;
            transition: background 0.2s;
        }}
        .btn-print:hover {{
            background: #1b2d21;
        }}
        .instructions {{
            margin-top: 10px;
            font-size: 11px;
            color: #876226;
            background: #fdfaf3;
            padding: 8px 12px;
            border-radius: 6px;
            border: 1px solid #eddcb2;
            text-align: left;
            display: inline-block;
        }}

        .a4-sheet {{
            width: 210mm;
            min-height: 297mm;
            background: white;
            padding: 12mm 10mm;
            box-shadow: 0 4px 25px rgba(0,0,0,0.12);
            display: flex;
            flex-direction: column;
            align-items: center;
        }}
        .sheet-header {{
            text-align: center;
            margin-bottom: 7mm;
        }}
        .sheet-header h2 {{
            font-size: 13pt;
            color: #1b2d21;
            font-weight: bold;
        }}
        .sheet-header p {{
            font-size: 8pt;
            color: #568058;
            margin-top: 2px;
        }}

        .stickers-grid {{
            display: grid;
            grid-template-columns: repeat(4, 30mm);
            grid-template-rows: repeat(3, 50mm);
            gap: 15mm 12mm;
            justify-content: center;
        }}

        .sticker {{
            width: 30mm;
            height: 50mm;
            background: #faf7f2;
            border: 0.25mm dashed #8fae98;
            border-radius: 2.5mm;
            padding: 1.2mm;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            position: relative;
            page-break-inside: avoid;
        }}
        .inner-frame {{
            width: 100%;
            height: 100%;
            border: 0.25mm solid #c5a045;
            border-radius: 2mm;
            padding: 1mm 1.2mm;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: space-between;
            text-align: center;
        }}
        .role {{
            font-size: 4.7pt;
            font-weight: bold;
            color: #876226;
            text-transform: uppercase;
            letter-spacing: 0.2px;
            line-height: 1.1;
        }}
        .name-1 {{
            font-size: 5.5pt;
            font-weight: bold;
            color: #1b2d21;
            line-height: 1.1;
            margin-top: 0.3mm;
        }}
        .name-2 {{
            font-size: 5.1pt;
            color: #2c422e;
            line-height: 1.1;
        }}
        .divider {{
            width: 80%;
            height: 0.2mm;
            background: #dfcf89;
            margin: 0.5mm 0;
        }}
        .scan-label {{
            font-size: 4.2pt;
            font-weight: bold;
            color: #416543;
            letter-spacing: 0.2px;
            margin-bottom: 0.3mm;
        }}
        .qr-wrapper {{
            width: 21.5mm;
            height: 21.5mm;
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        .qr-wrapper img {{
            width: 21.5mm;
            height: 21.5mm;
            display: block;
        }}
        .divider-bottom {{
            width: 80%;
            height: 0.2mm;
            background: #dfcf89;
            margin: 0.5mm 0 0.3mm 0;
        }}
        .univ {{
            font-size: 4.1pt;
            color: #568058;
            line-height: 1.1;
        }}
        .author {{
            font-size: 4.3pt;
            font-weight: bold;
            color: #1b2d21;
            line-height: 1.1;
        }}

        @media print {{
            body {{
                background: white;
                padding: 0;
            }}
            .no-print {{
                display: none;
            }}
            .a4-sheet {{
                box-shadow: none;
                padding: 8mm 10mm;
                min-height: auto;
            }}
        }}
    </style>
</head>
<body>

<div class="no-print">
    <h1>🏷️ Planche d'Étiquettes Format Réel 3 cm × 5 cm (6 Destinataires)</h1>
    <p>12 étiquettes (2 exemplaires pour chacun des 6 membres du jury et encadrants SNOVIBOX).</p>
    <button class="btn-print" onclick="window.print()">🖨️ Imprimer la planche (Ctrl + P)</button>
    <div class="instructions">
        <strong>📏 CONSEIL POUR UNE TAILLE EXACTE À 100% :</strong><br>
        Dans la boîte d'impression du navigateur (Ctrl + P) :<br>
        • Échelle : <strong>100%</strong> ou <strong>Par défaut</strong> (Ne <u>pas</u> cocher « Ajuster à la page »).<br>
        • Marges : <strong>Aucune</strong> ou <strong>Par défaut</strong>.
    </div>
</div>

<div class="a4-sheet">
    <div class="sheet-header">
        <h2>Planche d'Étiquettes 30 mm × 50 mm (3 cm × 5 cm)</h2>
        <p>Jury Universitaire & Encadrants SNOVIBOX • Master MISEI 2026 • RAKOTONDRAIBE Manitra H.</p>
    </div>
    <div class="stickers-grid">
{joined_cards}
    </div>
</div>

</body>
</html>"""
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"HTML 3x5cm généré avec succès : {html_path}")

if __name__ == "__main__":
    base_dir = os.path.dirname(__file__)
    stickers_dir = os.path.join(base_dir, "stickers_3x5cm")
    pdf_out = os.path.join(base_dir, "planche_stickers_3x5cm.pdf")
    html_out = os.path.join(base_dir, "stickers_3x5cm.html")

    generate_individual_pngs(stickers_dir)
    generate_pdf_a4(pdf_out)
    generate_html_a4(html_out)
