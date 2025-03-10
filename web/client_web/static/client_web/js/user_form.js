document.addEventListener("DOMContentLoaded", function() {
    const dropdownBtn = document.getElementById("schedule-btn");
    const dropdownContent = document.getElementById("schedule-list");
    const scheduleInput = document.getElementById("schedule-input");
    
    // Получаем все элементы списка для выбора
    const dropdownItems = document.querySelectorAll(".dropdown-item");

    // Обработчик для выбора времени из списка
    dropdownItems.forEach(item => {
        item.addEventListener('click', function () {
            const scheduleId = item.getAttribute('data-value');
            scheduleInput.value = scheduleId; // Обновляем скрытое поле
            dropdownBtn.textContent = item.textContent; // Обновляем текст на кнопке
            dropdownContent.style.display = "none"; // Закрываем список после выбора
        });
    });

    // Открытие списка при клике на кнопку
    dropdownBtn.addEventListener("click", function(event) {
        // Предотвращаем закрытие списка, если клик был внутри
        event.stopPropagation();
        dropdownContent.style.display = dropdownContent.style.display === "block" ? "none" : "block";
    });

    // Закрытие списка при клике вне его
    document.addEventListener("click", function(event) {
        if (!dropdownBtn.contains(event.target) && !dropdownContent.contains(event.target)) {
            dropdownContent.style.display = "none";
        }
    });
});

