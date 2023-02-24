import openai
from dotenv import load_dotenv
import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__, static_folder=".", static_url_path="")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chat.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Conversation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    conversation_id = db.Column(db.String(50), nullable=False, unique=True)
    prompt = db.Column(db.Text, nullable=False)
    response = db.Column(db.Text, nullable=False)

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
    with app.app_context():
        message = request.json.get("message")
        conversation_id = request.json.get("conversation_id")

        print(conversation_id)

        if conversation_id is None:
            conversation_id = str(len(Conversation.query.all()))
            db.session.add(Conversation(conversation_id=conversation_id, prompt="", response=""))
            db.session.commit()

        conversation = Conversation.query.filter_by(conversation_id=conversation_id).first()
        conversation.prompt += f"{message}\n"
        response = ask_openai(
            prompt=conversation.prompt,
            model="text-davinci-003",
            max_tokens=200,
            conversation_id=conversation_id
        )
        conversation.response += f"{response}\n"
        db.session.commit()
        print(conversation_id)
        answer = {
            "answer": response,
            "conversation_id": conversation_id,
            "conversation_history": {"prompt": conversation.prompt, "response": conversation.response}
        }
        print(conversation_id)
        return jsonify(answer)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
