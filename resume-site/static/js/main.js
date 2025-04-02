document.addEventListener("DOMContentLoaded", () => {
    console.log("Сайт-резюме Аскара запущен!");

    // Плавная прокрутка
    document.querySelectorAll('nav a[href^="#"]').forEach(link => {
        link.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({ behavior: 'smooth' });
            }
        });
    });

    // Кнопка наверх
    const toTop = document.getElementById('toTop');
    if (toTop) {
        window.addEventListener('scroll', () => {
            window.pageYOffset > 300
                ? toTop.classList.remove('hidden')
                : toTop.classList.add('hidden');
        });

        toTop.addEventListener('click', () => {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
    }

    // Отправка формы
    const form = document.getElementById('contactForm');
    const successPopup = document.getElementById('successPopup');
    if (form) {
        form.addEventListener('submit', async function (e) {
            e.preventDefault();

            const formData = new FormData(this);

            try {
                const response = await fetch('/send_message', {
                    method: 'POST',
                    body: formData
                });

                const result = await response.json();
                this.reset();

                // Всплывающее сообщение
                if (successPopup) {
                    successPopup.classList.remove('opacity-0');
                    successPopup.classList.add('opacity-100');
                    setTimeout(() => {
                        successPopup.classList.remove('opacity-100');
                        successPopup.classList.add('opacity-0');
                    }, 3000);
                }
            } catch (err) {
                console.error('Ошибка:', err);
            }
        });
    }

    // Обработка переключения языка
    const langLinks = document.querySelectorAll('a[href^="/?lang="]');
    langLinks.forEach(link => {
        link.addEventListener("click", function (e) {
            e.preventDefault();
            const lang = this.href.split('lang=')[1];
            const base = window.location.pathname;
            window.location.href = `${base}?lang=${lang}`;
        });
    });
});