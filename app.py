import os
import requests
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

N8N_WEBHOOK_URL = os.getenv("N8N_WEBHOOK_URL", "")

HTML = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Academia AI</title>

    <style>
        body {
            font-family: Arial, sans-serif;
            background: #111827;
            color: white;
            max-width: 800px;
            margin: 40px auto;
            padding: 20px;
        }

        h1 {
            text-align: center;
        }

        #chat {
            background: #1f2937;
            padding: 20px;
            border-radius: 12px;
            min-height: 350px;
            margin-bottom: 15px;
        }

        .usuario {
            color: #60a5fa;
            margin: 10px 0;
        }

        .bot {
            color: #34d399;
            margin: 10px 0;
        }

        form {
            display: flex;
            gap: 10px;
        }

        input {
            flex: 1;
            padding: 12px;
            border-radius: 8px;
            border: none;
        }

        button {
            padding: 12px 20px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
        }
    </style>
</head>

<body>

<h1>🏋️ Academia AI 🤖</h1>

<p style="text-align:center">
Seu personal trainer inteligente
</p>

<div id="chat">
    <div class="bot">
        <strong>Academia AI:</strong>
        Olá! Como posso ajudar no seu treino hoje?
    </div>
</div>

<form id="form">
    <input id="mensagem" placeholder="Digite sua pergunta..." required>
    <button type="submit">Enviar</button>
</form>

<script>

const form = document.getElementById("form");
const input = document.getElementById("mensagem");
const chat = document.getElementById("chat");

form.addEventListener("submit", async (e) => {

    e.preventDefault();

    const mensagem = input.value;

    chat.innerHTML += `
        <div class="usuario">
            <strong>Você:</strong> ${mensagem}
        </div>
    `;

    input.value = "";

    try {

        const resposta = await fetch("/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                mensagem: mensagem
            })
        });

        const dados = await resposta.json();

        chat.innerHTML += `
            <div class="bot">
                <strong>Academia AI:</strong> ${dados.resposta}
            </div>
        `;

    } catch {

        chat.innerHTML += `
            <div class="bot">
                Erro ao conectar com o agente.
            </div>
        `;
    }

});

</script>

</body>
</html>
"""


@app.route("/")
def home():
    return render_template_string(HTML)


@app.route("/chat", methods=["POST"])
def chat():

    mensagem = request.json.get("mensagem", "")

    if not N8N_WEBHOOK_URL:
        return jsonify({
            "resposta": "O agente ainda não foi conectado ao n8n."
        })

    try:

        resposta = requests.post(
            N8N_WEBHOOK_URL,
            json={
                "chatInput": mensagem
            },
            timeout=60
        )

        resposta.raise_for_status()

        dados = resposta.json()

        resposta_agente = (
            dados.get("resposta")
            or dados.get("text")
            or dados.get("response")
            or str(dados)
        )

        return jsonify({
            "resposta": resposta_agente
        })

    except Exception as erro:

        return jsonify({
            "resposta": f"Erro ao consultar o agente: {erro}"
        })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))