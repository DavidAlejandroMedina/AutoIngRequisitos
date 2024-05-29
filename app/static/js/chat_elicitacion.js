const chatSubmitBtn = document.getElementById("chat-submit");

chatSubmitBtn.addEventListener("click", sendMessage);

async function sendMessage() {
  const userInput = document.getElementById("user-input").value;
  if (userInput.trim() === "") return;

  const chatBox = document.getElementById("chat-box");
  const userMessageDiv = document.createElement("div");
  userMessageDiv.className = "user-message";
  userMessageDiv.textContent = userInput;
  chatBox.appendChild(userMessageDiv);

  document.getElementById("user-input").value = "";

  const response = await fetch("/chat", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ message: userInput }),
  });
  const data = await response.json();

  const assistantMessageDiv = document.createElement("div");
  assistantMessageDiv.className = "assistant-message";
  assistantMessageDiv.textContent = data.message;
  chatBox.appendChild(assistantMessageDiv);

  chatBox.scrollTop = chatBox.scrollHeight;
}
