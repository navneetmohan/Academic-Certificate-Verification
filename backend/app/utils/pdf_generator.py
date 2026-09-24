import io
import os
import qrcode
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

def generate_qr_code_image(data: str) -> io.BytesIO:
    """Generates a QR code image as BytesIO stream"""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=4,
        border=1,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#0f172a", back_color="white")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return buf

def generate_certificate_pdf(
    certificate_id: str,
    student_name: str,
    student_id: str,
    degree: str,
    department: str,
    institution_name: str,
    graduation_year: int,
    issue_date: str,
    certificate_type: str = "Bachelor of Science",
    verification_base_url: str = "http://localhost:5173/verify"
) -> bytes:
    """
    Generates a high-resolution, professional academic certificate in PDF format.
    Returns raw PDF bytes.
    """
    buffer = io.BytesIO()
    width, height = landscape(letter)  # 11 x 8.5 inches (792 x 612 points)

    c = canvas.Canvas(buffer, pagesize=landscape(letter))
    c.setTitle(f"Academic Certificate - {certificate_id}")
    c.setAuthor(institution_name)
    c.setSubject(f"{degree} awarded to {student_name}")

    # Color palette
    navy_primary = colors.HexColor("#0f2744")
    gold_accent = colors.HexColor("#c59b27")
    slate_subtext = colors.HexColor("#334155")
    bg_tint = colors.HexColor("#fdfbf7")

    # 1. Subtle background fill
    c.setFillColor(bg_tint)
    c.rect(0, 0, width, height, fill=1, stroke=0)

    # 2. Outer decorative border
    c.setStrokeColor(navy_primary)
    c.setLineWidth(3)
    c.rect(20, 20, width - 40, height - 40)

    # Inner decorative border (gold)
    c.setStrokeColor(gold_accent)
    c.setLineWidth(1.5)
    c.rect(26, 26, width - 52, height - 52)

    # Thin innermost line
    c.setStrokeColor(navy_primary)
    c.setLineWidth(0.5)
    c.rect(30, 30, width - 60, height - 60)

    # Corner decorations
    c.setFillColor(gold_accent)
    corner_size = 12
    # Top-left, top-right, bottom-left, bottom-right squares
    c.rect(23, height - 35, corner_size, corner_size, fill=1, stroke=0)
    c.rect(width - 35, height - 35, corner_size, corner_size, fill=1, stroke=0)
    c.rect(23, 23, corner_size, corner_size, fill=1, stroke=0)
    c.rect(width - 35, 23, corner_size, corner_size, fill=1, stroke=0)

    # 3. Institution Header
    c.setFillColor(navy_primary)
    c.setFont("Helvetica-Bold", 24)
    c.drawCentredString(width / 2.0, height - 75, institution_name.upper())

    c.setFillColor(gold_accent)
    c.setFont("Helvetica-Bold", 10)
    c.drawCentredString(width / 2.0, height - 92, "OFFICIAL ACADEMIC CREDENTIAL & DIPLOMA")

    # Decorative divider line
    c.setStrokeColor(gold_accent)
    c.setLineWidth(1)
    c.line(width / 2.0 - 150, height - 102, width / 2.0 + 150, height - 102)

    # 4. Certificate Body
    c.setFillColor(slate_subtext)
    c.setFont("Times-Italic", 14)
    c.drawCentredString(width / 2.0, height - 135, "This is to certify that")

    # Student Name
    c.setFillColor(navy_primary)
    c.setFont("Helvetica-Bold", 26)
    c.drawCentredString(width / 2.0, height - 172, student_name)

    # Student ID / Reg
    c.setFillColor(slate_subtext)
    c.setFont("Helvetica", 10)
    c.drawCentredString(width / 2.0, height - 192, f"Student Identification: {student_id}")

    # Conferral text
    c.setFont("Times-Roman", 13)
    c.drawCentredString(
        width / 2.0,
        height - 225,
        "having successfully fulfilled all academic curriculum and statutory requirements is hereby conferred the degree of"
    )

    # Degree Name
    c.setFillColor(navy_primary)
    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(width / 2.0, height - 258, degree)

    # Department & Honors
    c.setFillColor(slate_subtext)
    c.setFont("Helvetica", 12)
    c.drawCentredString(width / 2.0, height - 280, f"Department of {department}")

    c.setFont("Times-Italic", 11)
    c.drawCentredString(
        width / 2.0,
        height - 302,
        f"with all honors, rights, and privileges pertaining thereto in the Class of {graduation_year}."
    )

    # 5. Metadata Bar (Certificate ID, Date, Verification)
    meta_box_y = height - 370
    c.setStrokeColor(colors.HexColor("#e2e8f0"))
    c.setFillColor(colors.HexColor("#f8fafc"))
    c.roundRect(50, meta_box_y, width - 100, 48, 6, fill=1, stroke=1)

    c.setFillColor(slate_subtext)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(70, meta_box_y + 28, "CERTIFICATE ID:")
    c.setFont("Courier-Bold", 10)
    c.setFillColor(navy_primary)
    c.drawString(70, meta_box_y + 12, certificate_id)

    c.setFillColor(slate_subtext)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(280, meta_box_y + 28, "CONFERRAL DATE:")
    c.setFont("Helvetica", 10)
    c.setFillColor(navy_primary)
    c.drawString(280, meta_box_y + 12, issue_date)

    c.setFillColor(slate_subtext)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(460, meta_box_y + 28, "SECURITY STATUS:")
    c.setFont("Helvetica-Bold", 9)
    c.setFillColor(colors.HexColor("#166534")) # Dark green
    c.drawString(460, meta_box_y + 12, "IMMUTABLE BLOCKCHAIN REGISTRATION")

    # 6. Embedded QR Code
    verify_url = f"{verification_base_url}/{certificate_id}"
    qr_img_stream = generate_qr_code_image(verify_url)
    qr_image = ImageReader(qr_img_stream)

    qr_size = 90
    qr_x = width - 155
    qr_y = 52
    c.drawImage(qr_image, qr_x, qr_y, width=qr_size, height=qr_size)

    c.setFillColor(slate_subtext)
    c.setFont("Helvetica", 7.5)
    c.drawCentredString(qr_x + (qr_size / 2.0), qr_y - 10, "Scan to Verify Authenticity")

    # 7. Official Signatures Section
    sig_line_y = 85
    c.setStrokeColor(slate_subtext)
    c.setLineWidth(1)

    # University President
    c.line(80, sig_line_y, 230, sig_line_y)
    c.setFillColor(navy_primary)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(80, sig_line_y - 15, "Dr. Eleanor Vance")
    c.setFillColor(slate_subtext)
    c.setFont("Helvetica", 8)
    c.drawString(80, sig_line_y - 27, "President & Vice-Chancellor")

    # Dean / Registrar
    c.line(290, sig_line_y, 440, sig_line_y)
    c.setFillColor(navy_primary)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(290, sig_line_y - 15, "Prof. Marcus Thorne")
    c.setFillColor(slate_subtext)
    c.setFont("Helvetica", 8)
    c.drawString(290, sig_line_y - 27, "Dean of Academic Affairs")

    # 8. Cryptographic Integrity Seal
    seal_x = 525
    seal_y = 82
    c.setStrokeColor(gold_accent)
    c.setLineWidth(2)
    c.circle(seal_x, seal_y, 30, fill=0, stroke=1)
    c.setLineWidth(0.8)
    c.circle(seal_x, seal_y, 26, fill=0, stroke=1)
    c.setFillColor(gold_accent)
    c.setFont("Helvetica-Bold", 6.5)
    c.drawCentredString(seal_x, seal_y + 8, "OFFICIAL SEAL")
    c.setFont("Helvetica", 5.5)
    c.drawCentredString(seal_x, seal_y - 2, "VERIFIED")
    c.drawCentredString(seal_x, seal_y - 10, "LEDGER PROOF")

    c.showPage()
    c.save()

    buffer.seek(0)
    return buffer.getvalue()
