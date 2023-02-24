import openai
import os

OPENAI_API_KEY = "sua-chave-de-api-aqui"

# Autenticação com a API do OpenAI
openai.api_key = OPENAI_API_KEY

# Função para enviar a consulta para o ChatGPT
def ask_chatgpt(prompt):
    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )

    message = response.choices[0].text.strip()
    return message

# Loop para enviar perguntas ao ChatGPT
while True:
    prompt = input("Você: ")
    response = ask_chatgpt(prompt)
    print("ChatGPT:", response)
