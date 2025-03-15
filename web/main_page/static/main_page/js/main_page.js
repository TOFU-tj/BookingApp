// Функция для переключения формы
function toggleForm() {
    var formContainer = document.getElementById('formContainer');

    if (formContainer.classList.contains("visible")) {
        formContainer.classList.remove("visible");
        setTimeout(() => {
            formContainer.style.display = "none";
        }, 300); // Ждём завершения анимации
    } else {
        formContainer.style.display = "block";
        setTimeout(() => {
            formContainer.classList.add("visible");
        }, 10); // Немного подождать перед добавлением класса
    }
}

// Закрытие формы при клике вне её области
document.addEventListener("click", function(event) {
    var formContainer = document.getElementById('formContainer');
    var button = document.querySelector(".button");

    if (formContainer && formContainer.classList.contains("visible") && !formContainer.contains(event.target) && event.target !== button) {
        toggleForm();
    }
});

// Подключаем обработчик отправки формы
document.addEventListener("DOMContentLoaded", function() {
    var form = document.querySelector("#formContainer form");
    if (form) {
        form.addEventListener("submit", function(event) {
            // форма будет отправляться как обычный запрос, не нужно препятствовать отправке
        });
    }
});
