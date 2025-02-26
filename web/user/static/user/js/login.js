// Функция для переключения видимости пароля
function togglePassword() {
    var passwordField = document.getElementById('id_password');
    var toggleIcon = document.querySelector('.toggle-password');
    
    // Переключаем тип поля ввода
    if (passwordField.type === "password") {
        passwordField.type = "text"; // Показываем пароль
        toggleIcon.textContent = "🙈"; // Меняем иконку на "обезьянка"
    } else {
        passwordField.type = "password"; // Скрываем пароль
        toggleIcon.textContent = "👁"; // Меняем иконку обратно на глазик
    }
}

