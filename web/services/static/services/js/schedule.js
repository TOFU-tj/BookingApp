document.addEventListener("DOMContentLoaded", function () {
    flatpickr(".datepicker", {
        enableTime: false,
        dateFormat: "Y-m-d",
        locale: "ru"
    });

    flatpickr(".timepicker", {
        enableTime: true,
        noCalendar: true,
        dateFormat: "H:i",
        time_24hr: true
    });
});
