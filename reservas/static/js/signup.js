document.addEventListener('DOMContentLoaded', function () {
    const password1 = document.getElementById('id_password1');
    const password2 = document.getElementById('id_password2');
    const icon1 = document.querySelector('#id_icon_password1');
    const icon2 = document.querySelector('#id_icon_password2');

    const buttons = document.querySelectorAll('.btn-primary');
    const buttonsCancelar = document.querySelectorAll('.btn-danger');

    icon1.addEventListener('click', event => {
        event.preventDefault();
        if (password1.type === 'password') {
            password1.type = 'text',
            icon1.classList.remove('bi-eye-fill');
            icon1.classList.add('bi-eye-slash-fill');
        } else {
            password1.type = 'password';
            icon1.classList.add('bi-eye-fill');
            icon1.classList.remove('bi-eye-slash-fill');
        }
    });

    icon2.addEventListener('click', event => {
        event.preventDefault();
        if (password2.type === 'password') {
            password2.type = 'text',
            icon2.classList.remove('bi-eye-fill');
            icon2.classList.add('bi-eye-slash-fill');
        } else {
            password2.type = 'password';
            icon2.classList.add('bi-eye-fill');
            icon2.classList.remove('bi-eye-slash-fill');
        }
    });

    buttons.forEach((button, index) => {
        button.addEventListener('click', function () {
            const currentCard = document.getElementById('card_' + (index + 1));
            const nextCard = document.getElementById('card_' + (index + 2));

            currentCard.style.display = 'none';  // Oculta la tarjeta actual
            if (nextCard) {
                nextCard.style.display = 'block';  // Muestra la siguiente tarjeta si existe
            }
        });
    });

    buttonsCancelar.forEach((button, index) => {
        button.addEventListener('click', function () {
            const currentCard = document.getElementById('card_' + (index + 2));
            const previousCard = document.getElementById('card_' + (index + 1));

            currentCard.style.display = 'none';  // Oculta la tarjeta actual
            if (previousCard) {
                previousCard.style.display = 'block';  // Muestra la tarjeta anterior si existe
            }
        });
    });
});