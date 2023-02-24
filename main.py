import openai
from dotenv import load_dotenv
import os

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

def ask_openai(prompt, model, temperature=0.5, max_tokens=2048, top_p=1, frequency_penalty=0, presence_penalty=0):
    completions = openai.Completion.create(
        engine=model,
        prompt=prompt,
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=top_p,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty,
    )
    message = completions.choices[0].text
    return message.strip()

def main():
    prompt = "para que serve o chatgpt?"
    response = ask_openai(prompt, "text-davinci-003")
    print(response)

if __name__ == "__main__":
    main()
