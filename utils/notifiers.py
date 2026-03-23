import qrcode
import os

def generate_qr_code(pass_id: int) -> str:
    """Generates a QR code for a gate pass and returns the file path."""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(f"GATEPASS:{pass_id}")
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    
    # Ensure static/images directory exists
    os.makedirs(os.path.join("static", "images", "qrcodes"), exist_ok=True)
    
    filename = f"static/images/qrcodes/pass_{pass_id}.png"
    img.save(filename)
    return filename

def send_mock_sms(phone_or_parent: str, message: str):
    """Simulates sending an SMS."""
    print(f"--- MOCK SMS SENT ---")
    print(f"To: {phone_or_parent}")
    print(f"Message: {message}")
    print(f"---------------------")
    return True
