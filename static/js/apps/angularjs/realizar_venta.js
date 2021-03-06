toastr.options = {
    "closeButton": true,
    "progressBar": true,
    "showEasing": "swing",
    "extendedTimeOut": 5000,
    "timeOut": 3000,
    "progressBar": true
}

angular.module('InicioApp', ['ui.bootstrap', 'ngMap', 'NgSwitchery'])
.config(['$httpProvider', '$interpolateProvider', function($httpProvider, $interpolateProvider) {
    $interpolateProvider.startSymbol('{$');
    $interpolateProvider.endSymbol('$}');
}])
.config(function ($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
})
.controller('ModalCancelarPedidoCtrl', function ($scope, $http, $uibModalInstance, venta) {
    $scope.venta = venta;
    $scope.motivo = {"valida": true, "texto": ""};
    $scope.eliminando_pedido = false;

    $scope.cancelar = function() {
        $scope.eliminando_pedido = true;
        if($scope.motivo.texto.length >= 10){
            $scope.motivo.valida = true;
            $http({
                method: 'POST',
                url: '/cancelar-pedido',
                data: {
                    venta_id: venta.id,
                    motivo: $scope.motivo.texto,
                },
            }).then(function successCallback(response) {
                if (response.status == 200 && response.data[0] == "Ok"){
                    toastr["success"]("El pedido ha sido marcado como cancelado");
                    $uibModalInstance.dismiss('cancel');
                }else{
                    toastr["error"]("Error con la conexión al servidor (cancelar pedido), por favor verificar conexión a internet");
                    $scope.eliminando_pedido = false;
                }
            }, function errorCallback(response) {
                $scope.eliminando_pedido = false;
                toastr["error"]("Error con la conexión al servidor (cancelar pedido), por favor verificar conexión a internet");
            });
        }else{
            $scope.motivo.valida = false;
            $scope.eliminando_pedido = false;
        }
    };

    $scope.cancel = function() {
        $uibModalInstance.dismiss('cancel');
    };
})
.controller('ModalModificarPedidoCtrl', function ($scope, $http, $uibModalInstance, $uibModal, venta, categorias_productos) {
    $scope.venta = venta;
    $scope.para_llevar = false;
    $scope.categorias_productos = categorias_productos;
    $scope.modificando_pedido = false;
    $scope.buscar_producto = "";

    var productos = {};

    if(venta.domicilio > 0){
        $scope.para_llevar = true;
    }

    function cargar_listado_productos(){
        for(indice_categoria in $scope.categorias_productos){
            productos_en_categoria = $scope.categorias_productos[indice_categoria].productos;
            for(indice_producto in productos_en_categoria){
                producto = productos_en_categoria[indice_producto];
                productos[producto.id] = producto;
            }
        }
    }
    cargar_listado_productos();

    $scope.pedido_para_llevar = function(){
        if($scope.para_llevar == true){
            $scope.venta.domicilio = domicilio;
        }else{
            $scope.venta.domicilio = 0;
        }
        actualizar_costos_totales();
    }

    function quitar_acentos(string) {
        const accents =
            "ÀÁÂÃÄÅĄàáâãäåąßÒÓÔÕÕÖØÓòóôõöøóÈÉÊËĘèéêëęðÇĆçćÐÌÍÎÏìíîïÙÚÛÜùúûüÑŃñńŠŚšśŸÿýŽŻŹžżź";
        const accentsOut =
            "AAAAAAAaaaaaaaBOOOOOOOOoooooooEEEEEeeeeeeCCccDIIIIiiiiUUUUuuuuNNnnSSssYyyZZZzzz";
        return string
            .split("")
            .map((letter, index) => {
              const accentIndex = accents.indexOf(letter);
              return accentIndex !== -1 ? accentsOut[accentIndex] : letter;
            })
            .join("");
    }

    $scope.filtrar_producto = function(producto){
        if($scope.buscar_producto != ""){
            if(quitar_acentos(producto.nombre).toLowerCase().indexOf(quitar_acentos($scope.buscar_producto).toLowerCase()) == -1){
                return false;
            }
            return true;
        }
        return false;
    }

    $scope.cambiar_cantidad_producto = function(valor, producto, indice){
        producto.cantidad += valor;
        if(producto.cantidad <= 0){
            delete $scope.venta.productos_comprados[indice];
            // eliminar "empty" de productos comprados luego de eliminar
            $scope.venta.productos_comprados = $scope.venta.productos_comprados.filter(function(e){return e});
        }
        actualizar_costos_totales();
    }

    function actualizar_costos_totales(){
        $scope.venta.subtotal = 0;
        for(id_comprados in $scope.venta.productos_comprados){
            comprado = $scope.venta.productos_comprados[id_comprados];
            $scope.venta.subtotal += (comprado.precio * comprado.cantidad);
        }
        $scope.venta.total = $scope.venta.subtotal + $scope.venta.domicilio;
    }

    function existe_producto_en_compra(listado, producto){
        for(id_listado in listado){
            comprado = listado[id_listado];
            if(comprado.producto == producto.nombre){
                return id_listado;
            }
        }
        return false;
    }

    $scope.agregar_producto = function(producto){
        var existe = existe_producto_en_compra($scope.venta.productos_comprados, producto);
        if(existe){
            $scope.venta.productos_comprados[existe].cantidad += 1;
        }else{
            $scope.venta.productos_comprados[$scope.venta.productos_comprados.length] = {
                producto: producto.nombre,
                cantidad: 1,
                precio: producto.precio,
                id_producto: producto.id,
            };
        }
        actualizar_costos_totales();
    }

    $scope.ejecutar_agregar_producto = function(producto){
        if(producto.complementos.length > 0){
            $scope.seleccionar_complementos(producto);
        }else{
            $scope.agregar_producto(producto);
        }
    }

    $scope.modificar = function(){
        $scope.modificando_pedido = true;
        $http({
            method: 'POST',
            url: '/modificar-pedido',
            data: {
                venta: venta,
            },
        }).then(function successCallback(response) {
            if (response.status == 200 && response.data[0] == "Ok"){
                toastr["success"]("El pedido ha sido modificado");
                $uibModalInstance.dismiss('cancel');
            }else{
                toastr["error"]("Error con la conexión al servidor (modificar pedido), por favor verificar conexión a internet");
                $scope.modificando_pedido = false;
            }
        }, function errorCallback(response) {
            $scope.modificando_pedido = false;
            toastr["error"]("Error con la conexión al servidor (modificar pedido), por favor verificar conexión a internet");
        });
    }
    
    $scope.cancel = function() {
        $uibModalInstance.dismiss('cancel');
    };
})
.controller('CompraController', function($scope, $http, $window, $filter, $uibModal) {
    $scope.abrir_domicilio = function (_venta) {
        var modalInstance = $uibModal.open({
            controller: "ModalDomicilioCtrl",
            templateUrl: 'modal_domicilios.html',
            resolve: {
                venta: function()
                {
                    return _venta;
                },
                marcador: function()
                {
                    for(id_geolocalizacion in $scope.informacion_tabla.geolocalizacion){
                        ubicacion = $scope.informacion_tabla.geolocalizacion[id_geolocalizacion];
                        if(ubicacion[0] == _venta.id){
                            return ubicacion;
                        }
                    }
                },
            }
        });
        modalInstance.result.then(function () {
        }, function () {
        });
    };

    $scope.seleccionar_complementos = function (_producto) {
        var modalInstance = $uibModal.open({
            controller: "ElegirComplementosProductoCtrl",
            templateUrl: 'modal_elegir_complementos.html',
            resolve: {
                producto: function()
                {
                    return _producto;
                },
            }
        });
        modalInstance.result.then(function (producto_y_complementos) {
            id_producto = producto_y_complementos[0];
            complementos = producto_y_complementos[1];
            $scope.pedir_producto_complementos(id_producto, complementos);
        }, function () {
        });
    };

    $scope.cancelar_pedido = function (_venta) {
        var modalInstance = $uibModal.open({
            controller: "ModalCancelarPedidoCtrl",
            templateUrl: 'modal_cancelar_pedido.html',
            resolve: {
                venta: function()
                {
                    return _venta;
                }
            }
        });
        modalInstance.result.then(function () {
        }, function () {
            obtener_ventas_pendientes();
        });
    };

    $scope.modificar_pedido = function (_venta) {
        var modalInstance = $uibModal.open({
            controller: "ModalModificarPedidoCtrl",
            templateUrl: 'modal_modificar_pedido.html',
            resolve: {
                venta: function()
                {
                    return _venta;
                },
                categorias_productos: function()
                {
                    return $scope.categorias_productos;
                }
            }
        });
        modalInstance.result.then(function () {
        }, function () {
            obtener_ventas_pendientes();
        });
    };

    $scope.procesando_pedido = false;
    $scope.busqueda = "";
    $scope.informacion_tabla = {
        ventas_confirmadas: null,
        pagina_actual: 1,
        ventas_por_pagina: 5,
        maxSize: 5,
        total_ventas: 0,
        geolocalizacion: []
    };
    $scope.ventas_pendientes = null;

    $scope.categoria_seleccionada = null;
    $scope.categorias_productos = null;
    $scope.usuarios = null;

    $scope.datos_pedido = {
        "usuario_seleccionado": null,
        "comentarios": "",
        "para_llevar": false,
    };

    $scope.top_productos = [];

    function obtener_top_productos(){
        $http({
            method: 'GET',
            url: 'productos/listado-top',
        }).then(function successCallback(response) {
            if (response.status == 200){
                $scope.top_productos = response.data;
            }else{
                toastr["error"]("Error con la conexión al servidor (top productos), por favor verificar conexión a internet");
            }
        }, function errorCallback(response) {
            toastr["error"]("Error con la conexión al servidor (top productos), por favor verificar conexión a internet");
        });
    }
    obtener_top_productos();

    var productos = {};
    $scope.costos_totales = {subtotal: 0, domicilio: 0, total: 3000};

    var posicion_productos_carrito = {};
    $scope.carrito_compra = [];

    $scope.carrito_compra_complementos = [];

    $scope.filtros = {nombre: "", precio_desde: null, precio_hasta: null};

    $scope.pedido_para_llevar = function(){
        if($scope.datos_pedido.para_llevar == true){
            $scope.costos_totales.domicilio = domicilio;
        }else{
            $scope.costos_totales.domicilio = 0;
        }
        actualizar_costos_totales();
    }

    $scope.terminar_pedido = function(venta){
        var mensaje = "El pedido ha sido marcado como terminado";
        var tipo_mensaje = "success";
        if(venta.terminada != true){
            mensaje = "El pedido ha sido marcado como no terminado";
            tipo_mensaje = "warning";
        }
        $http({
            method: 'POST',
            url: '/terminar-pedido',
            data: {
                venta_id: venta.id,
                venta_terminada: venta.terminada,
            },
        }).then(function successCallback(response) {
            if (response.status == 200 && response.data[0] == "Ok"){
                toastr[tipo_mensaje](mensaje);
            }else{
                toastr["error"]("Error con la conexión al servidor (terminar pedido), por favor verificar conexión a internet");
            }
        }, function errorCallback(response) {
            toastr["error"]("Error con la conexión al servidor (terminar pedido), por favor verificar conexión a internet");
        });
    }

    $scope.pagar_pedido = function(venta){
        var mensaje = "El pedido ha sido marcado como pagado";
        var tipo_mensaje = "success";
        if(venta.pagada != true){
            mensaje = "El pedido ha sido marcado como no pagado";
            tipo_mensaje = "warning";
        }
        $http({
            method: 'POST',
            url: '/pagar-pedido',
            data: {
                venta_id: venta.id,
                venta_pagada: venta.pagada,
            },
        }).then(function successCallback(response) {
            if (response.status == 200 && response.data[0] == "Ok"){
                toastr[tipo_mensaje](mensaje);
            }else{
                toastr["error"]("Error con la conexión al servidor (pagar pedido), por favor verificar conexión a internet");
            }
        }, function errorCallback(response) {
            toastr["error"]("Error con la conexión al servidor (pagar pedido), por favor verificar conexión a internet");
        });
    }


    function limpiar_pedido(){
        $scope.datos_pedido.usuario_seleccionado = null;
        $scope.datos_pedido.comentarios = "";
        $scope.datos_pedido.para_llevar = false;
        posicion_productos_carrito = {};
        $scope.carrito_compra = [];
        $scope.carrito_compra_complementos = [];
        $scope.costos_totales = {subtotal: 0, domicilio: 0, total: 3000};
    }

    $scope.realizar_pedido = function(){
        $scope.procesando_pedido = true;
        $http({
            method: 'POST',
            url: '/realizar-venta',
            data: {
                usuario: $scope.datos_pedido.usuario_seleccionado,
                comentarios: $scope.datos_pedido.comentarios,
                compras: $scope.carrito_compra,
                compras_complementos: $scope.carrito_compra_complementos,
                costos: $scope.costos_totales,
            },
        }).then(function successCallback(response) {
            if (response.status == 200 && response.data[0] == "Ok"){
                toastr["success"]("Venta realizada exitosamente");
                limpiar_pedido();
                $window.localStorage.removeItem("productos_del_pedido");
                $window.localStorage.removeItem("productos_complementos_del_pedido");
                obtener_ventas_pendientes();
                $scope.procesando_pedido = false;
                $scope.ocultar_div_venta_pedido();
            }else{
                $scope.procesando_pedido = false;
                toastr["error"]("Error con la conexión al servidor (realizar pedido), por favor verificar conexión a internet");
            }
        }, function errorCallback(response) {
            $scope.procesando_pedido = false;
            toastr["error"]("Error con la conexión al servidor (realizar pedido), por favor verificar conexión a internet");
        });
    }

    function quitar_acentos(string) {
        const accents =
            "ÀÁÂÃÄÅĄàáâãäåąßÒÓÔÕÕÖØÓòóôõöøóÈÉÊËĘèéêëęðÇĆçćÐÌÍÎÏìíîïÙÚÛÜùúûüÑŃñńŠŚšśŸÿýŽŻŹžżź";
        const accentsOut =
            "AAAAAAAaaaaaaaBOOOOOOOOoooooooEEEEEeeeeeeCCccDIIIIiiiiUUUUuuuuNNnnSSssYyyZZZzzz";
        return string
            .split("")
            .map((letter, index) => {
              const accentIndex = accents.indexOf(letter);
              return accentIndex !== -1 ? accentsOut[accentIndex] : letter;
            })
            .join("");
    }

    $scope.filtrar_producto = function(producto){
        if($scope.filtros.nombre != ""){
            if(quitar_acentos(producto.nombre).toLowerCase().indexOf(quitar_acentos($scope.filtros.nombre).toLowerCase()) == -1){
                return false;
            }
        }
        if($scope.filtros.precio_desde != null && typeof $scope.filtros.precio_desde !== "undefined"){
            if($scope.filtros.precio_desde > producto.precio){
                return false
            }
        }
        if($scope.filtros.precio_hasta != null
            && typeof $scope.filtros.precio_hasta !== "undefined"
            && $scope.filtros.precio_hasta > $scope.filtros.precio_desde){
            if($scope.filtros.precio_hasta < producto.precio){
                return false
            }
        }
        return true;
    }

    cargados_localstorage = false;

    function registrar_pedido(){
        if(cargados_localstorage == false){
            return;
        }
        var productos = [];
        var productos_complementos = [];
        for(id_carrito in $scope.carrito_compra){
            productos.push([$scope.carrito_compra[id_carrito].id, $scope.carrito_compra[id_carrito].cantidad]);
        }
        for(id_carrito in $scope.carrito_compra_complementos){
            compra = $scope.carrito_compra_complementos[id_carrito];
            productos_complementos.push([compra.id, compra.cantidad, compra.complementos_elegidos]);
        }
        $window.localStorage.setItem("productos_del_pedido", JSON.stringify(productos));
        $window.localStorage.setItem("productos_complementos_del_pedido", JSON.stringify(productos_complementos));
    }

    function cargar_pedido_guardado(){
        productos_del_pedido = JSON.parse($window.localStorage.getItem("productos_del_pedido"));
        if(productos_del_pedido != null){
            for(id_producto in productos_del_pedido){
                producto = productos_del_pedido[id_producto];
                $scope.pedir_producto(producto[0], producto[1]);
            }
        }

        productos_del_pedido = JSON.parse($window.localStorage.getItem("productos_complementos_del_pedido"));
        if(productos_del_pedido != null){
            for(id_producto in productos_del_pedido){
                producto = productos_del_pedido[id_producto];
                $scope.pedir_producto_complementos(producto[0], producto[2], producto[1]);
            }
        }
        cargados_localstorage = true;
    }

    function actualizar_costos_totales(){
        $scope.costos_totales.subtotal = 0;
        for(id_producto_carrito in $scope.carrito_compra){
            producto_carrito = $scope.carrito_compra[id_producto_carrito];
            $scope.costos_totales.subtotal += (producto_carrito.precio * producto_carrito.cantidad);
        }
        for(id_producto_carrito in $scope.carrito_compra_complementos){
            producto_carrito = $scope.carrito_compra_complementos[id_producto_carrito];
            $scope.costos_totales.subtotal += (producto_carrito.precio * producto_carrito.cantidad);
        }
        $scope.costos_totales.total = $scope.costos_totales.subtotal + $scope.costos_totales.domicilio;

        registrar_pedido();
    }

    $scope.ejecutar_pedir_producto = function(producto){
        if(producto.complementos.length > 0){
            $scope.seleccionar_complementos(producto);
        }else{
            $scope.pedir_producto(producto.id);
        }
    }

    function revisar_existencia_producto_seleccionados_con_complementos(id_producto, complementos){
        for(id_carrito in $scope.carrito_compra_complementos){
            producto_compra = $scope.carrito_compra_complementos[id_carrito];
            if(producto_compra.id == id_producto){
                if(JSON.stringify(producto_compra.complementos_elegidos) === JSON.stringify(complementos)){
                    return [id_carrito, true];
                }
            }
        }
        return [null, false];
    }

    $scope.pedir_producto_complementos = function(id_producto, complementos, cantidad=1){
        existencia = revisar_existencia_producto_seleccionados_con_complementos(id_producto, complementos)
        id_carrito = existencia[0]; existe = existencia[1];
        if(existe){
            $scope.carrito_compra_complementos[id_carrito].cantidad += 1;
        }else{
            producto = productos[id_producto];
            producto.cantidad = cantidad;
            producto.complementos_elegidos = complementos;
            $scope.carrito_compra_complementos.push(JSON.parse(JSON.stringify(producto)));
        }
        actualizar_costos_totales();
    }

    $scope.pedir_producto = function(id_producto, cantidad=1){
        if(id_producto in posicion_productos_carrito){ // el producto esta en el carrito de compra
            $scope.carrito_compra[posicion_productos_carrito[id_producto]].cantidad += 1;
        }else{
            producto = productos[id_producto];
            producto.cantidad = cantidad;
            $scope.carrito_compra.push(producto);
            posicion_productos_carrito[id_producto] = Object.keys(posicion_productos_carrito).length;
        }
        actualizar_costos_totales();
    }

    $scope.seleccionar_categoria = function(id_categoria){
        $scope.categoria_seleccionada = id_categoria;
    }

    function actualizar_posicion_productos_carrito_por_eliminacion(posicion){
        for(indice_posicion in posicion_productos_carrito){
            if(posicion_productos_carrito[indice_posicion] > posicion){
                posicion_productos_carrito[indice_posicion] -= 1;
            }
        }
    }

    $scope.ocultar_div_venta_pedido = function(){
        if($scope.costos_totales.subtotal <= 0){
            $("#modal-dialog").modal('hide');
        }
    }

    $scope.cambiar_cantidad_producto = function(valor, compra){
        compra.cantidad += valor;
        if(compra.cantidad <= 0){
            if(typeof compra.complementos_elegidos !== "undefined"){
                posicion = revisar_existencia_producto_seleccionados_con_complementos(compra.id, compra.complementos_elegidos);
                if(posicion[1] == true){
                    $scope.carrito_compra_complementos.splice(posicion[0], 1);
                }
            }else{
                $scope.carrito_compra.splice(posicion_productos_carrito[compra.id], 1);
                posicion = posicion_productos_carrito[compra.id];
                delete posicion_productos_carrito[compra.id];
                actualizar_posicion_productos_carrito_por_eliminacion(posicion);
            }
        }
        actualizar_costos_totales();
        $scope.ocultar_div_venta_pedido();
    }

    inicializar();

    function cargar_listado_productos(){
        for(indice_categoria in $scope.categorias_productos){
            productos_en_categoria = $scope.categorias_productos[indice_categoria].productos
            for(indice_producto in productos_en_categoria){
                producto = productos_en_categoria[indice_producto];
                productos[producto.id] = producto;
            }
        }
    }

    function inicializar(){
        obtener_categorias_y_productos();
        obtener_usuarios();
        obtener_ventas_pendientes();
    }

    function obtener_categorias_y_productos(){
        $http({
            method: 'GET',
            url: '/categorias/todos'
        }).then(function successCallback(response) {
            if(response.status == 200){
                $scope.categorias_productos = response.data;
                cargar_listado_productos();
                cargar_pedido_guardado();
            }else{
                toastr["error"]("Error con la conexión al servidor (categorías y productos), por favor verificar conexión a internet");
            }
        }, function errorCallback(response) {
            toastr["error"]("Error con la conexión al servidor (categorías y productos), por favor verificar conexión a internet");
        });
    }

    function asignar_geolocalizacion_de_domicilios(){
        $scope.informacion_tabla.geolocalizacion = []
        for(id_venta in $scope.informacion_tabla.ventas_confirmadas){
            venta = $scope.informacion_tabla.ventas_confirmadas[id_venta];
            if(venta.es_domicilio == true){
                $scope.informacion_tabla.geolocalizacion.push([venta.id, [venta.ubicacion.latitud, venta.ubicacion.longitud]]);
            }
        }
    }

    function obtener_ventas_pendientes(){
        $http({
            method: 'GET',
            url: '/listado-ventas-confirmadas'
        }).then(function successCallback(response) {
            if(response.status == 200){
                $scope.informacion_tabla.ventas_confirmadas = response.data;
                $scope.informacion_tabla.total_ventas = $scope.informacion_tabla.ventas_confirmadas.length;
                asignar_geolocalizacion_de_domicilios();
            }else{
                toastr["error"]("Error con la conexión al servidor (servicio de pedidos no terminados), por favor verificar conexión a internet");
            }
        }, function errorCallback(response) {
            toastr["error"]("Error con la conexión al servidor (servicio de pedidos no terminados), por favor verificar conexión a internet");
        });
    }
    
    function obtener_usuarios(){
        $http({
            method: 'GET',
            url: '/usuarios/todos/'
        }).then(function successCallback(response) {
            if(response.status == 200){
                $scope.usuarios = response.data;
            }else{
                toastr["error"]("Error con la conexión al servidor (servicio de usuarios), por favor verificar conexión a internet");
            }
        }, function errorCallback(response) {
            toastr["error"]("Error con la conexión al servidor (servicio de usuarios), por favor verificar conexión a internet");
        });
    }

    $scope.actualizar_ventas_pendientes = function(){
        obtener_ventas_pendientes();
    }
});