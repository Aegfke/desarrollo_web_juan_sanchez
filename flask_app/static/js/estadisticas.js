//Primer grafico
Highcharts.chart("first-graph", {
  chart: {
    type: "line",
  },
  title: {
    text: "Número de Actividades por día",
  },
  xAxis: {
    type: "datetime",
    dateTimeLabelFormats: {
      month: "%b %e, %Y",
    },
    title: {
      text: "Fecha",
    },
  },
  yAxis: {
    title: {
      text: "Número de Actividades",
    },
  },
  legend: {
    align: "left",
    verticalAlign: "top",
    borderWidth: 0,
  },

  tooltip: {
    shared: true,
    crosshairs: true,
  },

  series: [
    {
      name: "Actividades",
      data: [],
      lineWidth: 1,
      marker: {
        enabled: true,
        radius: 4,
      },
      color: "#FC2865",
    },
  ],
});

//Segundo grafico
Highcharts.chart("second-graph", {
    chart: {
        type: 'pie'
    },
    title: {
        text: 'Distribución de actividades'
    },
    series: [{
      name:"Temas",
      data:[]
    }]
});

// Tercer grafico
Highcharts.chart("third-graph", {
    chart: {
        type: 'column'
    },
    title: {
        text: 'Actividades por mes'
    },
    xAxis: {
        type: 'datetime',
        labels: {
            format: '{value:%B %Y}'
        },
        tickInterval: 30 * 24 * 3600 * 1000,
        dateTimeLabelFormats: {
            month: '%B %Y'
        },
        title: {
            text: 'Meses'
        }
    },
    yAxis: {
        min: 0,
        title: {
            text: 'Cantidad de actividades'
        }
    },
    series: [
      { name: 'Mañana', data: [] },
      { name: 'Tarde', data: [] },
      { name: 'Noche', data: [] }
    ]
});


fetch("http://127.0.0.1:5000/get-stats-data")
  .then((response) => response.json())
  .then((data) => {

    const graph1 = data.graph1;
    let parsedData1 = graph1.map((item) => {
        const [year, month, day] = item.fecha
            .split("-")
            .map((part) => parseInt(part, 10));
        return [
            Date.UTC(year, month - 1, day),
            item.cantidad,
        ];
    });
    parsedData1.sort((a, b) => a[0] - b[0]);

    const graph2 = data.graph2;
    let parsedData2 = graph2.map((item) => {
        return [
            item.tema,
            item.cantidad
        ];
    });

    let mañana = [];
    let tarde = [];
    let noche = [];

    const graph3 = data.graph3;
    let parsedData3 = graph3.map((item) => {
      const [month, year] = item.mes_año
            .split("-")
            .map((part) => parseInt(part, 10));
      
      const tiempo = Date.UTC(year, month - 1);

      mañana.push([tiempo, item.cantidad.mañana]);
      tarde.push([tiempo, item.cantidad.tarde]);
      noche.push([tiempo, item.cantidad.noche]);
    });


    const chart = Highcharts.charts.find(
        (chart) => chart && chart.renderTo.id == "first-graph"
    );
    const chart2 = Highcharts.charts.find(
        (chart) => chart && chart.renderTo.id == "second-graph"
    );
    const chart3 = Highcharts.charts.find(
      (chart) => chart && chart.renderTo.id == "third-graph"
    )
    
    chart.update({
      series: [
        {
          data: parsedData1,
        },
      ],
    });
    chart2.update({
      series: [
        {
          data: parsedData2,
        },
      ],
    });
    chart3.update({
      series: [
        { name: 'Mañana', data: mañana },
        { name: 'Tarde', data: tarde },
        { name: 'Noche', data: noche }
      ]
    });

  })

  .catch((error) => console.error("Error:", error));