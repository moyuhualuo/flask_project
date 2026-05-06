(function () {
    const STORAGE_KEY = "moyu-color-theme";

    function applyTheme(theme) {
        document.documentElement.dataset.theme = theme;
        localStorage.setItem(STORAGE_KEY, theme);
        const button = document.querySelector(".theme-toggle");
        if (button) {
            button.textContent = theme === "dark" ? "白" : "黑";
            button.setAttribute("aria-label", theme === "dark" ? "切换为白色主题" : "切换为黑色主题");
            button.title = button.getAttribute("aria-label");
        }
    }

    function getInitialTheme() {
        return localStorage.getItem(STORAGE_KEY) || "dark";
    }

    document.addEventListener("DOMContentLoaded", () => {
        const button = document.createElement("button");
        button.type = "button";
        button.className = "theme-toggle";
        button.addEventListener("click", () => {
            const nextTheme = document.documentElement.dataset.theme === "dark" ? "light" : "dark";
            applyTheme(nextTheme);
        });
        document.body.appendChild(button);
        applyTheme(getInitialTheme());
    });
})();
