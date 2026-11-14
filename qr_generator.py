import qrcode
from qrcode.constants import ERROR_CORRECT_L, ERROR_CORRECT_M, ERROR_CORRECT_Q, ERROR_CORRECT_H
from PIL import Image

# Mapping for error correction levels
ERROR_CORRECTION_MAP = {
    "L (Low)": ERROR_CORRECT_L,
    "M (Medium)": ERROR_CORRECT_M,
    "Q (Quartile)": ERROR_CORRECT_Q,
    "H (High)": ERROR_CORRECT_H,
}

def generate_qr(data: str, *, version: int = 1, error_correction: str = "M (Medium)",
                box_size: int = 10, border: int = 4,
                fill_color: str = "black", back_color: str = "white") -> Image.Image:
    """Generate a QR code image.

    Args:
        data: The string data to encode.
        version: QR code size version (1 to 40). ``1`` is the smallest.
        error_correction: Human‑readable key from ``ERROR_CORRECTION_MAP``.
        box_size: Number of pixels for each "box" of the QR code.
        border: Border width (boxes).
        fill_color: Color for the QR modules.
        back_color: Background color.
    Returns:
        A Pillow ``Image`` instance ready for saving or displaying.
    """
    ec_level = ERROR_CORRECTION_MAP.get(error_correction, ERROR_CORRECT_M)
    qr = qrcode.QRCode(
        version=version,
        error_correction=ec_level,
        box_size=box_size,
        border=border,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color=fill_color, back_color=back_color).convert("RGB")
    return img

def format_wifi(ssid: str, password: str, encryption: str = "WPA") -> str:
    """Return a string formatted for Wi‑Fi QR codes.

    The format follows the widely‑used **WIFI** specification:
        ``WIFI:T:<encryption>;S:<ssid>;P:<password>;``
    ``encryption`` can be ``WPA``, ``WEP`` or empty for no password.
    """
    # Escape special characters ; , : in SSID/password according to spec
    esc = lambda s: s.replace('\\', '\\\\').replace(';', '\\;').replace(',', '\\,').replace(':', '\\:')
    ssid_esc = esc(ssid)
    pwd_esc = esc(password)
    return f"WIFI:T:{encryption};S:{ssid_esc};P:{pwd_esc};;"
