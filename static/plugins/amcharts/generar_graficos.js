
function reporte_datos_diarios(id_div, datos, titulo){
    var chart = AmCharts.makeChart(id_div, {
        "language": "es",
        "type": "serial",
        "theme": "light",
        "marginRight": 80,
        "autoMarginOffset": 20,
        "marginTop": 7,
        "mouseWheelZoomEnabled":true,
        "dataDateFormat": "YYYY-MM-DD",
        "valueAxes": [{
            "axisAlpha": 0.2,
            "position": "left",
            "dashLength": 1,
            "title": titulo
        }],
        "graphs": [{
            "id": "g1",
            "balloonText": "[[value]]",
            "balloon":{
              "drop":true,
            },
            "bullet": "round",
            "bulletBorderAlpha": 1,
            "bulletColor": "#FFFFFF",
            "hideBulletsCount": 50,
            "title": "red line",
            "useLineColorForBulletBorder": true,
            "valueField": "total_venta",
            "connect": false,
        }],
        "chartScrollbar": {
            "autoGridCount": true,
            "graph": "g1",
            "scrollbarHeight": 40
        },
        "chartCursor": {
           "limitToGraph":"g1"
        },
        "categoryField": "dia_venta",
        "categoryAxis": {
            "parseDates": true,
            "axisColor": "#DADADA",
            "dashLength": 1,
            "minorGridEnabled": true,
            "title": "Fecha"
        },
        "export": {
            "enabled": true
        },
        "dataProvider": datos,
    });

    chart.addListener("rendered", zoomChart);

    zoomChart();

    function zoomChart() {
        chart.zoomToIndexes(chart.dataProvider.length - 40, chart.dataProvider.length - 1);
    }
}


function reporte_ventas_productos(id_div, datos, titulo){
    var chart = AmCharts.makeChart(id_div, {
        "language": "es",
        "type": "serial",
        "theme": "light",
        "marginRight": 80,
        "autoMarginOffset": 20,
        "marginTop": 7,
        "mouseWheelZoomEnabled":true,
        "valueAxes": [{
          "axisAlpha": 0,
          "position": "left",
          "title": titulo
        }],
        "startDuration": 1,
        "graphs": [{
          "balloonText": "<b>[[category]]: [[value]]</b>",
          "fillColorsField": "color",
          "fillAlphas": 0.9,
          "lineAlpha": 0.2,
          "type": "column",
          "topRadius":1,
          "valueField": "total"
        }],
        "depth3D": 40,
  "angle": 30,
        "chartCursor": {
          "categoryBalloonEnabled": false,
          "cursorAlpha": 0,
          "zoomable": false
        },
        "categoryField": "nombre",
        "categoryAxis": {
          "gridPosition": "start",
          "labelRotation": 90
        },
        "export": {
          "enabled": true
        },
        "dataProvider": datos,
    });

    chart.addListener("rendered", zoomChart);

    zoomChart();

    function zoomChart() {
        chart.zoomToIndexes(chart.dataProvider.length - 40, chart.dataProvider.length - 1);
    }
}


function reporte_ventas_categorias(id_div, datos, titulo){
    var chart = AmCharts.makeChart( "chartdiv", {
  "type": "pie",
  "theme": "none",
  "dataProvider": datos,
  "valueField": "total",
  "titleField": "producto__categoria__nombre",
   "balloon":{
   "fixedPosition":true
  },
  "export": {
    "enabled": true
  }
} );
}

function reporte_ventas_clientes(id_div, datos, titulo){
    var chart = AmCharts.makeChart(id_div, {
        "language": "es",
        "type": "serial",
        "theme": "light",
        "marginRight": 80,
        "autoMarginOffset": 20,
        "marginTop": 7,
        "mouseWheelZoomEnabled":true,
        "valueAxes": [{
          "axisAlpha": 0,
          "position": "left",
          "title": titulo
        }],
        "startDuration": 1,
        "graphs": [{
          "balloonText": "<b>[[category]]: [[value]]</b>",
          "fillColorsField": "color",
          "fillAlphas": 0.9,
          "lineAlpha": 0.2,
          "type": "column",
          "valueField": "total"
        }],
        "depth3D": 20,
  "angle": 30,
        "chartCursor": {
          "categoryBalloonEnabled": false,
          "cursorAlpha": 0,
          "zoomable": false
        },
        "categoryField": "venta__cliente__first_name",
        "categoryAxis": {
          "gridPosition": "start",
          "labelRotation": 90
        },
        "export": {
          "enabled": true
        },
        "dataProvider": datos,
    });

    chart.addListener("rendered", zoomChart);

    zoomChart();

    function zoomChart() {
        chart.zoomToIndexes(chart.dataProvider.length - 40, chart.dataProvider.length - 1);
        console.log(datos)
    }
}


function reporte_ventas_vendedores(id_div, datos, titulo){
    var chart = AmCharts.makeChart(id_div, {
        "language": "es",
        "type": "serial",
        "theme": "light",
        "marginRight": 80,
        "autoMarginOffset": 20,
        "marginTop": 7,
        "mouseWheelZoomEnabled":true,
        "valueAxes": [{
          "axisAlpha": 0,
          "position": "left",
          "title": titulo
        }],
        "startDuration": 1,
        "graphs": [{
          "balloonText": "<b>[[category]]: [[value]]</b>",
          "fillColorsField": "color",
          "fillAlphas": 0.9,
          "lineAlpha": 0.2,
          "type": "column",
          "valueField": "total"
        }],
        "depth3D": 20,
  "angle": 30,
        "chartCursor": {
          "categoryBalloonEnabled": false,
          "cursorAlpha": 0,
          "zoomable": false
        },
        "categoryField": "venta__trabajador__first_name",
        "categoryAxis": {
          "gridPosition": "start",
          "labelRotation": 90
        },
        "export": {
          "enabled": true
        },
        "dataProvider": datos,
    });

    chart.addListener("rendered", zoomChart);

    zoomChart();

    function zoomChart() {
        chart.zoomToIndexes(chart.dataProvider.length - 40, chart.dataProvider.length - 1);
        console.log(datos)
    }
}
