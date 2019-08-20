toastr.options = {
    "closeButton": true,
    "progressBar": true,
    "showEasing": "swing",
    "extendedTimeOut": 5000,
    "timeOut": 3000,
    "progressBar": true
}

angular.module('InicioApp', ['ui.bootstrap'])
.config(['$httpProvider', '$interpolateProvider', function($httpProvider, $interpolateProvider) {
    $interpolateProvider.startSymbol('{$');
    $interpolateProvider.endSymbol('$}');
}])
.config(function ($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
})
.controller('ElegirComplementosProductoCtrl', function ($scope, $uibModalInstance, producto) {
    $scope.producto = producto;
    $scope.complementos_seleccionados = [];
    $scope.complementos_correctos = true;

    function inicializar(){
        tam = $scope.producto.complementos.length;
        for(var indice=0; indice<tam; indice++){
            $scope.complementos_seleccionados.push(null);
        }
    }
    function revisar_complementos(){
        for(id_complemento_seleccionado in $scope.complementos_seleccionados){
            complemento = $scope.complementos_seleccionados[id_complemento_seleccionado];
            if(complemento == null){
                $scope.complementos_correctos = false;
                return
            }
        }
        $scope.complementos_correctos = true;
    }

    inicializar();

    function obtener_seleccionados(){
        seleccionados = [];
        tam = $scope.producto.complementos.length;
        for(var indice=0; indice<tam; indice++){
            complementos = $scope.producto.complementos[indice].complementos;
            encontro = false;
            for(id_complemento in complementos){
                complemento = complementos[id_complemento];
                if(complemento.id == $scope.complementos_seleccionados[indice]){
                    seleccionados.push(complemento);
                    encontro = true;
                    break;
                }
            }
            if(encontro == false){
                seleccionados.push(null);
            }
        }
        return seleccionados;
    }

    $scope.confirmar = function () {
        revisar_complementos();
        if($scope.complementos_correctos == true){
            seleccionados = obtener_seleccionados();
            $uibModalInstance.close([$scope.producto.id, seleccionados]);
        }
    };

    $scope.cancel = function() {
        $uibModalInstance.dismiss('cancel');
    };
})
.controller('CompraController', function($scope, $http, $window, $uibModal) {
    $scope.categoria_seleccionada = null;
    $scope.categorias_productos = null;

    $scope.procesando_pedido = false;

    var productos = {};
    $scope.costos_totales = {subtotal: 0, domicilio: domicilio, total: 3000};

    var posicion_productos_carrito = {};
    $scope.carrito_compra = [];
    $scope.carrito_compra_complementos = [];

    $scope.filtros = {nombre: "", precio_desde: null, precio_hasta: null};

    $scope.ocultar_div_compra_pedido = function(){
        if($scope.costos_totales.subtotal <= 0){
            $("#modal-dialog").modal('hide');
        }
    }

    $scope.realizar_pedido = function(){
        $scope.procesando_pedido = true;
        $http({
            method: 'POST',
            url: '/realizar-compra',
            data: {
                compras: $scope.carrito_compra,
                compras_complementos: $scope.carrito_compra_complementos,
                costos: $scope.costos_totales,
            },
        }).then(function successCallback(response) {
            if (response.status == 200 && response.data[0] == "Ok"){
                $window.location.href = response.data[1];
            }else{
                toastr["error"]("Error con la conexión al servidor, por favor verificar conexión a internet");
                $scope.procesando_pedido = false;
            }
        }, function errorCallback(response) {
            toastr["error"]("Error con la conexión al servidor, por favor verificar conexión a internet");
            $scope.procesando_pedido = false;
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
        productos_del_pedido = JSON.parse($window.localStorage.getItem("productos_del_pedido"))
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
        $scope.ocultar_div_compra_pedido();
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
            }
        }, function errorCallback(response) {
            toastr["error"]("Error con la conexión al servidor, por favor verificar conexión a internet");
        });
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

    $scope.ejecutar_pedir_producto = function(producto){
        if(producto.complementos.length > 0){
            $scope.seleccionar_complementos(producto);
        }else{
            $scope.pedir_producto(producto.id);
        }
    }
});