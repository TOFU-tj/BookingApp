$(document).ready(function() {
    // Перехватываем отправку формы
    $('.add-to-basket-form').on('submit', function(event) {
        event.preventDefault(); // Предотвращаем стандартную отправку формы

        var form = $(this); // Получаем саму форму
        var serviceId = form.find('input[name="service_id"]').val(); // Получаем ID услуги

        $.ajax({
            type: 'POST',
            url: form.attr('action'),
            data: form.serialize(), // Отправляем все данные формы
            success: function(response) {
                // Когда запрос прошел успешно
                if (response.success) {
                    // Показываем уведомление, что товар добавлен в корзину
                    $('#notification-' + serviceId).show();
                    setTimeout(function() {
                        $('#notification-' + serviceId).fadeOut();
                    }, 2000); // Убираем уведомление через 2 секунды
                }
            },
            error: function(xhr, errmsg, err) {
                console.log('Ошибка при добавлении в корзину: ', errmsg);
            }
        });
    });
});

