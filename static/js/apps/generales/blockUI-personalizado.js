
// Situa el mensaje: "enviando..." en la mitad de la pantalla
$("form.bloquear-ui-enviar").submit(function (event) {
    $.blockUI({
        message: '<h4 style="color:#ffffff !important;"> Procesando datos...</h4>',
        css: {
            border: 'none',
            padding: '15px',
            backgroundColor: '#005bbf',
            '-webkit-border-radius': '10px',
            '-moz-border-radius': '10px',
            opacity: 1,
            color: '#ffffff'
        }
    });
    setTimeout($.unblockUI, 200000);
});

// Situa el mensaje: "Calculando..." en la mitad de la pantalla
$("form.bloquear-ui-calculo").submit(function (event) {
    $.blockUI({
        message: '<h4 style="color:#ffffff !important;"> Calculando...</h4>',
        css: {
            border: 'none',
            padding: '15px',
            backgroundColor: '#005bbf',
            '-webkit-border-radius': '10px',
            '-moz-border-radius': '10px',
            opacity: 1,
            color: '#ffffff'
        }
    });
    setTimeout($.unblockUI, 200000);
});
