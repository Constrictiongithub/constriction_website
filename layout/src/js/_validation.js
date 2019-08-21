$(function () {
    Array.prototype.filter.call($('form.needs-validation'), function(form) {
        $(form).on('submit', function(event) {
            if (form.checkValidity() === false) {
                event.preventDefault();
                event.stopPropagation();
                $(".percentage").trigger("keyup");
                $(".thousandseparator").trigger("keyup");
            }
            form.classList.add('was-validated');
        });
    });
});