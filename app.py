from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from reviewer import review_code

app = FastAPI(title="Code Review Bot")


class CodeRequest(BaseModel):
    code: str


@app.get("/", response_class=HTMLResponse)
def index():
    return """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Code Review Bot</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: system-ui, sans-serif;
      background: #0f0f0f;
      color: #e2e2e2;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      align-items: center;
      padding: 48px 16px;
    }
    h1 { font-size: 2rem; margin-bottom: 4px; }
    .caption { color: #888; margin-bottom: 32px; font-size: 0.9rem; }
    textarea {
      width: 100%;
      max-width: 800px;
      height: 280px;
      background: #1a1a1a;
      border: 1px solid #333;
      border-radius: 8px;
      color: #e2e2e2;
      font-family: monospace;
      font-size: 0.9rem;
      padding: 16px;
      resize: vertical;
      outline: none;
    }
    textarea:focus { border-color: #555; }
    button {
      margin-top: 16px;
      padding: 12px 32px;
      background: #2563eb;
      color: white;
      border: none;
      border-radius: 8px;
      font-size: 1rem;
      cursor: pointer;
      width: 100%;
      max-width: 800px;
    }
    button:hover { background: #1d4ed8; }
    button:disabled { background: #333; color: #666; cursor: not-allowed; }
    #result {
      margin-top: 32px;
      width: 100%;
      max-width: 800px;
      background: #1a1a1a;
      border: 1px solid #333;
      border-radius: 8px;
      padding: 24px;
      white-space: pre-wrap;
      font-family: monospace;
      font-size: 0.85rem;
      line-height: 1.6;
      display: none;
    }
    #status { margin-top: 12px; color: #888; font-size: 0.85rem; }
  </style>
</head>
<body>
  <h1>🤖 Code Review Bot</h1>
  <p class="caption">Powered by LLaMA 3 (local) — paste your Python code and get real AI feedback.</p>
  <textarea id="code" placeholder="Paste your Python code here..."></textarea>
  <button id="btn" onclick="submitReview()">Review Code</button>
  <p id="status"></p>
  <pre id="result"></pre>

  <script>
    const codeEl = document.getElementById("code");
    const btn = document.getElementById("btn");
    const status = document.getElementById("status");
    const result = document.getElementById("result");

    codeEl.addEventListener("input", () => {
      btn.disabled = !codeEl.value.trim();
    });
    btn.disabled = true;

    async function submitReview() {
      btn.disabled = true;
      result.style.display = "none";
      status.textContent = "Analyzing your code...";

      try {
        const res = await fetch("/review", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ code: codeEl.value }),
        });
        const data = await res.json();
        result.textContent = data.review;
        result.style.display = "block";
        status.textContent = "";
      } catch (e) {
        status.textContent = "Error: could not reach the server.";
      } finally {
        btn.disabled = false;
      }
    }
  </script>
</body>
</html>
"""


@app.post("/review")
def review(request: CodeRequest):
    result = review_code(request.code)
    return {"review": result}
