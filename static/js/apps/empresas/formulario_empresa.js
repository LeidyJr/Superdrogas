function visualizar_url_pagina_propia(){
    elemento = $("#id_pagina_propia");
    if(elemento.prop('checked')){
        $("#div_url_pagina_propia").show();
        $("#id_url_pagina").prop('required', true);
    }else{
        $("#div_url_pagina_propia").hide();
        $("#id_url_pagina").prop('required', false);
    }
}
function visualizar_servicios_domicilios(){
    elemento = $("#id_servicio_domicilio");
    if(elemento.prop('checked')){
        $("#div_medios_domicilios").show();
        $("#id_medios_domicilios").prop('required', true);
    }else{
        $("#div_medios_domicilios").hide();
        $("#id_medios_domicilios").prop('required', false);
    }
}
function visualizar_configuracion_domicilios(){
    elemento = $("#id_ofrecer_domicilio");
    if(elemento.prop('checked')){
        $(".div_configuracion_domicilios").show();
        $("#id_costo_domicilio").prop('required', true);
        $("#id_km_distancia_domicilios").prop('required', true);
    }else{
        $(".div_configuracion_domicilios").hide();
        $("#id_costo_domicilio").prop('required', false);
        $("#id_km_distancia_domicilios").prop('required', false);
    }
}
$("#id_pagina_propia").change(function(){
    visualizar_url_pagina_propia(); 
});
$("#id_servicio_domicilio").change(function(){
    visualizar_servicios_domicilios();
});
$("#id_ofrecer_domicilio").change(function(){
    visualizar_configuracion_domicilios();
});
$(document).ready(function() {
    visualizar_url_pagina_propia();
    visualizar_servicios_domicilios();
    visualizar_configuracion_domicilios();
});