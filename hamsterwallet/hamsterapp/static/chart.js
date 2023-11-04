// Create the chart
const f = () => {
    Highcharts.chart('container', {
        chart: {
            renderTo: 'container',
            type: 'pie',
            backgroundColor: 'transparent',
        },
        plotOptions: {
            pie: {
                shadow: false
            }
        },
        tooltip: {
            formatter: function () {
                return '<b>' + this.point.name + '</b>: ' + this.y + ' %';
            }
        },
        series: [{
            name: 'Browsers',
            data: [["Firefox", 6], ["MSIE", 4], ["Chrome", 7]],
            size: '100%',
            innerSize: '70%',
            dataLabels: {
                enabled: false
            }
        }],
        credits: {
            enabled: false
        },
        title: {
            text: ""
        }
    });
}

f();