document.addEventListener("DOMContentLoaded", function() {
    const inputs = document.querySelectorAll(".service-form input, .service-form textarea");
    inputs.forEach(input => {
        input.addEventListener("focus", () => {
            input.style.boxShadow = "0 0 10px rgba(255, 75, 43, 0.8)";
        });
        input.addEventListener("blur", () => {
            input.style.boxShadow = "none";
        });
    });
});
