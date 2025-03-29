document.addEventListener("DOMContentLoaded", function () {
    const dateSelect = document.getElementById("id_date");
    const timeSlotSelect = document.getElementById("id_time_slot");

    // Получаем slug_company и slug_username из URL
    const urlParams = new URLSearchParams(window.location.search);
    const slugCompany = urlParams.get('slug_company');
    const slugUsername = urlParams.get('slug_username');

    if (!slugCompany || !slugUsername) {
        console.error("Slug company or slug username is missing in the URL!");
        return;
    }

    dateSelect.addEventListener("change", function () {
        const selectedDate = dateSelect.value;

        if (selectedDate) {
            // Очищаем предыдущие слоты
            timeSlotSelect.innerHTML = '<option value="">Загрузка...</option>';
            timeSlotSelect.disabled = true;

            // Загружаем доступные временные слоты через AJAX
            fetch(`/${slugCompany}/${slugUsername}/get-available-slots/?date=${selectedDate}`, {
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
});