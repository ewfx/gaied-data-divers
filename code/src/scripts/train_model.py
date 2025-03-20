from transformers import pipeline

# Initialize the classifier
classifier = pipeline("text-classification", model="distilbert-base-uncased-finetuned-sst-2-english")

# Save the model correctly
classifier.model.save_pretrained("models/email_classifier")
classifier.tokenizer.save_pretrained("models/email_classifier")

print("Model saved in models/email_classifier/")
