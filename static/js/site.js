// Переключение темы. Выбор сохраняется в браузере.
const themeButton = document.getElementById("theme-toggle");
const savedTheme = localStorage.getItem("journal-theme");
if (savedTheme === "light") {
    document.body.classList.add("light-theme");
}
if (themeButton) {
    themeButton.addEventListener("click", function () {
        document.body.classList.toggle("light-theme");
        if (document.body.classList.contains("light-theme")) {
            localStorage.setItem("journal-theme", "light");
        } else {
            localStorage.setItem("journal-theme", "dark");
        }
    });
}
