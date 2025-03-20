from transformers import DistilBertTokenizer, TFDistilBertForSequenceClassification
import tensorflow as tf
import numpy as np

class EmailClassifier:
    def __init__(self):
        # Load tokenizer and model correctly
        self.tokenizer = DistilBertTokenizer.from_pretrained("models/email_classifier")
        self.model = TFDistilBertForSequenceClassification.from_pretrained("models/email_classifier")

    def predict(self, email_text):
        # Tokenize input
        inputs = self.tokenizer(email_text, truncation=True, padding=True, return_tensors="tf")

        # Run model prediction
        outputs = self.model(inputs["input_ids"], attention_mask=inputs["attention_mask"])
        logits = outputs.logits.numpy()

        # Convert logits to probabilities
        probabilities = tf.nn.softmax(logits).numpy()
        category_index = np.argmax(probabilities)

        return category_index, probabilities[0][category_index]
