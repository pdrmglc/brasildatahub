document.addEventListener('DOMContentLoaded', function() {
    const forms = document.querySelectorAll('form');

    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            const anoInicial = parseInt(form.querySelector('[name="ano_inicial"]').value);
            const anoFinal = parseInt(form.querySelector('[name="ano_final"]').value);

            if (anoInicial > anoFinal) {
                alert('O ano inicial não pode ser maior que o ano final.');
                event.preventDefault(); // Impede o envio do formulário
            }
        });
    });
});
