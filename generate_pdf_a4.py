"""
Générateur de planche PDF A4 haute définition prête pour impression immédiate
Soutenance de Master MISEI - RAKOTONDRAIBE Manitra Harivony
"""

import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
import qrcode

def create_a4_pdf():
    current_dir = os.path.dirname(__file__)
    pdf_path = os.path.join(current_dir, "planche_etiquettes_A4.pdf")
    qrcodes_dir = os.path.join(current_dir, "qrcodes")
    os.makedirs(qrcodes_dir, exist_ok=True)

    base_url = "https://eduque-me.github.io/Qr"

    recipients = [
        {
            "id": 0,
            "name": "Mme RANDRIAMANANTANY Zely Arivelo",
            "role": "Présidente du Jury",
            "sub": "Professeur à la Faculté des Sciences",
            "tag": "HOMMAGE & RECONNAISSANCE"
        },
        {
            "id": 1,
            "name": "M. RAKOTOARIMANANA Liva Graffin",
            "role": "Encadreur Pédagogique",
            "sub": "Professeur, Resp. Parcours MISEI",
            "tag": "GRATITUDE & RESPECT"
        },
        {
            "id": 2,
            "name": "Monsieur CLERK",
            "role": "Examinateur du Jury",
            "sub": "Docteur en Physique",
            "tag": "TÉMOIGNAGE DE GRATITUDE"
        },
        {
            "id": 3,
            "name": "M. ANDRIANAIVO Rivo Nirina",
            "role": "Encadreur Professionnel",
            "sub": "Gérant de l'entreprise SNOVIBOX SARL",
            "tag": "PROFONDE RECONNAISSANCE"
        }
    ]

    # Générer les QR codes PNG temporaires haute résolution
    qr_images = []
    for r in recipients:
        url = f"{base_url}/?prof={r['id']}"
        qr = qrcode.QRCode(
            version=None,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=1
        )
        qr.add_data(url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="#1b2d21", back_color="white")
        path = os.path.join(qrcodes_dir, f"temp_qr_{r['id']}.png")
        img.save(path)
        qr_images.append(path)

    # Initialisation PDF A4
    c = canvas.Canvas(pdf_path, pagesize=A4)
    page_w, page_h = A4  # 210mm x 297mm

    # Marges et dimensions de chaque carte
    margin_x = 12 * mm
    margin_y = 12 * mm
    gap_x = 8 * mm
    gap_y = 10 * mm

    card_w = (page_w - 2 * margin_x - gap_x) / 2
    card_h = (page_h - 2 * margin_y - gap_y) / 2

    coords = [
        (margin_x, margin_y + card_h + gap_y),                   # Haut Gauche (Pot 1)
        (margin_x + card_w + gap_x, margin_y + card_h + gap_y),   # Haut Droite (Pot 2)
        (margin_x, margin_y),                                    # Bas Gauche (Pot 3)
        (margin_x + card_w + gap_x, margin_y)                    # Bas Droite (Pot 4)
    ]

    for idx, (x, y) in enumerate(coords):
        r = recipients[idx]
        qr_path = qr_images[idx]

        # Fond carte crème doux
        c.setFillColor(colors.HexColor("#faf7f2"))
        c.roundRect(x, y, card_w, card_h, 6 * mm, fill=1, stroke=0)

        # Ligne de découpe pointillée
        c.setStrokeColor(colors.HexColor("#a3beaa"))
        c.setLineWidth(0.8)
        c.setDash(4, 3)
        c.roundRect(x, y, card_w, card_h, 6 * mm, fill=0, stroke=1)
        c.setDash()  # reset dash

        # Cadre intérieur or
        c.setStrokeColor(colors.HexColor("#c5a045"))
        c.setLineWidth(1)
        pad = 4 * mm
        c.roundRect(x + pad, y + pad, card_w - 2 * pad, card_h - 2 * pad, 4 * mm, fill=0, stroke=1)

        # Repère de trou de suspension (si attache avec ficelle)
        hole_x = x + card_w / 2
        hole_y = y + card_h - pad - 4 * mm
        c.setStrokeColor(colors.HexColor("#c5a045"))
        c.circle(hole_x, hole_y, 2 * mm, fill=0, stroke=1)

        center_x = x + card_w / 2

        # En-tête institutionnel
        c.setFont("Helvetica-Bold", 7.5)
        c.setFillColor(colors.HexColor("#2a4031"))
        c.drawCentredString(center_x, y + card_h - 14 * mm, "UNIVERSITÉ D'ANTANANARIVO • MASTER MISEI")

        c.setFont("Helvetica", 6.5)
        c.setFillColor(colors.HexColor("#547d60"))
        c.drawCentredString(center_x, y + card_h - 18 * mm, "Soutenance de Diplôme d'Ingénieur • 2026")

        # Ruban Tag
        c.setFont("Helvetica-Bold", 7)
        c.setFillColor(colors.HexColor("#aa8233"))
        c.drawCentredString(center_x, y + card_h - 25 * mm, f"• {r['tag']} •")

        # Nom du professeur
        c.setFont("Times-Bold", 11)
        c.setFillColor(colors.HexColor("#1b2d21"))
        c.drawCentredString(center_x, y + card_h - 31 * mm, r["name"])

        # Rôle
        c.setFont("Helvetica-Bold", 9)
        c.setFillColor(colors.HexColor("#324f3b"))
        c.drawCentredString(center_x, y + card_h - 36 * mm, r["role"])

        # Détail académique
        c.setFont("Helvetica-Oblique", 7.5)
        c.setFillColor(colors.HexColor("#444444"))
        c.drawCentredString(center_x, y + card_h - 40 * mm, r["sub"])

        # QR Code
        qr_size = 46 * mm
        qr_x = center_x - qr_size / 2
        qr_y = y + 25 * mm
        c.drawImage(qr_path, qr_x, qr_y, width=qr_size, height=qr_size)

        # Instructions sous le QR code
        c.setFont("Helvetica-Bold", 7.5)
        c.setFillColor(colors.HexColor("#2a4031"))
        c.drawCentredString(center_x, y + 19.5 * mm, "Scannez avec votre smartphone")

        c.setFont("Helvetica", 6.2)
        c.setFillColor(colors.HexColor("#555555"))
        c.drawCentredString(center_x, y + 16 * mm, "Message personnel & Conseils d'entretien de la plante")

        # Verset biblique de bénédiction
        c.setFont("Times-Italic", 7.2)
        c.setFillColor(colors.HexColor("#aa8233"))
        c.drawCentredString(center_x, y + 11.5 * mm, "« Que l’Éternel te bénisse, et qu’il te garde ! » (Nb 6:24)")

        # Signature
        c.setStrokeColor(colors.HexColor("#dddddd"))
        c.setLineWidth(0.5)
        c.line(x + 10 * mm, y + 8.5 * mm, x + card_w - 10 * mm, y + 8.5 * mm)

        c.setFont("Helvetica", 6.2)
        c.setFillColor(colors.HexColor("#666666"))
        c.drawCentredString(center_x, y + 5 * mm, "Présenté par : RAKOTONDRAIBE Manitra Harivony")

    c.save()
    print(f"PDF généré avec succès : {pdf_path}")
    return pdf_path

if __name__ == "__main__":
    create_a4_pdf()
