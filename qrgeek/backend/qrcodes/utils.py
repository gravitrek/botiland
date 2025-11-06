"""
Utilities for QR code generation and processing.
"""
import io
import qrcode
from PIL import Image, ImageDraw
from django.core.files.base import ContentFile


def generate_qr_code(data, **options):
    """
    Generate QR code image from data.

    Args:
        data: The data to encode in QR code
        **options: QR code customization options
            - size: Size in pixels (default: 400)
            - foreground_color: Hex color (default: #000000)
            - background_color: Hex color (default: #FFFFFF)
            - error_correction: L, M, Q, or H (default: M)
            - logo: PIL Image object to embed
            - format: png or svg (default: png)

    Returns:
        ContentFile object with QR code image
    """
    # QR code options
    size = options.get('size', 400)
    fg_color = options.get('foreground_color', '#000000')
    bg_color = options.get('background_color', '#FFFFFF')
    error_correction_level = options.get('error_correction', 'M')
    logo = options.get('logo', None)
    output_format = options.get('format', 'png').lower()

    # Map error correction levels
    error_correction_map = {
        'L': qrcode.constants.ERROR_CORRECT_L,
        'M': qrcode.constants.ERROR_CORRECT_M,
        'Q': qrcode.constants.ERROR_CORRECT_Q,
        'H': qrcode.constants.ERROR_CORRECT_H,
    }

    # Create QR code
    qr = qrcode.QRCode(
        version=None,  # Auto-detect version
        error_correction=error_correction_map.get(
            error_correction_level,
            qrcode.constants.ERROR_CORRECT_M
        ),
        box_size=10,
        border=4,
    )

    qr.add_data(data)
    qr.make(fit=True)

    # Generate image
    img = qr.make_image(fill_color=fg_color, back_color=bg_color)
    img = img.convert('RGB')

    # Resize to requested size
    img = img.resize((size, size), Image.Resampling.LANCZOS)

    # Add logo if provided
    if logo:
        img = add_logo_to_qr(img, logo)

    # Save to buffer
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)

    return ContentFile(buffer.read())


def add_logo_to_qr(qr_img, logo_img, logo_size_ratio=0.3):
    """
    Add logo to the center of QR code.

    Args:
        qr_img: PIL Image of QR code
        logo_img: PIL Image of logo
        logo_size_ratio: Ratio of logo size to QR code size (default: 0.3)

    Returns:
        PIL Image with logo embedded
    """
    # Calculate logo size
    qr_width, qr_height = qr_img.size
    logo_max_size = int(min(qr_width, qr_height) * logo_size_ratio)

    # Resize logo maintaining aspect ratio
    logo_img = logo_img.convert('RGBA')
    logo_img.thumbnail((logo_max_size, logo_max_size), Image.Resampling.LANCZOS)

    # Create white background for logo
    logo_width, logo_height = logo_img.size
    logo_bg = Image.new('RGBA', (logo_width + 20, logo_height + 20), 'white')

    # Paste logo on background
    logo_bg.paste(logo_img, (10, 10), logo_img)

    # Calculate position (center)
    logo_pos = (
        (qr_width - logo_bg.width) // 2,
        (qr_height - logo_bg.height) // 2
    )

    # Paste logo on QR code
    qr_img = qr_img.convert('RGBA')
    qr_img.paste(logo_bg, logo_pos, logo_bg)

    return qr_img.convert('RGB')


def encode_vcard(data):
    """
    Encode vCard data for QR code.

    Args:
        data: Dictionary with vCard fields

    Returns:
        vCard formatted string
    """
    vcard = ["BEGIN:VCARD", "VERSION:3.0"]

    # Name
    if data.get('first_name') or data.get('last_name'):
        name = f"{data.get('last_name', '')};{data.get('first_name', '')}"
        vcard.append(f"N:{name}")
        vcard.append(f"FN:{data.get('first_name', '')} {data.get('last_name', '')}")

    # Organization
    if data.get('company'):
        vcard.append(f"ORG:{data['company']}")

    # Title
    if data.get('title'):
        vcard.append(f"TITLE:{data['title']}")

    # Phone
    if data.get('phone'):
        vcard.append(f"TEL:{data['phone']}")

    # Email
    if data.get('email'):
        vcard.append(f"EMAIL:{data['email']}")

    # Website
    if data.get('website'):
        vcard.append(f"URL:{data['website']}")

    # Address
    if data.get('address'):
        vcard.append(f"ADR:;;{data['address']}")

    vcard.append("END:VCARD")
    return "\n".join(vcard)


def encode_wifi(data):
    """
    Encode WiFi credentials for QR code.

    Args:
        data: Dictionary with WiFi fields (ssid, password, security_type, hidden)

    Returns:
        WiFi formatted string
    """
    ssid = data.get('ssid', '')
    password = data.get('password', '')
    security = data.get('security_type', 'WPA')
    hidden = 'true' if data.get('hidden', False) else 'false'

    return f"WIFI:T:{security};S:{ssid};P:{password};H:{hidden};;"


def encode_email(data):
    """
    Encode email for QR code.

    Args:
        data: Dictionary with email fields (to, subject, body)

    Returns:
        mailto URL
    """
    to = data.get('to', '')
    subject = data.get('subject', '')
    body = data.get('body', '')

    parts = [f"mailto:{to}"]
    if subject:
        parts.append(f"subject={subject}")
    if body:
        parts.append(f"body={body}")

    return "?".join(parts) if len(parts) > 1 else parts[0]


def encode_sms(data):
    """
    Encode SMS for QR code.

    Args:
        data: Dictionary with SMS fields (phone, message)

    Returns:
        SMS URL
    """
    phone = data.get('phone', '')
    message = data.get('message', '')

    if message:
        return f"SMSTO:{phone}:{message}"
    return f"SMSTO:{phone}"


def encode_location(data):
    """
    Encode GPS location for QR code.

    Args:
        data: Dictionary with location fields (latitude, longitude)

    Returns:
        geo URL
    """
    lat = data.get('latitude', 0)
    lng = data.get('longitude', 0)

    return f"geo:{lat},{lng}"


def get_qr_content(qr_code):
    """
    Get the actual content to encode based on QR type.

    Args:
        qr_code: QRCode model instance

    Returns:
        String to encode in QR code
    """
    qr_type = qr_code.qr_type
    content = qr_code.content

    if qr_type == 'url':
        return content.get('url', '')

    elif qr_type == 'vcard':
        return encode_vcard(content)

    elif qr_type == 'text':
        return content.get('text', '')

    elif qr_type == 'email':
        return encode_email(content)

    elif qr_type == 'sms':
        return encode_sms(content)

    elif qr_type == 'phone':
        return f"tel:{content.get('phone', '')}"

    elif qr_type == 'wifi':
        return encode_wifi(content)

    elif qr_type == 'location':
        return encode_location(content)

    elif qr_type == 'event':
        # For events, return URL to event page
        return content.get('url', '')

    elif qr_type == 'menu':
        # For menus, return URL to menu page
        return content.get('url', '')

    elif qr_type == 'product':
        # For products, return URL to product page
        return content.get('url', '')

    else:
        # Default: return URL or text
        return content.get('url') or content.get('text', '')
