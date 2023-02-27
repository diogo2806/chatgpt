const chatForm = document.getElementById("chat-form");
const chatInput = document.getElementById("chat-input");
const chatLog = document.getElementById("chat-log");
let conversationId;
let messages = [];

chatForm.addEventListener("submit", (event) => {
  event.preventDefault();
  const message = chatInput.value;
  chatInput.value = "";
  addMessage("Você", message);
  messages.push({ sender: "Você", message: message });
  axios
    .post("/chat", { message, conversation_id: conversationId })
    .then((response) => {
      const answer = response.data.answer;
      conversationId = response.data.conversation_id;
      addMessage("Chatbot", answer);
      messages.push({ sender: "Chatbot", message: answer });
      displayChatLog();
    })
    .catch((error) => console.error(error));
});

function addMessage(sender, message) {
  const messageElement = document.createElement("div");
  messageElement.innerHTML = `<strong>${sender}:</strong> ${message}`;
  chatLog.appendChild(messageElement);
}

function displayChatLog() {
  chatLog.innerHTML = "";
  messages.forEach((msg) => {
    addMessage(msg.sender, msg.message);
  });
}
