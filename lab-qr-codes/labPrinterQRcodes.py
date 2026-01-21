# pip install pandas qrcode[pil] pillow openpyxl

import pandas as pd
import qrcode
from PIL import Image, ImageDraw, ImageFont
import os

# Function to create a QR code with a label
def create_qr_with_label(url, label, output_dir, index):
    # Create a QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    # Create a new image with label
    img_with_label = Image.new('RGB', (img.size[0], img.size[1] + 50), 'white')
    img_with_label.paste(img, (0, 50))

    # Draw the label with dynamic font size
    draw = ImageDraw.Draw(img_with_label)
    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"  # Adjust path to your font file
    max_font_size = 20

    # Function to find appropriate font size
    def get_font_size(text, max_width):
        font_size = max_font_size
        while font_size > 10:
            font = ImageFont.truetype(font_path, font_size)
            text_width = draw.textbbox((0, 0), text, font=font)[2] - draw.textbbox((0, 0), text, font=font)[0]
            if text_width <= max_width:
                return font
            font_size -= 1
        return ImageFont.truetype(font_path, 10)  # Default to smallest font if none fit

    font = get_font_size(label, img_with_label.size[0])

    text_bbox = draw.textbbox((0, 0), label, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_x = (img_with_label.size[0] - text_width) // 2
    draw.text((text_x, 10), label, fill="black", font=font)

    # Save the image
    output_path = os.path.join(output_dir, f'qrcode_{index}.png')
    img_with_label.save(output_path)

# Main script
def generate_qr_codes_from_spreadsheet(file_path, sheet_name, url_column, label_column, output_dir):
    # Read the spreadsheet and specify the sheet name
    df = pd.read_excel(file_path, sheet_name=sheet_name)

    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Generate QR codes for each URL
    for index, row in df.iterrows():
        url = row[url_column]
        label = row[label_column]
        create_qr_with_label(url, label, output_dir, index)

# Usage
file_path = 'FAST Equipment_2024-05-28.xlsx'  # Path to your spreadsheet
sheet_name = 'FFF Printers'    # Name of the sheet to target
url_column = 'Log'       # Column name with URLs
label_column = 'QR Code Label'   # Column name with labels
output_dir = 'qr_codes_output'  # Directory to save QR codes

generate_qr_codes_from_spreadsheet(file_path, sheet_name, url_column, label_column, output_dir)
