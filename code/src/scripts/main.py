from email_parser import extract_email_content
from ocr_processor import extract_pdf_from_eml, extract_text_from_image
from email_classifier import EmailClassifier
from ner_extractor import extract_key_information
# from multi_intent_detector import detect_multi_intent
from duplicate_detector import is_duplicate

def process_email(email_path):
    email_body, attachments = extract_email_content(email_path)

    extracted_text = email_body
    for attachment in attachments:
        if attachment.endswith(".pdf"):
            extracted_pdf_text = extract_pdf_from_eml(attachment, "output.pdf")
            if extracted_pdf_text:  # Ensure it's not None before concatenating
                extracted_text += extracted_pdf_text
        elif attachment.endswith((".jpg", ".png")):
            extracted_text += extract_text_from_image(attachment)

    # Classify email text
    classifier = EmailClassifier()
    category, confidence = classifier.predict(extracted_text)
    classification = {"category": category, "confidence": confidence}

    key_info = extract_key_information(extracted_text)

    email_data = {"classification": classification, "key_info": key_info}

    duplicate = is_duplicate(email_data)
    if duplicate:
        print("Duplicate request detected! Ignoring email.")
    else:
        print(email_data)

if __name__ == "__main__":
    process_email("../sample/sample_email.eml")
