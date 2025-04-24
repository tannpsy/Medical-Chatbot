document.getElementById("sendButton").addEventListener("click", () => {
    const userInput = document.getElementById("userInput").value.trim();
    if (!userInput) return;

    addMessage("user", userInput);
    document.getElementById("userInput").value = "";

    fetch("/get_diagnosis", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ symptoms: userInput })
    })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                addMessage("bot", `🤖 I'm sorry, but ${data.error}`);
            } else {
                const response = `
                    🤔 Here's what I found based on your symptoms:<br><br>
                    🌟 <strong>Disease:</strong> ${data.disease} <br>
                    📋 <strong>Description:</strong> ${data.description} <br>
                    💊 <strong>Recommended Treatment:</strong> ${data.treatment} <br>
                    🛡️ <strong>Prevention Tips:</strong> ${data.prevention}
                `;
                addMessage("bot", response);
            }
        })
        .catch(() => addMessage("bot", "Oops! Something went wrong. Please try again."));
});

function addMessage(sender, content) {
    const chatbox = document.getElementById("chatbox");
    const message = document.createElement("div");
    message.classList.add("message", sender);
    message.innerHTML = `<div class="message-content">${content}</div>`;
    chatbox.appendChild(message);
    chatbox.scrollTop = chatbox.scrollHeight;
}
