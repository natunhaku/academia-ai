import os
import requests
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

N8N_WEBHOOK_URL = os.getenv("N8N_WEBHOOK_URL", "")

HTML = r"""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Academia AI</title>

  <style>
    * { box-sizing: border-box; }

    :root {
      --bg: #070b12;
      --graphene: #0d131d;
      --graphene-2: #121a26;
      --graphene-3: #182230;
      --line: rgba(148, 163, 184, 0.16);
      --line-strong: rgba(96, 165, 250, 0.28);
      --text: #f8fafc;
      --text-soft: #cbd5e1;
      --muted: #7f8ea3;
      --blue: #2563eb;
      --blue-2: #3b82f6;
      --blue-3: #60a5fa;
      --green: #22c55e;
      --danger: #ef4444;
      --shadow: 0 24px 60px rgba(0,0,0,.34);
    }

    html, body {
      margin: 0;
      height: 100%;
      background:
        radial-gradient(circle at 70% 0%, rgba(37,99,235,.10), transparent 28%),
        linear-gradient(180deg, #070b12 0%, #0a0f17 100%);
      color: var(--text);
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }

    body { overflow: hidden; }

    button, textarea { font: inherit; }

    .layout {
      height: 100vh;
      display: grid;
      grid-template-columns: 260px minmax(0, 1fr);
    }

    /* SIDEBAR */
    .sidebar {
      position: relative;
      display: flex;
      flex-direction: column;
      background:
        linear-gradient(180deg, rgba(15,23,42,.98), rgba(8,13,22,.98));
      border-right: 1px solid var(--line);
      padding: 18px 14px;
    }

    .brand {
      display: flex;
      align-items: center;
      gap: 12px;
      padding: 6px 8px 18px;
    }

    .brand-logo {
      width: 40px;
      height: 40px;
      border-radius: 12px;
      display: grid;
      place-items: center;
      background: linear-gradient(145deg, var(--blue-2), #1d4ed8);
      box-shadow: 0 10px 30px rgba(37,99,235,.28);
      font-weight: 800;
      letter-spacing: -.5px;
    }

    .brand-copy strong {
      display: block;
      font-size: 15px;
    }

    .brand-copy span {
      display: block;
      margin-top: 2px;
      color: var(--muted);
      font-size: 11px;
    }

    .new-chat {
      width: 100%;
      height: 44px;
      display: flex;
      align-items: center;
      gap: 10px;
      padding: 0 14px;
      background: rgba(255,255,255,.025);
      border: 1px solid var(--line);
      border-radius: 12px;
      color: var(--text-soft);
      cursor: pointer;
      transition: .18s ease;
    }

    .new-chat:hover {
      border-color: var(--line-strong);
      background: rgba(37,99,235,.08);
      color: white;
    }

    .section-label {
      margin: 22px 10px 8px;
      font-size: 10px;
      text-transform: uppercase;
      letter-spacing: .12em;
      color: #64748b;
    }

    .history {
      display: flex;
      flex-direction: column;
      gap: 6px;
      overflow: auto;
    }

    .history-item {
      padding: 10px 12px;
      border-radius: 10px;
      color: #aeb8c7;
      font-size: 12px;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      cursor: default;
      background: transparent;
    }

    .history-item.active {
      background: rgba(37,99,235,.10);
      color: #dbeafe;
      border: 1px solid rgba(96,165,250,.12);
    }

    .sidebar-bottom {
      margin-top: auto;
      border-top: 1px solid var(--line);
      padding-top: 14px;
    }

    .status-card {
      display: flex;
      align-items: center;
      gap: 10px;
      padding: 10px;
      border-radius: 12px;
      color: var(--muted);
      font-size: 11px;
    }

    .status-dot {
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background: var(--green);
      box-shadow: 0 0 12px rgba(34,197,94,.7);
    }

    /* MAIN */
.main {
    min-width: 0;
    min-height: 0;
    display: flex;
    flex-direction: column;
    position: relative;
}

    .topbar {
      height: 64px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 28px;
      border-bottom: 1px solid rgba(148,163,184,.08);
      background: rgba(7,11,18,.72);
      backdrop-filter: blur(16px);
    }

    .top-title h1 {
      margin: 0;
      font-size: 15px;
      font-weight: 650;
    }

    .top-title p {
      margin: 3px 0 0;
      color: var(--muted);
      font-size: 11px;
    }

    .pill {
      display: flex;
      align-items: center;
      gap: 8px;
      padding: 7px 10px;
      border: 1px solid var(--line);
      border-radius: 999px;
      color: #9fb0c4;
      font-size: 11px;
      background: rgba(255,255,255,.025);
    }

    .chat-wrap {
      flex: 1;
      min-height: 0;
      overflow: hidden;
      position: relative;
    }

    #chat {
      height: 100%;
      overflow-y: auto;
      padding: 32px max(24px, calc((100vw - 260px - 880px)/2)) 170px;
      scroll-behavior: smooth;
    }

    #chat::-webkit-scrollbar { width: 8px; }
    #chat::-webkit-scrollbar-track { background: transparent; }
    #chat::-webkit-scrollbar-thumb {
      background: #202a38;
      border-radius: 999px;
    }

    /* WELCOME */
    .welcome {
      min-height: 70vh;
      display: flex;
      align-items: center;
      justify-content: center;
    }

    .welcome-card {
      width: min(760px, 100%);
      text-align: center;
      padding: 24px;
    }

    .welcome-mark {
      width: 64px;
      height: 64px;
      margin: 0 auto 20px;
      border-radius: 20px;
      display: grid;
      place-items: center;
      background:
        linear-gradient(145deg, rgba(37,99,235,.22), rgba(59,130,246,.08));
      border: 1px solid rgba(96,165,250,.22);
      box-shadow: var(--shadow);
      color: #bfdbfe;
      font-size: 20px;
      font-weight: 800;
    }

    .welcome h2 {
      margin: 0;
      font-size: clamp(26px, 4vw, 38px);
      letter-spacing: -1.4px;
      font-weight: 700;
    }

    .welcome p {
      max-width: 620px;
      margin: 12px auto 0;
      color: var(--muted);
      line-height: 1.7;
      font-size: 14px;
    }

    .quick-actions {
      display: grid;
      grid-template-columns: repeat(2, minmax(0,1fr));
      gap: 10px;
      max-width: 680px;
      margin: 28px auto 0;
    }

    .quick-btn {
      text-align: left;
      padding: 14px 15px;
      min-height: 66px;
      border-radius: 14px;
      border: 1px solid var(--line);
      background:
        linear-gradient(180deg, rgba(255,255,255,.035), rgba(255,255,255,.018));
      color: var(--text-soft);
      cursor: pointer;
      transition: .18s ease;
    }

    .quick-btn:hover {
      transform: translateY(-1px);
      border-color: rgba(96,165,250,.30);
      background: rgba(37,99,235,.07);
    }

    .quick-btn strong {
      display: block;
      color: #e5edf8;
      font-size: 12px;
      margin-bottom: 4px;
    }

    .quick-btn span {
      color: var(--muted);
      font-size: 11px;
    }

    /* MESSAGES */
    .row {
      display: flex;
      margin: 22px 0;
      animation: fadeIn .18s ease;
    }

    .row.user { justify-content: flex-end; }
    .row.bot { justify-content: flex-start; }

    @keyframes fadeIn {
      from { opacity: 0; transform: translateY(5px); }
      to { opacity: 1; transform: translateY(0); }
    }

    .user-bubble {
      max-width: min(76%, 640px);
      padding: 12px 16px;
      border-radius: 18px 18px 6px 18px;
      background:
        linear-gradient(180deg, #1a2635, #16202d);
      border: 1px solid rgba(148,163,184,.14);
      color: #eef4fb;
      line-height: 1.6;
      font-size: 14px;
      box-shadow: 0 10px 28px rgba(0,0,0,.18);
    }

    .bot-message {
      width: 100%;
      max-width: 820px;
    }

    .bot-head {
      display: flex;
      align-items: center;
      gap: 10px;
      margin-bottom: 10px;
    }

    .bot-avatar {
      width: 30px;
      height: 30px;
      border-radius: 10px;
      display: grid;
      place-items: center;
      background: linear-gradient(145deg, var(--blue-2), #1d4ed8);
      color: white;
      font-size: 10px;
      font-weight: 800;
    }

    .bot-name {
      font-size: 12px;
      font-weight: 650;
      color: #dbeafe;
    }

    .bot-sub {
      margin-left: auto;
      color: #536276;
      font-size: 10px;
    }

    .bot-content {
      padding-left: 40px;
      color: #d9e2ee;
      font-size: 14px;
      line-height: 1.75;
    }

    .bot-content h1,
    .bot-content h2,
    .bot-content h3 {
      color: white;
      margin: 20px 0 10px;
      line-height: 1.3;
      letter-spacing: -.3px;
    }

    .bot-content h1 { font-size: 22px; }
    .bot-content h2 { font-size: 19px; }
    .bot-content h3 { font-size: 16px; }

    .bot-content p { margin: 8px 0; }

    .bot-content strong {
      color: #f8fbff;
      font-weight: 700;
    }

    .bot-content em { color: #c4cfdd; }

    .bot-content ul,
    .bot-content ol {
      margin: 10px 0 10px 22px;
      padding: 0;
    }

    .bot-content li { margin: 7px 0; }

    .bot-content hr {
      border: 0;
      border-top: 1px solid var(--line);
      margin: 18px 0;
    }

    /* TYPING */
    .typing {
      display: inline-flex;
      align-items: center;
      gap: 5px;
      padding-left: 40px;
      margin-top: 2px;
    }

    .typing span {
      width: 6px;
      height: 6px;
      border-radius: 50%;
      background: #708096;
      animation: typing 1s infinite;
    }

    .typing span:nth-child(2) { animation-delay: .14s; }
    .typing span:nth-child(3) { animation-delay: .28s; }

    @keyframes typing {
      0%,60%,100% { opacity: .25; transform: translateY(0); }
      30% { opacity: 1; transform: translateY(-3px); }
    }

    /* COMPOSER */
    .composer-shell {
      position: fixed;
      left: 260px;
      right: 0;
      bottom: 0;
      padding: 30px 24px 18px;
      background:
        linear-gradient(180deg,
          rgba(7,11,18,0) 0%,
          rgba(7,11,18,.82) 28%,
          rgba(7,11,18,.98) 65%);
    }

    .composer {
      width: min(860px, 100%);
      margin: 0 auto;
    }

    .composer-box {
      display: flex;
      align-items: flex-end;
      gap: 10px;
      padding: 10px 10px 10px 16px;
      border: 1px solid rgba(148,163,184,.16);
      border-radius: 18px;
      background:
        linear-gradient(180deg, rgba(24,34,48,.96), rgba(17,25,36,.96));
      box-shadow: 0 18px 50px rgba(0,0,0,.28);
      transition: .18s ease;
    }

    .composer-box:focus-within {
      border-color: rgba(96,165,250,.38);
      box-shadow:
        0 0 0 3px rgba(37,99,235,.08),
        0 18px 50px rgba(0,0,0,.28);
    }

    textarea {
      flex: 1;
      min-height: 42px;
      max-height: 150px;
      resize: none;
      border: 0;
      outline: 0;
      color: white;
      background: transparent;
      padding: 10px 0 8px;
      line-height: 1.5;
      font-size: 14px;
    }

    textarea::placeholder { color: #64748b; }

    .send {
      width: 44px;
      height: 44px;
      border: 0;
      border-radius: 14px;
      color: white;
      background: linear-gradient(145deg, var(--blue-2), #1d4ed8);
      cursor: pointer;
      font-size: 18px;
      box-shadow: 0 10px 24px rgba(37,99,235,.26);
      transition: .18s ease;
    }

    .send:hover { transform: translateY(-1px); }
    .send:disabled { opacity: .45; cursor: not-allowed; transform: none; }

    .disclaimer {
      text-align: center;
      margin-top: 9px;
      color: #536276;
      font-size: 10px;
    }

    /* MOBILE */
    .mobile-menu {
      display: none;
      width: 38px;
      height: 38px;
      border: 1px solid var(--line);
      border-radius: 10px;
      background: rgba(255,255,255,.025);
      color: white;
      cursor: pointer;
    }

    @media (max-width: 820px) {
      .layout { grid-template-columns: 1fr; }

      .sidebar {
        position: fixed;
        inset: 0 auto 0 0;
        width: 260px;
        z-index: 30;
        transform: translateX(-100%);
        transition: .2s ease;
        box-shadow: 30px 0 60px rgba(0,0,0,.45);
      }

      .sidebar.open { transform: translateX(0); }

      .mobile-menu { display: inline-grid; place-items: center; }

      .composer-shell { left: 0; }

      .topbar { padding: 0 16px; }

      #chat { padding: 24px 16px 160px; }

      .quick-actions { grid-template-columns: 1fr; }

      .bot-content { padding-left: 0; }

      .user-bubble { max-width: 88%; }
    }
  </style>
</head>

<body>
<div class="layout">

  <aside class="sidebar" id="sidebar">
    <div class="brand">
      <div class="brand-logo">AI</div>
      <div class="brand-copy">
        <strong>Academia AI</strong>
        <span>Treino inteligente</span>
      </div>
    </div>

    <button class="new-chat" onclick="novoChat()">
      <span>＋</span>
      <span>Novo chat</span>
    </button>

    <div class="section-label">Conversas</div>

    <div class="history" id="history">
      <div class="history-item active">Nova conversa</div>
    </div>

    <div class="sidebar-bottom">
      <div class="status-card">
        <span class="status-dot"></span>
        <span>Agente conectado</span>
      </div>
    </div>
  </aside>

  <section class="main">
    <header class="topbar">
      <div style="display:flex;align-items:center;gap:12px;">
        <button class="mobile-menu" onclick="toggleSidebar()">☰</button>

        <div class="top-title">
          <h1>Academia AI</h1>
          <p>Seu personal trainer inteligente</p>
        </div>
      </div>

      <div class="pill">
        <span class="status-dot"></span>
        IA online
      </div>
    </header>

    <div class="chat-wrap">
      <div id="chat">
        <div class="welcome" id="welcome">
          <div class="welcome-card">
            <div class="welcome-mark">AI</div>

            <h2>Como posso ajudar no seu treino?</h2>

            <p>
              Converse com seu treinador virtual para montar rotinas,
              ajustar exercícios e organizar seus treinos de forma simples.
            </p>

            <div class="quick-actions">
              <button class="quick-btn" onclick="usarSugestao('Monte um treino completo de peito para iniciante')">
                <strong>Treino de peito</strong>
                <span>Exercícios, séries, repetições e descanso</span>
              </button>

              <button class="quick-btn" onclick="usarSugestao('Monte um treino para hipertrofia')">
                <strong>Hipertrofia</strong>
                <span>Rotina focada em ganho de massa muscular</span>
              </button>

              <button class="quick-btn" onclick="usarSugestao('Monte um treino completo de pernas')">
                <strong>Treino de pernas</strong>
                <span>Quadríceps, posteriores, glúteos e panturrilhas</span>
              </button>

              <button class="quick-btn" onclick="usarSugestao('Monte um treino para fazer em casa sem equipamentos')">
                <strong>Treino em casa</strong>
                <span>Opções sem aparelhos de academia</span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="composer-shell">
      <div class="composer">
        <form id="form">
          <div class="composer-box">
            <textarea
              id="mensagem"
              rows="1"
              placeholder="Pergunte qualquer coisa sobre treino..."
              autocomplete="off"
            ></textarea>

            <button class="send" id="enviar" type="submit">↑</button>
          </div>
        </form>

        <div class="disclaimer">
          Academia AI pode cometer erros. Consulte um profissional quando necessário.
        </div>
      </div>
    </div>
  </section>
</div>

<script>
const form = document.getElementById("form");
const input = document.getElementById("mensagem");
const chat = document.getElementById("chat");
const sendButton = document.getElementById("enviar");
const sidebar = document.getElementById("sidebar");
const history = document.getElementById("history");

function escapeHtml(text) {
  return String(text)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

function formatMarkdown(text) {
  if (!text) return "";

  text = escapeHtml(text)
    .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
    .replace(/\*(.*?)\*/g, "<em>$1</em>");

  const lines = text.split(/\r?\n/);

  let html = "";
  let ul = false;
  let ol = false;

  function closeLists() {
    if (ul) {
      html += "</ul>";
      ul = false;
    }
    if (ol) {
      html += "</ol>";
      ol = false;
    }
  }

  lines.forEach((line) => {
    const clean = line.trim();

    if (!clean) {
      closeLists();
      html += "<br>";
      return;
    }

    if (clean.startsWith("### ")) {
      closeLists();
      html += "<h3>" + clean.slice(4) + "</h3>";
      return;
    }

    if (clean.startsWith("## ")) {
      closeLists();
      html += "<h2>" + clean.slice(3) + "</h2>";
      return;
    }

    if (clean.startsWith("# ")) {
      closeLists();
      html += "<h1>" + clean.slice(2) + "</h1>";
      return;
    }

    if (/^---+$/.test(clean)) {
      closeLists();
      html += "<hr>";
      return;
    }

    const numbered = clean.match(/^(\d+)\.\s+(.*)/);

    if (numbered) {
      if (ul) {
        html += "</ul>";
        ul = false;
      }

      if (!ol) {
        html += "<ol>";
        ol = true;
      }

      html += "<li>" + numbered[2] + "</li>";
      return;
    }

    if (clean.startsWith("- ") || clean.startsWith("• ")) {
      if (ol) {
        html += "</ol>";
        ol = false;
      }

      if (!ul) {
        html += "<ul>";
        ul = true;
      }

      html += "<li>" + clean.slice(2) + "</li>";
      return;
    }

    closeLists();
    html += "<p>" + clean + "</p>";
  });

  closeLists();

  return html;
}

function removeWelcome() {
  const welcome = document.getElementById("welcome");
  if (welcome) welcome.remove();
}

function addUser(text) {
  removeWelcome();

  const row = document.createElement("div");
  row.className = "row user";

  const bubble = document.createElement("div");
  bubble.className = "user-bubble";
  bubble.textContent = text;

  row.appendChild(bubble);
  chat.appendChild(row);

  chat.scrollTop = chat.scrollHeight;
}

function addBot(text) {
  removeWelcome();

  const row = document.createElement("div");
  row.className = "row bot";

  row.innerHTML = `
    <div class="bot-message">
      <div class="bot-head">
        <div class="bot-avatar">AI</div>
        <div class="bot-name">Academia AI</div>
        <div class="bot-sub">Resposta do agente</div>
      </div>

      <div class="bot-content">
        ${formatMarkdown(text)}
      </div>
    </div>
  `;

  chat.appendChild(row);
  chat.scrollTop = chat.scrollHeight;
}

function showTyping() {
  const row = document.createElement("div");
  row.className = "row bot";
  row.id = "typing";

  row.innerHTML = `
    <div class="bot-message">
      <div class="bot-head">
        <div class="bot-avatar">AI</div>
        <div class="bot-name">Academia AI</div>
        <div class="bot-sub">Pensando...</div>
      </div>

      <div class="typing">
        <span></span>
        <span></span>
        <span></span>
      </div>
    </div>
  `;

  chat.appendChild(row);
  chat.scrollTop = chat.scrollHeight;
}

function removeTyping() {
  const el = document.getElementById("typing");
  if (el) el.remove();
}

function addHistory(text) {
  const active = history.querySelector(".history-item.active");
  if (active && active.textContent === "Nova conversa") {
    active.textContent = text.length > 32 ? text.slice(0,32) + "..." : text;
  }
}

async function sendMessage(text) {
  text = text.trim();
  if (!text) return;

  addHistory(text);
  addUser(text);

  input.value = "";
  input.style.height = "auto";
  input.disabled = true;
  sendButton.disabled = true;

  showTyping();

  try {
    const response = await fetch("/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        mensagem: text
      })
    });

    const data = await response.json();

    removeTyping();

    if (!response.ok) {
      addBot(data.resposta || "Não foi possível processar sua solicitação.");
      return;
    }

    addBot(data.resposta || "Não recebi uma resposta do agente.");
  } catch (error) {
    removeTyping();
    addBot("Não foi possível conectar ao agente. Tente novamente.");
  } finally {
    input.disabled = false;
    sendButton.disabled = false;
    input.focus();
  }
}

function usarSugestao(text) {
  input.value = text;
  sendMessage(text);
}

function novoChat() {
  chat.innerHTML = `
    <div class="welcome" id="welcome">
      <div class="welcome-card">
        <div class="welcome-mark">AI</div>
        <h2>Como posso ajudar no seu treino?</h2>
        <p>
          Converse com seu treinador virtual para montar rotinas,
          ajustar exercícios e organizar seus treinos de forma simples.
        </p>
      </div>
    </div>
  `;

  history.innerHTML = '<div class="history-item active">Nova conversa</div>';
  input.value = "";
  input.focus();
}

function toggleSidebar() {
  sidebar.classList.toggle("open");
}

form.addEventListener("submit", (event) => {
  event.preventDefault();
  sendMessage(input.value);
});

input.addEventListener("keydown", (event) => {
  if (event.key === "Enter" && !event.shiftKey) {
    event.preventDefault();
    form.requestSubmit();
  }
});

input.addEventListener("input", function () {
  this.style.height = "auto";
  this.style.height = Math.min(this.scrollHeight, 150) + "px";
});
</script>
</body>
</html>
"""


