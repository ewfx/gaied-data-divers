import openai

openai.api_key = "YOUR_OPENAI_API_KEY"

def detect_multi_intent(content):
    prompt = f"Does this email contain multiple requests? Answer Yes or No:\n\n{content}"

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "You are an expert in email analysis."},
                  {"role": "user", "content": prompt}]
    )

    return "Yes" in response["choices"][0]["message"]["content"]
