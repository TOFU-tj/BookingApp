document.addEventListener('DOMContentLoaded', function () {
    const linkInput = document.getElementById('link-input');
    const copyButton = document.getElementById('copy-button');

    if (copyButton && linkInput) {
        copyButton.addEventListener('click', async function () {
            try {
                // Выделяем текст в поле ввода
                linkInput.select();
                linkInput.setSelectionRange(0, 99999); // Для мобильных устройств

                // Копируем текст в буфер обмена
                await navigator.clipboard.writeText(linkInput.value);

                // Добавляем класс "copied" для обратной связи
                copyButton.classList.add('copied');
                copyButton.textContent = 'Скопировано!';

                // Возвращаем исходное состояние через 2 секунды
                setTimeout(() => {
                    copyButton.classList.remove('copied');
                    copyButton.textContent = 'Копировать';
                }, 2000);
            } catch (err) {
                console.error('Не удалось скопировать текст: ', err);
                alert('Не удалось скопировать ссылку. Пожалуйста, попробуйте еще раз.');
            }
        });
    }
});