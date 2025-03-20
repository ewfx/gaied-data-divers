import email

import pdfplumber
import pytesseract
# Set the Tesseract-OCR path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
from PIL import Image


def extract_pdf_from_eml(eml_path, output_pdf_path):
    with open(eml_path, "r", encoding="utf-8") as file:
        msg = email.message_from_file(file)

    for part in msg.walk():
        if part.get_content_type() == "application/pdf":
            pdf_data = part.get_payload(decode=True)  # Decode base64
            with open(output_pdf_path, "wb") as pdf_file:
                pdf_file.write(pdf_data)
            print(f"✅ PDF extracted to {output_pdf_path}")
            return output_pdf_path

    print("⚠️ No PDF found in the EML file.")
    return None
# import fitz  # PyMuPDF

# def extract_text_from_pdf(pdf_path):
#     """
#     Extracts text from a PDF file.
#
#     :param pdf_path: Path to the PDF file.
#     :return: Extracted text as a string.
#     """
#     text = ""
#     with fitz.open(pdf_path) as doc:
#         for page in doc:
#             text += page.get_text("text") + "\n"
#     return text


def extract_text_from_image(image_path):
    image = Image.open(image_path)
    return pytesseract.image_to_string(image)
