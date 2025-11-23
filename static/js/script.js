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
        msg.innerHTML = text;
        chatbox.appendChild(msg);
        scrollToBottom();
        return msg;
    }

    function showTypingBubble() {
        const typing = document.createElement("div");
        typing.classList.add("bot-msg");
        typing.id = "typing";
        typing.innerHTML = "⏳ CropIntel is typing...";
        chatbox.appendChild(typing);
        scrollToBottom();
    }

    function hideTypingBubble() {
        const t = document.getElementById("typing");
        if (t) t.remove();
    }

    // ⭐ CHATGPT-LIKE TYPEWRITER + FORMATTING
    async function typeWriter(targetBubble, text) {

        // ✨ Convert markdown spacing to HTML spacing
        let formatted = text
            .replace(/\n\n/g, "<br><br>")     // double newlines → extra spacing
            .replace(/\n/g, "<br>")           // single newline → normal break
            .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>"); // Bold markdown

        targetBubble.innerHTML = "";
        let i = 0;

        while (i < formatted.length) {
            targetBubble.innerHTML += formatted[i];

            scrollToBottom();

            const char = formatted[i];
            let delay = 15;

            // Natural pauses like ChatGPT
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

            // ⭐ Apply ChatGPT style typing animation with spacing
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