@app.route("/")
def home():
    return render_template_string(HTML)


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


@app.route("/chat", methods=["POST"])
def chat():
    payload = request.get_json(silent=True) or {}
    mensagem = payload.get("mensagem", "").strip()

    if not mensagem:
        return jsonify({
            "resposta": "Digite uma mensagem para conversar com o Academia AI."
        }), 400

    if not N8N_WEBHOOK_URL:
        return jsonify({
            "resposta": "O webhook do n8n ainda não foi configurado."
        }), 500

    try:
        resposta = requests.post(
            N8N_WEBHOOK_URL,
            json={"chatInput": mensagem},
            timeout=90
        )

        resposta.raise_for_status()

        if not resposta.text.strip():
            return jsonify({
                "resposta": "O n8n respondeu sem conteúdo."
            }), 502

        try:
            dados = resposta.json()
        except ValueError:
            return jsonify({
                "resposta": resposta.text
            })

        resposta_agente = (
            dados.get("resposta")
            or dados.get("output")
            or dados.get("text")
            or dados.get("response")
            or str(dados)
        )

        return jsonify({
            "resposta": resposta_agente
        })

    except requests.Timeout:
        return jsonify({
            "resposta": "O agente demorou mais que o esperado para responder."
        }), 504

    except requests.RequestException as erro:
        return jsonify({
            "resposta": f"Erro ao consultar o agente: {erro}"
        }), 502

    except Exception as erro:
        return jsonify({
            "resposta": f"Erro inesperado: {erro}"
        }), 500


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.getenv("PORT", 5000))
    )
