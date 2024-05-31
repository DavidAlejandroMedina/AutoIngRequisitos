const chatSubmitBtn = document.getElementById("chat-submit");
chatSubmitBtn.addEventListener("click", sendMessage);

const inputChat = document.getElementById("user-input")
inputChat.addEventListener("keydown", function(event){
  if (event.key === 'Enter') {
    sendMessage();
  }
})


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

  console.log(data.message)

  const assistantMessageDiv = document.createElement("div");
  assistantMessageDiv.className = "assistant-message";
  assistantMessageDiv.textContent = data.message;
  const boldMessage = data.message.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
  assistantMessageDiv.innerHTML = boldMessage.replace(/\n/g, '<br>');
  chatBox.appendChild(assistantMessageDiv);
  

  chatBox.scrollTop = chatBox.scrollHeight;
}
