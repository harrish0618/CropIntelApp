/* GENERAL PAGE SETTINGS */
body {
    margin: 0;
    padding: 0;
    font-family: "Poppins", sans-serif;
    overflow: hidden;
}

/* ===========================
   BACKGROUND VIDEO
=========================== */
#bg-video {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    object-fit: cover;
    z-index: -10;
    filter: brightness(82%) blur(0.5px);
}

/* ===========================
   MAIN GLASS PANEL
=========================== */
.main-container {
    width: 80%;
    max-width: 900px;
    padding: 30px;

    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);

    background: rgba(255, 255, 255, 0.25);
    border-radius: 24px;
    backdrop-filter: blur(18px);
    -webkit-backdrop-filter: blur(18px);

    box-shadow: 0 0 50px rgba(0,0,0,0.25);

    animation: fadeSlide 1.6s ease forwards;
    z-index: 10;
}

@keyframes fadeSlide {
    from { opacity: 0; transform: translate(-50%, -40%); }
    to   { opacity: 1; transform: translate(-50%, -50%); }
}

/* ===========================
   HEADER WITH LOGO
=========================== */
.header {
    text-align: center;
    margin-bottom: 20px;
}

.logo {
    width: 90px;
    animation: logoPulse 3s infinite ease-in-out;
}

@keyframes logoPulse {
    0% { transform: scale(1); opacity: 0.9; }
    50% { transform: scale(1.07); opacity: 1; }
    100% { transform: scale(1); opacity: 0.9; }
}

.subtitle {
    font-weight: 300;
    margin-top: -10px;
    opacity: 0.9;
}

/* ===========================
   CHATBOX
=========================== */
.chatbox {
    height: 350px;
    overflow-y: auto;
    padding-right: 10px;
    margin-bottom: 20px;
}

.chatbox::-webkit-scrollbar {
    width: 6px;
}
.chatbox::-webkit-scrollbar-thumb {
    background: #4CAF50;
    border-radius: 10px;
}

/* ===========================
   CHAT BUBBLES
=========================== */
.user-msg, .bot-msg {
    padding: 12px 16px;
    border-radius: 16px;
    margin: 10px 0;
    max-width: 75%;
    animation: bubblePop 0.3s ease forwards;
}

@keyframes bubblePop {
    0% { transform: scale(0.7); opacity: 0; }
    100% { transform: scale(1); opacity: 1; }
}

.user-msg {
    background: rgba(80, 205, 80, 0.8);
    color: #fff;
    align-self: flex-end;
    margin-left: auto;
}

.bot-msg {
    background: rgba(255, 255, 255, 0.65);
    color: #000;
    margin-right: auto;
}

/* ===========================
   INPUT BAR
=========================== */
.input-row {
    display: flex;
    gap: 10px;
}

#userInput {
    flex: 1;
    padding: 14px;
    border-radius: 12px;
    border: none;
    font-size: 16px;
    outline: none;
    background: rgba(255, 255, 255, 0.85);
}

.send-btn {
    padding: 14px 20px;
    font-size: 18px;
    border: none;
    background: #2e8b57;
    color: white;
    border-radius: 12px;
    cursor: pointer;
    transition: 0.2s ease;
}

.send-btn:hover {
    transform: scale(1.1);
    background: #36a569;
}
