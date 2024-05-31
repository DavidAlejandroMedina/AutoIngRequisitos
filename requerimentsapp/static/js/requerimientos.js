const fileSubmitBtn = document.getElementById("chat-submit");
fileSubmitBtn.addEventListener("click", sendFile);


const inputChat = document.getElementById("user-input")
inputChat.addEventListener("keydown", function(event){
  if (event.key === 'Enter') {
    sendFile();
  }
})

async function sendFile() {
  var userInput = document.getElementById("user-input").value;
  if (userInput.trim() === "") {
    userInput = "Describe el último documento y solicita que te de más información"
  }


  const fileInput = document.getElementById("file-input");
  const file = fileInput.files[0];

  if (!file || file.type !== 'application/pdf') {
    console.error("No se seleccionó un archivo PDF");
    return;
  }

  const chatBox = document.getElementById("chat-box");
  const userMessageDiv = document.createElement("div");
  userMessageDiv.className = "user-message";
  userMessageDiv.textContent = userInput;
  chatBox.appendChild(userMessageDiv);
  document.getElementById("user-input").value = "";
 
  var formData = new FormData();
  formData.append('pdf', file);
  formData.append('message', userInput)

  const response = await fetch('/upload_file', {
    method: 'POST',
    body: formData
  })
  const data = await response.json();
  print(data.message)

  const assistantMessageDiv = document.createElement("div");
  assistantMessageDiv.className = "assistant-message";
  assistantMessageDiv.textContent = data.message;
  const boldMessage = data.message.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
  assistantMessageDiv.innerHTML = boldMessage.replace(/\n/g, '<br>');
  chatBox.appendChild(assistantMessageDiv);

  chatBox.scrollTop = chatBox.scrollHeight;
}

