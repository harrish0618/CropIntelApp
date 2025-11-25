document.addEventListener("DOMContentLoaded", () => {
    const sendBtn = document.getElementById("sendBtn");
    const userInput = document.getElementById("userInput");
    const chatbox = document.getElementById("chatbox");

    function scrollToBottom() {
        chatbox.scrollTop = chatbox.scrollHeight;
    }

    function addMessage(text, sender = "bot") {
        const msg = document.createElement("div");
        msg.classList.add(sender === "user" ? "user-msg" : "bot-msg");

        if (sender === "user") {
            msg.textContent = text;
        } else {
            // Bot messages: filled later by typeWriter
            msg.innerHTML = text;
        }

        chatbox.appendChild(msg);
        scrollToBottom();
        return msg;
    }

    function showTypingBubble() {
        const typing = document.createElement("div");
        typing.classList.add("bot-msg");
        typing.id = "typing";
        typing.textContent = "⏳ CropIntel is typing...";
        chatbox.appendChild(typing);
        scrollToBottom();
    }

    function hideTypingBubble() {
        const t = document.getElementById("typing");
        if (t) t.remove();
    }

    // CHATGPT-LIKE TYPEWRITER (no bold conversion, no <strong>)
    async function typeWriter(targetBubble, text) {

        // Convert only spacing, not markdown bold
        let formatted = text
            .replace(/\n\n/g, "<br><br>")   // double newline → gap
            .replace(/\n/g, "<br>");        // single newline → break

        targetBubble.innerHTML = "";
        let i = 0;

        while (i < formatted.length) {
            targetBubble.innerHTML += formatted[i];

            scrollToBottom();

            const char = formatted[i];
            let delay = 15;

            if (char === "." || char === "!" || char === "?") delay = 250;
            else if (char === ",") delay = 120;

            await new Promise(r => setTimeout(r, delay));
            i++;
        }
    }

    async function sendMessage() {
        const text = userInput.value.trim();
        if (!text) return;

        addMessage(text, "user");
        userInput.value = "";

        showTypingBubble();

        try {
            const response = await fetch("/ask", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ message: text })
            });

            const data = await response.json();
            hideTypingBubble();

            const botBubble = addMessage("", "bot");

            await typeWriter(botBubble, data.reply);

        } catch (err) {
            hideTypingBubble();
            addMessage("⚠️ Error connecting to server.", "bot");
        }
    }

    sendBtn.addEventListener("click", sendMessage);
    userInput.addEventListener("keypress", (e) => {
        if (e.key === "Enter") sendMessage();
    });
});
