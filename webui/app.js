const apiBase = location.protocol === "file:" ? "http://localhost:8000" : "";
const statusEl = document.getElementById("status");
const initBtn = document.getElementById("initBtn");
const sendBtn = document.getElementById("sendBtn");
const inputEl = document.getElementById("input");
const messagesEl = document.getElementById("messages");
const vectorStoreEl = document.getElementById("vectorStore");
const chatModelEl = document.getElementById("chatModel");
const topKEl = document.getElementById("topK");

function addMessage(role, text, sources) {
  const div = document.createElement("div");
  div.className = `msg ${role}`;
  div.textContent = text;
  if (sources && sources.length) {
    const s = document.createElement("div");
    s.className = "sources";
    const title = document.createElement("div");
    title.textContent = "Sources:";
    title.style.fontWeight = "bold";
    s.appendChild(title);
    sources.forEach((src, i) => {
      const item = document.createElement("div");
      item.className = "source-item";
      const meta = Object.entries(src.metadata || {})
        .map(([k,v]) => `${k}: ${v}`)
        .join(" | ");
      item.innerHTML = `<strong>${i+1}</strong> ${escapeHtml(src.content)}<div class='meta'>${meta}</div>`;
      s.appendChild(item);
    });
    div.appendChild(s);
  }
  messagesEl.appendChild(div);
  messagesEl.scrollTop = messagesEl.scrollHeight;
}

function escapeHtml(str) {
  return str.replace(/[&<>]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]));
}

async function init() {
  statusEl.textContent = "Initializing...";
  try {
    const body = {
      vector_store: vectorStoreEl.value,
      top_k: parseInt(topKEl.value, 10),
      chat_model: chatModelEl.value
    };
    const res = await fetch(`${apiBase}/init`, {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify(body)
    });
    if (!res.ok) throw new Error(await res.text());
    const data = await res.json();
    statusEl.textContent = `Initialized (${data.config.vector_store}, k=${data.config.top_k})`;
    addMessage("assistant", "✅ Initialized RAG chain.");
  } catch (e) {
    statusEl.textContent = "Init failed";
    addMessage("assistant", `❌ Init error: ${e.message}`);
  }
}

async function send() {
  const q = inputEl.value.trim();
  if (!q) return;
  addMessage("user", q);
  inputEl.value = "";
  try {
    const res = await fetch(`${apiBase}/chat`, {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({query: q})
    });
    if (!res.ok) throw new Error(await res.text());
    const data = await res.json();
    addMessage("assistant", data.answer, data.sources);
  } catch (e) {
    addMessage("assistant", `❌ Chat error: ${e.message}`);
  }
}

initBtn.addEventListener("click", init);
sendBtn.addEventListener("click", send);
inputEl.addEventListener("keydown", e => { if (e.key === "Enter" && !e.shiftKey){ e.preventDefault(); send(); }});

document.querySelectorAll('.sample').forEach(btn => {
  btn.addEventListener('click', () => { inputEl.value = btn.dataset.q; inputEl.focus(); });
});

// On load, show hint
addMessage("assistant", "👋 Welcome. Click Initialize to start.");
