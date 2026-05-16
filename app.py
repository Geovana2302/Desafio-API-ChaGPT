from flask import Flask, render_template, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv
import os

# Carrega variáveis do .env
load_dotenv()

# Inicializa Flask
app = Flask(__name__)

# Pega a API Key
api_key = os.getenv("OPENROUTER_API_KEY")

# Verifica se a chave existe
if not api_key:
    raise ValueError("API KEY não encontrada!")

# Inicializa cliente OpenAI
#client = OpenAI(api_key=api_key)
client = OpenAI(
    api_key=api_key,
    base_url="https://openrouter.ai/api/v1"
)


# Página inicial
@app.route("/")
def home():
    return render_template("index.html")


# Endpoint do chat
@app.route("/chat", methods=["POST"])
def chat():

    # Recebe JSON enviado pelo front
    data = request.json

    mensagem = data.get("message")

    try:

        # Envia para OpenAI
        resposta = client.chat.completions.create(
            model="gpt-4.1-mini",
            max_tokens=300,
            messages=[
                {
                    "role": "system",
                    "content": "Você é um assistente útil."
                },
                {
                    "role": "user",
                    "content": mensagem
                }
            ]
        )

        texto = resposta.choices[0].message.content

        return jsonify({
            "reply": texto
        })

    except Exception as erro:

        return jsonify({
            "error": str(erro)
        }), 500


# Executa aplicação
if __name__ == "__main__":
    app.run(debug=True)