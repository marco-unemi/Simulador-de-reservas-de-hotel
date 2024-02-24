document.addEventListener('DOMContentLoaded', function () {

    const card1 = document.getElementById('card_1');
    const card2 = document.getElementById('card_2');
    const card3 = document.getElementById('card_3');
    const card4 = document.getElementById('card_4');

    const buttonCard2 = document.getElementById('id_card_2');
    const buttonCard3 = document.getElementById('id_card_3');
    const buttonCard4 = document.getElementById('id_card_4');

    buttonCard2.addEventListener('click', event => {
        event.preventDefault()
        card1.style.display = 'none';
        card3.style.display = 'none';
        card4.style.display = 'none';
        card2.style.display = 'block';
    })


    buttonCard3.addEventListener('click', event => {
        event.preventDefault()
        card1.style.display = 'none';
        card2.style.display = 'none';
        card4.style.display = 'none';
        card3.style.display = 'block';
    })

    buttonCard4.addEventListener('click', event => {
        event.preventDefault()
        card1.style.display = 'none';
        card2.style.display = 'none';
        card3.style.display = 'none';
        card4.style.display = 'block';
    })

});


