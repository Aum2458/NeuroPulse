import qrcode
import os
from datetime import datetime
from typing import Optional

# -------------------------------------------------
# Constants
# -------------------------------------------------
QR_DIR = "static/qrcodes"

# -------------------------------------------------
# QR Generator
# -------------------------------------------------
def generate_qr(file_path: Optional[str]) -> Optional[str]:
    """
    Generates a QR code pointing to a file served by Flask.

    Args:
        file_path (str): e.g. 'static/reports/report_xyz.pdf'

    Returns:
        str | None: QR image path (e.g. 'static/qrcodes/qr_xxx.png')
    """
    if not file_path:
        return None

    os.makedirs(QR_DIR, exist_ok=True)

    # Normalize path for web usage
    relative_path = str(file_path).replace("\\", "/").lstrip("/")
    qr_url = f"/{relative_path}"

    # Unique filename
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    qr_filename = f"qr_{timestamp}.png"
    qr_full_path = os.path.join(QR_DIR, qr_filename)

    try:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=8,
            border=4
        )
        qr.add_data(qr_url)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        img.save(qr_full_path)

        print(f"✅ QR generated: {qr_full_path} -> {qr_url}")
        return qr_full_path
    except Exception as e:
        print(f"⚠️ QR generation failed: {e}")
        return None
