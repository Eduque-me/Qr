"""
Générateur de QR codes haute définition et étiquettes pour les 4 pots de fleur
Soutenance de Master MISEI - RAKOTONDRAIBE Manitra Harivony
"""

import os
import qrcode
from PIL import Image, ImageDraw, ImageFont

def generate_qrcodes(base_url="https://eduque-me.github.io/Qr"):
    output_dir = os.path.join(os.path.dirname(__file__), "qrcodes")
    os.makedirs(output_dir, exist_ok=True)

    recipients = [
        {
            "id": 0,
            "filename": "pot_1_prof_RANDRIAMANANTANY.png",
            "name": "Mme RANDRIAMANANTANY Zely Arivelo",
            "role": "Présidente du Jury",
            "desc": "Professeur à la Faculté des Sciences"
        },
        {
            "id": 1,
            "filename": "pot_2_prof_RAKOTOARIMANANA.png",
            "name": "M. RAKOTOARIMANANA Liva Graffin",
            "role": "Encadreur Pédagogique",
            "desc": "Professeur, Resp. Parcours MISEI"
        },
        {
            "id": 2,
            "filename": "pot_3_dr_CLERK.png",
            "name": "Monsieur CLERK",
            "role": "Examinateur du Jury",
            "desc": "Docteur en Physique"
        },
        {
            "id": 3,
            "filename": "pot_4_mr_ANDRIANAIVO.png",
            "name": "M. ANDRIANAIVO Rivo Nirina",
            "role": "Encadreur Professionnel",
            "desc": "Gérant SNOVIBOX SARL"
        }
    ]

    generated_files = []

    for item in recipients:
        url = f"{base_url.rstrip('/')}/?prof={item['id']}"
        
        # Génération du QR Code avec correction d'erreur élevée (H) pour scan facile même si petit
        qr = qrcode.QRCode(
            version=None,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=12,
            border=2,
        )
        qr.add_data(url)
        qr.make(fit=True)

        # Image QR Code en vert botanique foncé chic (#1b2d21) sur fond blanc
        qr_img = qr.make_image(fill_color="#1b2d21", back_color="white").convert("RGBA")
        
        # Sauvegarde simple du QR Code seul
        qr_path = os.path.join(output_dir, f"qrcode_{item['id']}.png")
        qr_img.save(qr_path)

        # Création d'une étiquette complète prête à imprimer (format carte chic ~ 600x900 px)
        card_w, card_h = 700, 950
        card = Image.new("RGBA", (card_w, card_h), (250, 247, 242, 255))
        draw = ImageDraw.Draw(card)

        # Bordure dorée / élégante
        margin = 25
        draw.rounded_rectangle(
            [(margin, margin), (card_w - margin, card_h - margin)],
            radius=24,
            outline=(197, 160, 69, 255),
            width=3
        )
        # Ligne intérieure fine
        draw.rounded_rectangle(
            [(margin + 10, margin + 10), (card_w - margin - 10, card_h - margin - 10)],
            radius=18,
            outline=(202, 218, 203, 180),
            width=1
        )

        # Pastille pour trou de suspension (si accroché au pot avec ficelle)
        hole_x, hole_y = card_w // 2, margin + 25
        draw.ellipse([(hole_x - 14, hole_y - 14), (hole_x + 14, hole_y + 14)], outline=(197, 160, 69, 200), width=2)

        # Redimensionnement et collage du QR Code au centre
        qr_display_size = 360
        qr_resized = qr_img.resize((qr_display_size, qr_display_size), Image.Resampling.LANCZOS)
        qr_pos = ((card_w - qr_display_size) // 2, 340)
        card.paste(qr_resized, qr_pos, qr_resized)

        # Sauvegarde de la carte complète
        card_path = os.path.join(output_dir, item["filename"])
        card.save(card_path)
        generated_files.append((item["name"], card_path, url))
        print(f"Généré : {item['filename']} -> {url}")

    return generated_files

if __name__ == "__main__":
    generate_qrcodes()
