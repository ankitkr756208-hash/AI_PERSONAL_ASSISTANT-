from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv
from groq import Groq

app = Flask(__name__)

load_dotenv()
api_key = os.getenv('GROQ_API_KEY')
client = Groq(api_key=api_key)


@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/ask', methods=['POST'])
def ask():
    question = request.form.get("question")

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "Act like a helpful personal assistant"},
            {"role": "user", "content": question}
        ],
        temperature=0.7,
        max_tokens=512
    )

    ans = response.choices[0].message.content.strip()

    return jsonify({'answer': ans}), 200


# @app.route('/summarize', methods=['POST'])
# def summarize():
#     email_text = request.form.get("email")

#     response = client.chat.completions.create(
#         model="llama-3.3-70b-versatile",
#         messages=[
#             {"role": "system", "content": "Act like an expert email assistant"},
#             {
#                 "role": "user",
#                 "content": f"Summarize the following email in 2-3 sentences:\n{email_text}"
#             }
#         ],
#         temperature=0.3,
#         max_tokens=512
#     )

#     summary = response.choices[0].message.content.strip()

#     return jsonify({'summary': summary}), 200

@app.route('/summarize', methods=['POST'])
def summarize():
    text = request.form.get("text")   # changed "email" → "text"

    if not text:
        return jsonify({'error': 'Text is required'}), 400

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "You are a professional text summarizer. Give clear, concise summaries."
                },
                {
                    "role": "user",
                    "content": f"Summarize the following text in 2-3 sentences:\n{text}"
                }
            ],
            temperature=0.3,
            max_tokens=200
        )

        summary = response.choices[0].message.content.strip()

        return jsonify({'summary': summary}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)