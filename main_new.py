import csv
import os
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, LETTER
from PIL import Image
import qrcode

# --- Settings ---
paper_size_name = 'LETTER'  # or 'A4'
paper_size = A4 if paper_size_name == 'A4' else LETTER

font = "Helvetica-Bold"
exportname = "all_cards_on_a4.pdf"
card_width_mm = 85.60
card_height_mm = 53.98
card_width_pt = card_width_mm * mm
card_height_pt = card_height_mm * mm
corner_radius = 3 * mm  # Rounded corner radius

# Margins and spacing
margin_x = 22.5 * mm
margin_y = 29 * mm
gap_x = 0 * mm
gap_y = 0 * mm

# Load logo
logo_path = 'logo.png'
photos_dir = './photos/'    # folder with photos
fallback_photo = 'sb.jpg'   # default photo if missing
logo_img = Image.open(logo_path)

# Output PDF
pdf_filename = exportname
c = canvas.Canvas(pdf_filename, pagesize=paper_size)
page_width, page_height = paper_size

# Compute grid: how many cards fit horizontally & vertically
cards_per_row = int((page_width - 2 * margin_x + gap_x) // (card_width_pt + gap_x))
cards_per_col = int((page_height - 2 * margin_y + gap_y) // (card_height_pt + gap_y))

cards_per_row = 2
cards_per_col = 4

# --- Read CSV and draw cards ---
with open('employees.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    x_idx = 0
    y_idx = 0

    for row in reader:
        first_name = row['first_name']
        last_name = row['last_name']
        job_title = row['job_title']
        photo_id = (row.get('photo') or '').strip()
        photo_file = f"{photo_id}.jpg"
        full_name = f"{first_name} {last_name}"
        if photo_id == '':
            print(f'❌ geted{full_name, job_title, "---no photo, used default---"}')
        else:
            print(f'✅ geted{full_name, job_title, photo_file}')

        # Compute position on page
        pos_x = margin_x + x_idx * (card_width_pt + gap_x)
        pos_y = page_height - margin_y - (y_idx+1) * card_height_pt - y_idx * gap_y

        # Draw card background
        # c.setFillColorRGB(0.9, 0.9, 1)  # light blue
        c.setFillColorRGB(1, 1, 1)

        # Draw vertical center line
        # c.setStrokeColor(colors.grey)
        # c.setLineWidth(0.3 * mm)
        # center_x = page_width / 2
        # c.line(center_x, margin_y / 2, center_x, page_height - margin_y / 2)
        ############################

        c.roundRect(pos_x, pos_y, card_width_pt, card_height_pt, corner_radius, fill=True, stroke=True)

        # Draw logo top-left
        logo_w, logo_h = logo_img.size
        aspect = logo_h / logo_w
        logo_target_w = 36 * mm
        logo_target_h = logo_target_w * aspect
        c.drawInlineImage(logo_path, pos_x + 5*mm, pos_y + card_height_pt - logo_target_h - 5*mm,
                          width=logo_target_w, height=logo_target_h)

        # Draw personal photo top-right
        photo_path = os.path.join(photos_dir, photo_file)
        if not os.path.isfile(photo_path):
            photo_path = os.path.join(photos_dir, fallback_photo)
        try:
            photo_img = Image.open(photo_path)
            photo_target_w = 18 * mm
            aspect = photo_img.height / photo_img.width
            photo_target_h = photo_target_w * aspect
            photo_x = pos_x + card_width_pt - photo_target_w - 3*mm
            photo_y = pos_y + card_height_pt - photo_target_h - 3*mm
            c.drawInlineImage(photo_path, photo_x, photo_y, width=photo_target_w, height=photo_target_h)
        except Exception as e:
            print(f"⚠ Failed to draw photo: {photo_path}")

        # Auto-fit name font size
        max_font = 24
        min_font = 18
        font_size = max_font
        available_width = card_width_pt - 20*mm
        while c.stringWidth(full_name, font, font_size) > available_width and font_size > min_font:
            font_size -= 1
        c.setFont(font, font_size)
        c.setFillColor(colors.black)

        # Draw name centered
        name_x = pos_x + card_width_pt / 2
        name_y = pos_y + card_height_pt / 2 - 3*mm
        c.drawCentredString(name_x, name_y, full_name)

        # Auto-fit job title font size
        max_job_font = 14
        min_job_font = 12
        job_font_size = max_job_font
        available_job_width = card_width_pt - 20 * mm

        while c.stringWidth(job_title, font, job_font_size) > available_job_width and job_font_size > min_job_font:
            job_font_size -= 1



        if len(job_title) > 15:
            # Still too long → split into two lines
            words = job_title.split()
            half = len(words) // 2
            if half == 0:
                lines = [job_title]
            else:
                lines = [' '.join(words[:half]), ' '.join(words[half:])]

            c.setFont(font, job_font_size)
            line_spacing = job_font_size + 1  # small gap between lines
            start_y = pos_y + card_height_pt / 2 - 15 * mm
            for i, line in enumerate(lines):
                c.drawCentredString(name_x, start_y - i * line_spacing, line)
        else:
            # Fits on one line
            c.setFont(font, job_font_size)
            job_y = pos_y + card_height_pt / 2 - 15 * mm
            c.drawCentredString(name_x, job_y, job_title)

        # c.setFont(font, job_font_size)
        # job_y = pos_y + card_height_pt / 2 - 10 * mm
        # c.drawCentredString(name_x, job_y, job_title)

        # Generate QR code
        qr_text = f"{full_name} - {job_title}"
        qr = qrcode.make(qr_text).convert("RGB")
        qr_target_size = 12 * mm
        c.drawInlineImage(qr, pos_x + card_width_pt - qr_target_size - 3*mm, pos_y + 3*mm,
                          width=qr_target_size, height=qr_target_size)

        # Move to next cell
        x_idx += 1
        if x_idx >= cards_per_row:
            x_idx = 0
            y_idx += 1
            if y_idx >= cards_per_col:
                c.showPage()
                y_idx = 0

# Save PDF
c.save()
print(f"✅ Generated: {pdf_filename}")
