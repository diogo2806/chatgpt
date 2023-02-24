import openai
from dotenv import load_dotenv
import os
from flask import Flask, request, jsonify

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__, static_folder=".", static_url_path="")
conversations = {}

def ask_openai(prompt, model, temperature=0.5, max_tokens=2048, top_p=1, frequency_penalty=0, presence_penalty=0, conversation_id=None):
    completions = openai.Completion.create(
        engine=model,
        prompt=prompt,
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=top_p,
        n=1,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty,
        stop=None,
        user=conversation_id
    )
    message = completions.choices[0].text
    return message.strip()


@app.route("/")
def index():
    return app.send_static_file("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    message = request.json.get("message")
    conversation_id = request.json.get("conversation_id")
    
    if conversation_id is None:
        conversation_id = str(len(conversations))
        conversations[conversation_id] = {"prompt": "", "response": ""}

    conversations[conversation_id]["prompt"] += f"{message}\n"
    response = ask_openai(
        prompt=conversations[conversation_id]["prompt"], 
        model="text-davinci-003", 
        max_tokens=200, 
        conversation_id=conversation_id
    )
    conversations[conversation_id]["response"] += f"{response}\n"
    
    return jsonify({"answer": response, "conversation_id": conversation_id})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
