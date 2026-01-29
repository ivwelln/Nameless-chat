const root = document.documentElement;
const isAuthenticated = root.dataset.authenticated === "true";

const authOverlay = document.getElementById("authOverlay");
const tabButtons = document.querySelectorAll(".tab-switch");
const forms = document.querySelectorAll(".auth-form");
const openAuthBtn = document.querySelector("[data-open-auth]");
const chatForm = document.getElementById("chatForm");
const addChatBtn = document.querySelector(".tab-add");

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

    if (!res.ok) {
        const err = await res.json().catch(() => ({ detail: "Ошибка запроса" }));
        throw new Error(err.detail || "Ошибка запроса");
    }
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

if (addChatBtn) {
    addChatBtn.addEventListener("click", async (event) => {
        if (!isAuthenticated) {
            document.body.classList.add("auth-open");
            return;
        }
        event.preventDefault();
        try {
            await submitAuth("/chat/create");
            const tabs = addChatBtn.closest(".chat-tabs");
            if (!tabs) return;

            const newTab = document.createElement("button");
            newTab.className = "tab active";
            newTab.type = "button";
            newTab.textContent = "Новый чат";

            tabs.insertBefore(newTab, addChatBtn);
        } catch (error) {
            alert(error.message);
        }
    });
}
