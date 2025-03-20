import re
import spacy
import os
import dateparser
import dateutil.parser

model_path = os.path.expanduser("C:/Windows/System32/venv/Lib/site-packages/en_core_web_sm/en_core_web_sm-3.8.0")
nlp = spacy.load(model_path)

def extract_key_information(text):
    """
    Extracts deal_name, amount, and expiration_date from text.
    Prioritizes "fund your share" amount, then "repay", then highest amount.
    """
    print("\n🔹 Extracted Text:\n", text)  # Debugging: Print extracted text

    doc = nlp(text)

    deal_name = None
    amount = None
    expiration_date = None

    # 🔹 Step 1: Extract Deal Name Using Regex First
    # Extract Deal Name (Fix: Stop at newline or period)
    deal_name_match = re.search(r"DEAL NAME:\s*([A-Za-z0-9\s\-,.$]+)", text, re.IGNORECASE)
    if deal_name_match:
        deal_name = deal_name_match.group(1).split("\n")[0].strip()  # ✅ Stop at first newline
    else:
        # 🔹 Step 2: Fallback to spaCy (If regex fails)
        org_entities = [ent.text for ent in doc.ents if ent.label_ == "ORG"]
        if org_entities:
            deal_name = org_entities[0]  # First detected organization

    # 🔹 Extract expiration date using regex
    date_match = re.search(r"(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})", text)
    if date_match:
        expiration_date = date_match.group()
    else:
        # Fallback: Use dateutil.parser
        words = text.split()
        for word in words:
            try:
                parsed_date = dateutil.parser.parse(word, fuzzy=True)
                expiration_date = parsed_date.strftime("%Y-%m-%d")
                break
            except (ValueError, TypeError):
                continue

    # Extract all monetary values (handling spaces, new lines, and "MM" notation)
    amount_matches = re.finditer(
        r"(?:USD\s*[$]?[\s\n]*|USD\s*)?([\d,]+(?:\.\d{2})?|[\d]+MM)", text, re.IGNORECASE
    )
    extracted_amounts = []

    for match in amount_matches:
        amount_str = match.group(1).strip()

        # ✅ Skip years but allow large numbers
        if amount_str.isdigit() and 1000 <= int(amount_str) <= 2025:
            print(f"⚠️ Skipping invalid amount (possible year): {amount_str}")
            continue  # Skip "2023" but not "20,000,000.00"

        try:
            if "MM" in amount_str:  # Convert million notation
                numeric_value = float(amount_str.replace("MM", "").replace(",", "")) * 1_000_000
            else:
                numeric_value = float(amount_str.replace(",", ""))

            # ✅ Only accept numbers larger than 10,000 to avoid small values
            if numeric_value > 10000:
                extracted_amounts.append((numeric_value, match.start()))
            else:
                print(f"⚠️ Skipping small amount: {numeric_value}")

        except ValueError:
            print(f"⚠️ Skipping invalid amount: {amount_str}")

    # 🔹 Determine the most relevant amount
    if extracted_amounts:
        # 1️⃣ Look for "fund your share" keyword first
        fund_match = re.search(r"fund your share", text, re.IGNORECASE)
        if fund_match:
            fund_pos = fund_match.start()
            amount = min(extracted_amounts, key=lambda x: abs(x[1] - fund_pos))[0]

        # 2️⃣ If no "fund", check for "repay" keyword
        elif re.search(r"repay", text, re.IGNORECASE):
            repay_match = re.search(r"repay", text, re.IGNORECASE)
            repay_pos = repay_match.start()
            amount = min(extracted_amounts, key=lambda x: abs(x[1] - repay_pos))[0]

        # 3️⃣ If neither, fallback to the highest amount
        else:
            amount = max(extracted_amounts, key=lambda x: x[0])[0]

    return {
        "deal_name": deal_name or "N/A",
        "amount": str(int(amount)) if amount else None,
        "expiration_date": expiration_date,
    }

def preprocess_text(text):
    return text.replace("\n", " ").strip()  # Normalize text for better processing
