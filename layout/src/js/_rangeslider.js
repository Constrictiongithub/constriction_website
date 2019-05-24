require("ion-rangeslider/js/ion.rangeSlider.js");
import '../scss/rangeslider.scss';

$(function () {

    const PRICE_VALUES = [
        0, 5000, 10000, 25000, 50000, 75000,
        100000, 200000, 300000, 400000, 500000, 600000, 800000,
        1000000, 2000000, 3000000, 4000000, 6000000, 8000000,
        10000000, 20000000, 30000000, 40000000, 50000000
    ];
    const PRICE_LABELS = ["0", "5K", "10K", "25K", "50K", "75K",
        "100K", "200K", "300K", "400K", "500K", "600K", "800K",
        "1M", "2M", "3M", "4M", "6M", "8M",
        "10M", "20M", "30M", "40M", "50M"];

    $(".range-slider").ionRangeSlider({
        type: "double",
        grid: true,
        min: PRICE_VALUES[0],
        max: PRICE_VALUES[PRICE_VALUES.length - 1],
        values: PRICE_VALUES,
        prettify: function (n) {
            return PRICE_LABELS[PRICE_VALUES.indexOf(n)];
        }
    });
    const rangeSlider = $(".range-slider").data("ionRangeSlider");
    rangeSlider.update();
});