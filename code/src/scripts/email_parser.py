import os
from email import policy
from email.parser import BytesParser

def extract_email_content(email_path):
    with open(email_path, 'rb') as f:
        msg = BytesParser(policy=policy.default).parse(f)

    email_body = msg.get_body(preferencelist=('plain', 'html')).get_content()
    attachments = []

    for part in msg.iter_attachments():
        filename = part.get_filename()
        if filename:
            # Define your temp directory (modify as needed)
            temp_dir = os.path.join(os.getcwd(), "temp_files")  # Creates a folder in the current working directory

            # Ensure the directory exists
            os.makedirs(temp_dir, exist_ok=True)

            # Define the file path
            file_path = os.path.join(temp_dir,filename)
            with open(file_path, 'wb') as f:
                f.write(part.get_payload(decode=True))
            attachments.append(file_path)

    return email_body, attachments
