document.addEventListener("DOMContentLoaded", function () {
    const burger = document.querySelector(".burger-menu");
    const navLinks = document.querySelector(".navbar-links");
    const dropdown = document.querySelector(".dropdown");
    const dropdownMenu = document.querySelector(".dropdown-menu");

    // Функция для открытия/закрытия бургер-меню
    function toggleMenu() {
        navLinks.classList.toggle("show");
    }

    // Функция для закрытия меню
    function closeMenu() {
        navLinks.classList.remove("show");
    }

    // Обработчик клика на бургер-меню
    burger.addEventListener("click", function (event) {
        event.stopPropagation();
        toggleMenu();
    });

    // Закрытие меню при клике вне навигации
    document.addEventListener("click", function (event) {
        if (!navLinks.contains(event.target) && !burger.contains(event.target)) {
            closeMenu();
        }
    });

    // Закрытие по нажатию Escape
    document.addEventListener("keydown", function (event) {
        if (event.key === "Escape") {
            closeMenu();
        }
    });

    // Dropdown-меню
    dropdown.addEventListener("click", function (event) {
        event.stopPropagation(); // Предотвращаем всплытие события
        dropdownMenu.classList.toggle("show");
    });

    // Закрытие dropdown при клике вне его
    document.addEventListener("click", function (event) {
        if (!dropdown.contains(event.target)) {
            dropdownMenu.classList.remove("show");
        }
    });
});
