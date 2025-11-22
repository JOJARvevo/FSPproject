(() => {
    const card = document.querySelector(".countdown-card");
    if (card) {
        const target = new Date(card.dataset.eventDate);
        const pad = (n) => n.toString().padStart(2, "0");
        const updateTimer = () => {
            const now = new Date();
            const diff = target - now;
            if (diff <= 0) {
                ["days", "hours", "minutes", "seconds"].forEach((id) => {
                    document.getElementById(id).textContent = "00";
                });
                return;
            }
            const days = Math.floor(diff / (1000 * 60 * 60 * 24));
            const hours = Math.floor((diff / (1000 * 60 * 60)) % 24);
            const minutes = Math.floor((diff / (1000 * 60)) % 60);
            const seconds = Math.floor((diff / 1000) % 60);
            document.getElementById("days").textContent = pad(days);
            document.getElementById("hours").textContent = pad(hours);
            document.getElementById("minutes").textContent = pad(minutes);
            document.getElementById("seconds").textContent = pad(seconds);
        };
        updateTimer();
        setInterval(updateTimer, 1000);
    }
})();

(() => {
    const root = document.documentElement;
    const toggle = document.getElementById("themeToggle");
    const stored = localStorage.getItem("theme");
    const applyTheme = (theme) => {
        root.setAttribute("data-theme", theme);
        document.body.setAttribute("data-theme", theme);
        const lightLabel = toggle?.querySelector(".light-label");
        const darkLabel = toggle?.querySelector(".dark-label");
        if (theme === "dark") {
            lightLabel?.classList.add("d-none");
            darkLabel?.classList.remove("d-none");
        } else {
            lightLabel?.classList.remove("d-none");
            darkLabel?.classList.add("d-none");
        }
    };

    applyTheme(stored === "dark" ? "dark" : "light");

    toggle?.addEventListener("click", () => {
        const current = root.getAttribute("data-theme") === "dark" ? "dark" : "light";
        const next = current === "dark" ? "light" : "dark";
        localStorage.setItem("theme", next);
        applyTheme(next);
    });
})();
