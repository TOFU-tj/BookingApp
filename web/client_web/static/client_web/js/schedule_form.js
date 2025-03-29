document.addEventListener("DOMContentLoaded", function () {
    const formContainer = document.querySelector(".form-container");
    const slugCompany = formContainer.getAttribute("data-slug-company");
    const slugUsername = formContainer.getAttribute("data-slug-username");

    const dateSelect = document.getElementById("id_select_day");
    const timeSlotSelect = document.getElementById("id_select_time");

    if (dateSelect && timeSlotSelect) {
        dateSelect.addEventListener("change", function () {
            const selectedDateId = dateSelect.value;

            if (selectedDateId) {
                // Очищаем предыдущие слоты
                timeSlotSelect.innerHTML = '<option value="">Загрузка...</option>';
                timeSlotSelect.disabled = true;

                // Загружаем доступные временные слоты через AJAX
                fetch(`/client_web_page/${slugCompany}/${slugUsername}/schedule/get-available-slots/?date=${selectedDateId}`, {
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest'
                    }
                })
                    .then(response => response.json())
                    .then(slots => {
                        timeSlotSelect.innerHTML = ""; // Очищаем предыдущие слоты

                        if (slots.length > 0) {
                            slots.forEach(slot => {
                                const option = document.createElement("option");
                                option.value = slot.id;
                                option.textContent = `${slot.start_time} - ${slot.end_time}`;
                                timeSlotSelect.appendChild(option);
                            });

                            timeSlotSelect.disabled = false; // Активируем выпадающий список
                        } else {
                            timeSlotSelect.innerHTML = '<option value="" disabled>Нет доступных слотов</option>';
                            timeSlotSelect.disabled = true; // Деактивируем выпадающий список
                        }
                    })
                    .catch(error => {
                        console.error("Ошибка при загрузке слотов:", error);
                        timeSlotSelect.innerHTML = '<option value="" disabled>Ошибка загрузки</option>';
                        timeSlotSelect.disabled = true;
                    });
            } else {
                timeSlotSelect.innerHTML = '<option value="" disabled>Выберите дату</option>';
                timeSlotSelect.disabled = true; // Деактивируем выпадающий список
            }
        });
    }
});