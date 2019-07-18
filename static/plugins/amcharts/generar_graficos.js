
function nivel_madurez_componentes(id_div, datos, titulo){
    
       var chart = AmCharts.makeChart(id_div, {
        "language": "es",
        "type": "radar",
        "theme": "light",
        "mouseWheelZoomEnabled":true,
        "dataProvider": datos,
        "title": titulo,
        "graphs": [{

          "bullet": "round",
          "bulletSizeField": "bullet1",
          "lineThickness": 2,
          "valueField": "nivel_madurez",
          "type": "line",
          "alphaField": "alpha1",
          "dashLengthField": "dash1"
        }],

        "valueAxes": [{
          "minimum": 0,
          "maximum": 5
        }],
        "categoryField": "nombre"
      });   


}