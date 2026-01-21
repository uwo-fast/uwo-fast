# pip install reportlab

from PIL import Image
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import os

def create_pdf_from_qr_codes(input_dir, output_pdf):
    # A4 page size
    page_width, page_height = A4

    # Create a PDF canvas
    c = canvas.Canvas(output_pdf, pagesize=A4)
    
    # Load QR code images
    qr_files = [f for f in os.listdir(input_dir) if f.endswith('.png')]
    qr_files.sort()  # Optional: Sort files if necessary
    
    # Image size and spacing
    max_width = page_width / 2 - 40  # Maximum width for each image (with margin)
    max_height = max_width  # Assuming the QR code images are roughly square
    margin = 10  # Margin around images
    x_spacing = 10  # Spacing between images in a row
    y_spacing = 10  # Spacing between rows

    # Initial positions
    x = margin
    y = page_height - margin

    for i, qr_file in enumerate(qr_files):
        qr_path = os.path.join(input_dir, qr_file)
        img = Image.open(qr_path)
        
        # Calculate the image size while maintaining aspect ratio
        img_width, img_height = img.size
        ratio = min(max_width / img_width, max_height / img_height)
        img_width = int(img_width * ratio)
        img_height = int(img_height * ratio)

        # Draw the image
        y -= img_height
        c.drawImage(qr_path, x, y, img_width, img_height)
        y += img_height

        # Move to the next position
        if (i + 1) % 2 == 0:  # Move to the next row after every two images
            x = margin
            y -= img_height + y_spacing
            if y < margin + img_height:
                c.showPage()  # Add a new page if the current page is full
                y = page_height - margin
        else:
            x += img_width + x_spacing

    # Save the PDF
    c.save()

# Usage
input_dir = 'qr_codes_output'  # Directory containing QR code images
output_pdf = 'qr_codes_to_print.pdf'  # Output PDF file

create_pdf_from_qr_codes(input_dir, output_pdf)
