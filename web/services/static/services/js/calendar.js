document.addEventListener("DOMContentLoaded", function () {
    const calendarElement = document.getElementById("calendar");
    if (!calendarElement) {
        console.error("Календарь не найден на странице!");
        return; // Если элемент не найден, остановим выполнение скрипта
    }

    const today = new Date();
    let currentMonth = today.getMonth();
    let currentYear = today.getFullYear();

    // Рендерим календарь
    function renderCalendar(month, year) {
        const firstDay = new Date(year, month).getDay();
        const lastDate = new Date(year, month + 1, 0).getDate();
        
        // Очищаем старый календарь
        calendarElement.innerHTML = "";

        // Добавляем пустые ячейки до первого дня месяца
        for (let i = 0; i < firstDay; i++) {
            const emptyCell = document.createElement("div");
            calendarElement.appendChild(emptyCell);
        }

        // Генерируем дни месяца
        for (let day = 1; day <= lastDate; day++) {
            const dayElement = document.createElement("div");
            dayElement.classList.add("day");
            dayElement.textContent = day;
            dayElement.dataset.date = `${year}-${String(month + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`;

            // Блокируем прошедшие даты
            const dayDate = new Date(year, month, day);
            if (dayDate < today) {
                dayElement.classList.add("disabled");
            }

            // Добавляем обработчик клика
            dayElement.addEventListener("click", function () {
                if (!dayElement.classList.contains("disabled")) {
                    const dateInput = document.getElementById("schedule_date");
                    dateInput.value = dayElement.dataset.date; // Сохраняем дату в поле
                    dayElement.classList.toggle("selected"); // Отображаем выбранную дату
                }
            });

            calendarElement.appendChild(dayElement);
        }
    }

    // Переключение месяцев
    function changeMonth(offset) {
        currentMonth += offset;
        if (currentMonth > 11) {
            currentMonth = 0;
            currentYear++;
        } else if (currentMonth < 0) {
            currentMonth = 11;
            currentYear--;
        }
        renderCalendar(currentMonth, currentYear);
    }

    // Инициализируем календарь
    renderCalendar(currentMonth, currentYear);

    // Обработчики для кнопок переключения месяца
    document.getElementById("prev-month").addEventListener("click", function () {
        changeMonth(-1);
    });

    document.getElementById("next-month").addEventListener("click", function () {
        changeMonth(1);
    });
});
