# 🪪 Employee Badge Generator (PDF)

This Python script generates printable employee ID cards in PDF format using data from a CSV file. Each card includes the employee's **name**, **job title**, **photo**, **company logo**, and a **QR code**.

---

## 📦 Requirements

Install required Python packages:

```bash
pip install reportlab pillow qrcode

📄 What Each Card Contains
Company Logo (top-left)

Personal Photo (top-right)

Full Name (auto-scaled)

Job Title (single or multiline)

QR Code (bottom-right, contains Full Name - Job Title)

Rounded corners

🛠 Notes
The script supports both A4 and LETTER paper sizes.

Font sizes auto-fit to prevent text overflow.

Cards are sized to match standard ID card dimensions (85.60mm × 53.98mm).

The PDF is optimized for printing.

📄 License
MIT License — Free for personal or commercial use.


## 📦 Create exe file for Windows
pyinstaller --noconsole --add-data "photos;photos" --add-data "emp.csv;emp.csv" --add-data "logo-usko.png;logo-usko.png" --icon=icon.ico main.py
