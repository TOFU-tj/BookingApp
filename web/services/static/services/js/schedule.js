document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".delete-btn").forEach(button => {
        button.addEventListener("click", function () {
            let scheduleId = this.getAttribute("data-id");

            fetch(`/services/schedule/delete/${scheduleId}/`, {
                method: "POST",
                headers: {
                    "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value,
                    "Content-Type": "application/json"
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.message === "Удалено") {
                    document.getElementById(`schedule-${scheduleId}`).remove();
                }
            })
            .catch(error => console.error("Ошибка удаления:", error));
        });
    });
});
