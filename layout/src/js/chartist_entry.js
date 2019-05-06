import "../scss/chartist.scss";
import { format } from 'date-fns';
let Chartist = require("chartist/dist/chartist.js");
require('chartist-plugin-legend');

let charts = [];
$('.line-chart').each(function () {
    let data = { "series": [] };
    let legend = $(this).siblings(".legend")[0];
    $.getJSON($(this).data("url"), function (json_series) {
        json_series.forEach(function (json_serie){
            let entries = [];
            json_serie["entries"].forEach(function (json_entry) {
                entries.push({ x: new Date(json_entry.date), y: json_entry.value });
            });
            let serie = { "data": entries, "name": json_serie["title"], };
            data["series"].push(serie);
        });
    });
    let options = {
        axisX: {
            type: Chartist.FixedScaleAxis,
            divisor: 6,
            labelInterpolationFnc: function (value) {
                return format(value, 'YYYY [Q]Q');
            },
        },
        axisY: {
            labelInterpolationFnc: function (value) {
                if (value >= 1000000)
                    return value/1000000 + "M";
                if (value >= 1000)
                    return value / 1000 + "K";
            },
        },
        plugins: [Chartist.plugins.legend({position: legend, })],
    };
    charts.push({ type: Chartist.Line, elem: this, data: data, options: options})
});

charts.forEach(function (chart) {
    setTimeout(function () {
        new chart.type(chart.elem, chart.data, chart.options)
    }, 1000);
});