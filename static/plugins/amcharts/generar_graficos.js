
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