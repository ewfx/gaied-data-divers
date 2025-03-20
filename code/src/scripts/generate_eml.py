import yaml
import email
from email.message import EmailMessage


def yaml_to_eml(yaml_file, output_file):
    with open(yaml_file, "r") as f:
        email_data = yaml.safe_load(f)

    msg = EmailMessage()
    msg["From"] = email_data["from"]
    msg["To"] = email_data["to"]
    msg["Subject"] = email_data["subject"]
    msg.set_content(email_data["body"])

    with open(output_file, "w") as eml_file:
        eml_file.write(msg.as_string())

if __name__ == "__main__":
    yaml_to_eml("sample_email.yaml", "../sample/sample_email.eml")
    print("EML file generated successfully.")