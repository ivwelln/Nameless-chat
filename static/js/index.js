const root = document.documentElement;
const isAuthenticated = root.dataset.authenticated === "true";

const authOverlay = document.getElementById("authOverlay");
const tabButtons = document.querySelectorAll(".tab-switch");
const forms = document.querySelectorAll(".auth-form");
const openAuthBtn = document.querySelector("[data-open-auth]");
const chatForm = document.getElementById("chatForm");
const addChatBtn = document.querySelector(".tab-add");
const chatTitle = document.getElementById("chatTitle");
const chatBody = document.getElementById("chatBody");
const chatEmpty = document.getElementById("chatEmpty");

function setActiveTab(tab) {
    tabButtons.forEach((btn) => btn.classList.toggle("active", btn.dataset.tab === tab));
    forms.forEach((form) => form.classList.toggle("active", form.dataset.panel === tab));
}

if (openAuthBtn) {
    openAuthBtn.addEventListener("click", () => {
        document.body.classList.add("auth-open");
    });
}

if (authOverlay) {
    authOverlay.addEventListener("click", (event) => {
        if (event.target === authOverlay) {
            document.body.classList.remove("auth-open");
        }
    });
}

tabButtons.forEach((btn) => {
    btn.addEventListener("click", () => setActiveTab(btn.dataset.tab));
});

function readForm(form) {
    return Object.fromEntries(new FormData(form).entries());
}

async function submitAuth(url, payload) {
    const res = await fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
        body: JSON.stringify(payload),
    });

    const contentType = res.headers.get("content-type") || "";
    const isJson = contentType.includes("application/json");
    const data = isJson ? await res.json().catch(() => null) : null;

    if (!res.ok) {
        const detail = data && data.detail ? data.detail : "Ошибка запроса";
        throw new Error(detail);
    }
    return data;
}

const loginForm = document.getElementById("loginForm");
const registerForm = document.getElementById("registerForm");

if (loginForm) {
    loginForm.addEventListener("submit", async (event) => {
        event.preventDefault();
        try {
            await submitAuth("/auth/login", readForm(loginForm));
            window.location.reload();
        } catch (error) {
            alert(error.message);
        }
    });
}

if (registerForm) {
    registerForm.addEventListener("submit", async (event) => {
        event.preventDefault();
        try {
            await submitAuth("/auth/register", readForm(registerForm));
            window.location.reload();
        } catch (error) {
            alert(error.message);
        }
    });
}

if (chatForm && isAuthenticated) {
    const input = chatForm.querySelector("input");
    const button = chatForm.querySelector("button");
    if (input) input.removeAttribute("disabled");
    if (button) button.removeAttribute("disabled");
}

function showEmpty(text) {
    if (!chatBody) return;
    chatBody.innerHTML = "";
    const empty = document.createElement("div");
    empty.className = "chat-empty";
    empty.textContent = text;
    chatBody.appendChild(empty);
}

function setActiveChatTab(tab) {
    document.querySelectorAll(".chat-tab").forEach((btn) => btn.classList.remove("active"));
    tab.classList.add("active");
    if (chatTitle) chatTitle.textContent = tab.textContent.trim();
}

function getInitials(name) {
    if (!name) return "??";
    const parts = name.trim().split(/\s+/);
    const first = parts[0]?.[0] || "";
    const second = parts[1]?.[0] || parts[0]?.[1] || "";
    return (first + second).toUpperCase();
}

function formatTime(value) {
    if (!value) return "";
    const date = new Date(value);
    if (Number.isNaN(date.getTime())) return String(value);
    return date.toLocaleTimeString("ru-RU", { hour: "2-digit", minute: "2-digit" });
}

function renderMessages(messages) {
    if (!chatBody) return;
    chatBody.innerHTML = "";

    if (!messages || messages.length === 0) {
        showEmpty("Сообщений пока нет.");
        return;
    }

    messages.forEach((msg) => {
        const userName = msg.user?.username || msg.username || msg.user_name || "Пользователь";
        const time = formatTime(msg.timestamp || msg.created_at);

        const message = document.createElement("div");
        message.className = "message";

        const avatar = document.createElement("div");
        avatar.className = "avatar";
        avatar.textContent = getInitials(userName);

        const bubble = document.createElement("div");
        bubble.className = "bubble";

        const meta = document.createElement("div");
        meta.className = "meta";
        meta.textContent = time ? `${userName} · ${time}` : userName;

        const text = document.createElement("div");
        text.className = "text";
        text.textContent = msg.content || "";

        bubble.appendChild(meta);
        bubble.appendChild(text);
        message.appendChild(avatar);
        message.appendChild(bubble);
        chatBody.appendChild(message);
    });
}

async function loadMessages(chatId) {
    if (!chatId) return;
    showEmpty("Загрузка...");
    try {
        const res = await fetch(`/chat/${chatId}/messages`, { credentials: "include" });
        if (!res.ok) throw new Error("Не удалось загрузить сообщения");
        const data = await res.json();
        renderMessages(data);
    } catch (error) {
        showEmpty(error.message || "Ошибка загрузки сообщений");
    }
}

function bindChatTab(tab) {
    tab.addEventListener("click", () => {
        if (!isAuthenticated) {
            document.body.classList.add("auth-open");
            return;
        }
        const chatId = tab.dataset.chatId;
        if (!chatId) return;
        setActiveChatTab(tab);
        loadMessages(chatId);
    });
}

document.querySelectorAll(".chat-tab").forEach(bindChatTab);

if (addChatBtn) {
    addChatBtn.addEventListener("click", async (event) => {
        if (!isAuthenticated) {
            document.body.classList.add("auth-open");
            return;
        }
        event.preventDefault();
        try {
            const data = await submitAuth("/chat/create");
            const tabs = addChatBtn.closest(".chat-tabs");
            if (!tabs) return;

            const newTab = document.createElement("button");
            newTab.className = "tab chat-tab";
            newTab.type = "button";
            newTab.textContent = data && data.name ? data.name : "Новый чат";
            if (data && data.id) newTab.dataset.chatId = data.id;

            tabs.insertBefore(newTab, addChatBtn);
            bindChatTab(newTab);
            setActiveChatTab(newTab);
            if (data && data.id) {
                loadMessages(data.id);
            } else {
                showEmpty("Чат создан. Обновите страницу, чтобы загрузить сообщения.");
            }
        } catch (error) {
            alert(error.message);
        }
    });
}

const firstTab = document.querySelector(".chat-tab");
if (firstTab && isAuthenticated) {
    setActiveChatTab(firstTab);
    if (firstTab.dataset.chatId) {
        loadMessages(firstTab.dataset.chatId);
    }
}
