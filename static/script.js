const display = document.getElementById("display");
const keys = document.getElementById("keys");

let expression = "";
let evaluated = false;
const MAX_LENGTH = 500;

function cleanExpression() {
  if (display.classList.contains("error")) {
    expression = "";
    display.classList.remove("error");
    evaluated = false;
  }
}

function updateDisplay() {
  display.textContent = expression || "0";
}

function appendChar(char) {
  cleanExpression();

  if (evaluated) {
    expression = "";
    evaluated = false;
  }

  if (expression.length + char.length > MAX_LENGTH) {
    return;
  }

  expression += char;
  updateDisplay();
}

function backspace() {
  cleanExpression();
  evaluated = false;
  expression = expression.slice(0, -1);
  updateDisplay();
}

function clearAll() {
  expression = "";
  evaluated = false;
  display.classList.remove("error");
  updateDisplay();
}

async function evaluateExpression() {
  cleanExpression();

  if (!expression.trim()) {
    return;
  }

  display.textContent = "…";

  try {
    const response = await fetch("/api/calculate", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ expression }),
    });

    const data = await response.json();

    if (!response.ok) {
      expression = "";
      evaluated = false;
      display.textContent = data.error || "Error";
      display.classList.add("error");
      return;
    }

    expression = String(data.result);
    evaluated = true;
    display.classList.remove("error");
    updateDisplay();
  } catch {
    expression = "";
    evaluated = false;
    display.textContent = "Network error";
    display.classList.add("error");
  }
}

function handleButton(button) {
  const action = button.dataset.action;

  if (action === "append") {
    appendChar(button.dataset.char);
  } else if (action === "backspace") {
    backspace();
  } else if (action === "clear") {
    clearAll();
  } else if (action === "evaluate") {
    evaluateExpression();
  }
}

keys.addEventListener("click", (event) => {
  const button = event.target.closest("button");

  if (!button) {
    return;
  }

  handleButton(button);
});

document.addEventListener("keydown", (event) => {
  if (event.key === "Enter" || event.key === "=") {
    event.preventDefault();
    evaluateExpression();
  } else if (event.key === "Backspace") {
    event.preventDefault();
    backspace();
  } else if (event.key === "Escape") {
    clearAll();
  } else if (event.key === "^") {
    event.preventDefault();
    appendChar("**");
  } else if (/^[0-9+\-*/%.()]+$/.test(event.key)) {
    appendChar(event.key);
  }
});
