document.addEventListener("DOMContentLoaded", function () {
    const pricingCard = document.querySelector(".pricing-card");

    // Добавляем класс для запуска анимации
    setTimeout(() => {
        pricingCard.classList.add("animate");
    }, 300);
});