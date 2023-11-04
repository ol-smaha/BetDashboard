(function(window, document, $, undefined) {
    "use strict";
    $(function() {

        if ($('#morris_area').length) {
            const element = document.getElementById("morris_area")
            Morris.Area({
                element: 'morris_area',
                behaveLikeLine: true,
                data: JSON.parse(element.dataset.data),
                xkey: 'x',
                ykeys: JSON.parse(element.dataset.ykeys),
                labels: JSON.parse(element.dataset.labels),
                lineColors: ['#5969ff', '#ff407b'],
                resize: true,
                gridTextSize: '14px'
            });

        }

        if ($('#morris_area_1').length) {
            const element = document.getElementById("morris_area_1")
            Morris.Area({
                element: 'morris_area_1',
                behaveLikeLine: true,
                data: JSON.parse(element.dataset.data),
                xkey: 'x',
                ykeys: JSON.parse(element.dataset.ykeys),
                labels: JSON.parse(element.dataset.labels),
                lineColors: ['#5969ff', '#ff407b'],
                resize: true,
                gridTextSize: '14px'
            });

        }

        if ($('#morris_area_2').length) {
            const element = document.getElementById("morris_area_2")
            Morris.Area({
                element: 'morris_area_2',
                behaveLikeLine: true,
                data: JSON.parse(element.dataset.data),
                xkey: 'x',
                ykeys: JSON.parse(element.dataset.ykeys),
                labels: JSON.parse(element.dataset.labels),
                lineColors: ['#5969ff', '#ff407b'],
                resize: true,
                gridTextSize: '14px'
            });

        }

        if ($('#morris_area_3').length) {
            const element = document.getElementById("morris_area_3")
            Morris.Area({
                element: 'morris_area_3',
                behaveLikeLine: true,
                data: JSON.parse(element.dataset.data),
                xkey: 'x',
                ykeys: JSON.parse(element.dataset.ykeys),
                labels: JSON.parse(element.dataset.labels),
                lineColors: ['#5969ff', '#ff407b'],
                resize: true,
                gridTextSize: '14px'
            });

        }

        if ($('#morris_area_4').length) {
            const element = document.getElementById("morris_area_4")
            Morris.Area({
                element: 'morris_area_4',
                behaveLikeLine: true,
                data: JSON.parse(element.dataset.data),
                xkey: 'x',
                ykeys: JSON.parse(element.dataset.ykeys),
                labels: JSON.parse(element.dataset.labels),
                lineColors: ['#5969ff', '#ff407b'],
                resize: true,
                gridTextSize: '14px'
            });

        }

        if ($('#morris_line').length) {
            const element = document.getElementById("morris_line")
            Morris.Line({
                element: 'morris_line',
                behaveLikeLine: true,
                data: JSON.parse(element.dataset.data),
                xkey: 'x',
                ykeys: JSON.parse(element.dataset.ykeys),
                labels: JSON.parse(element.dataset.labels),
                   lineColors: ['#5969ff', '#ff407b'],
                     resize: true,
                        gridTextSize: '14px'
            });

        }

        if ($('#morris_bar').length) {
            Morris.Bar({
                element: 'morris_bar',
                data: [
                    { x: '2011 Q1', y: 0 },
                    { x: '2011 Q2', y: 1 },
                    { x: '2011 Q3', y: 2 },
                    { x: '2011 Q4', y: 3 },
                    { x: '2012 Q1', y: 4 },
                    { x: '2012 Q2', y: 5 },
                    { x: '2012 Q3', y: 6 },
                    { x: '2012 Q4', y: 7 },
                    { x: '2013 Q1', y: 8 }
                ],
                xkey: 'x',
                ykeys: ['y'],
                labels: ['Y'],
                   barColors: ['#5969ff'],
                     resize: true,
                        gridTextSize: '14px'

            });
        }


        if ($('#morris_stacked').length) {
            const element = document.getElementById("morris_stacked")
            Morris.Bar({
                element: 'morris_stacked',
                data: JSON.parse(element.dataset.data),
                xkey: 'x',
                ykeys: JSON.parse(element.dataset.ykeys),
                labels: JSON.parse(element.dataset.labels),
                stacked: true,
                   barColors: ['#5969ff', '#ff407b', '#25d5f2'],
                     resize: true,
                        gridTextSize: '14px'
            });
        }

        if ($('#morris_stacked_1').length) {
            const element = document.getElementById("morris_stacked_1")
            Morris.Bar({
                element: 'morris_stacked_1',
                data: JSON.parse(element.dataset.data),
                xkey: 'x',
                ykeys: JSON.parse(element.dataset.ykeys),
                labels: JSON.parse(element.dataset.labels),
                stacked: true,
                   barColors: ['#5969ff', '#ff407b', '#25d5f2'],
                     resize: true,
                        gridTextSize: '14px'
            });
        }

        if ($('#morris_stacked_2').length) {
            const element = document.getElementById("morris_stacked_2")
            Morris.Bar({
                element: 'morris_stacked_2',
                data: JSON.parse(element.dataset.data),
                xkey: 'x',
                ykeys: JSON.parse(element.dataset.ykeys),
                labels: JSON.parse(element.dataset.labels),
                stacked: true,
                   barColors: ['#5969ff', '#ff407b', '#25d5f2'],
                     resize: true,
                        gridTextSize: '14px'
            });
        }

        if ($('#morris_stacked_3').length) {
            const element = document.getElementById("morris_stacked_3")
            Morris.Bar({
                element: 'morris_stacked_3',
                data: JSON.parse(element.dataset.data),
                xkey: 'x',
                ykeys: JSON.parse(element.dataset.ykeys),
                labels: JSON.parse(element.dataset.labels),
                stacked: true,
                   barColors: ['#5969ff', '#ff407b', '#25d5f2'],
                     resize: true,
                        gridTextSize: '14px'
            });
        }

        if ($('#morris_stacked_4').length) {
            const element = document.getElementById("morris_stacked_4")
            Morris.Bar({
                element: 'morris_stacked_4',
                data: JSON.parse(element.dataset.data),
                xkey: 'x',
                ykeys: JSON.parse(element.dataset.ykeys),
                labels: JSON.parse(element.dataset.labels),
                stacked: true,
                   barColors: ['#5969ff', '#ff407b', '#25d5f2'],
                     resize: true,
                        gridTextSize: '14px'
            });
        }

        if ($('#morris_udateing').length) {
            var nReloads = 0;

            function data(offset) {
                var ret = [];
                for (var x = 0; x <= 360; x += 10) {
                    var v = (offset + x) % 360;
                    ret.push({
                        x: x,
                        y: Math.sin(Math.PI * v / 180).toFixed(4),
                        z: Math.cos(Math.PI * v / 180).toFixed(4)
                    });
                }
                return ret;
            }
            var graph = Morris.Line({
                element: 'morris_udateing',
                data: data(0),
                xkey: 'x',
                ykeys: ['y', 'z'],
                labels: ['sin()', 'cos()'],
                parseTime: false,
                ymin: -1.0,
                ymax: 1.0,
                hideHover: true,
                lineColors: ['#5969ff', '#ff407b'],
                  resize: true
            });

            function update() {
                nReloads++;
                graph.setData(data(5 * nReloads));
                $('#reloadStatus').text(nReloads + ' reloads');
            }
            setInterval(update, 100);
        }


        if ($('#morris_donut').length) {
            const element = document.getElementById("morris_donut")

            Morris.Donut({
                element: 'morris_donut',
                data: JSON.parse(element.dataset.data),
                labelColor: "#1e8728",
                   gridTextSize: '14px',
                colors: [
                     "#5969ff",
                     "#ff407b",
                     "#25d5f2",
                     "#ffc750",
                ],
                resize: true
            });
        }
    });

    const BetProfitGraphNowProfitAreaTab = document.getElementById("now-profit-area-tab");
    BetProfitGraphNowProfitAreaTab.addEventListener('click', updateTab);

    const BetProfitGraphLastProfitAreaTab = document.getElementById("last-profit-area-tab");
    BetProfitGraphLastProfitAreaTab.addEventListener('click', updateTab);

    const BetProfitGraphMonthProfitAreaTab = document.getElementById("month-profit-area-tab");
    BetProfitGraphMonthProfitAreaTab.addEventListener('click', updateTab);

    const BetProfitGraphYearProfitAreaTab = document.getElementById("year-profit-area-tab");
    BetProfitGraphYearProfitAreaTab.addEventListener('click', updateTab);

    const BetProfitGraphNowProfitStackedTab = document.getElementById("now-profit-stacked-tab");
    BetProfitGraphNowProfitStackedTab.addEventListener('click', updateTab);

    const BetProfitGraphLastProfitStackedTab = document.getElementById("last-profit-stacked-tab");
    BetProfitGraphLastProfitStackedTab.addEventListener('click', updateTab);

    const BetProfitGraphMonthProfitStackedTab = document.getElementById("month-profit-stacked-tab");
    BetProfitGraphMonthProfitStackedTab.addEventListener('click', updateTab);

    const BetProfitGraphYearProfitStackedTab = document.getElementById("year-profit-stacked-tab");
    BetProfitGraphYearProfitStackedTab.addEventListener('click', updateTab);

    function updateTab(){
        setTimeout(function() { window.dispatchEvent(new Event('resize')); }, 500);
    };


})(window, document, window.jQuery);