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
                lineColors: JSON.parse(element.dataset.colors),
                resize: true,
                hideHover: 'auto',
                gridTextSize: '14px',
                hoverCallback: function(index, options, content) {
                    var data = options.data[index];
                    content += "<div class='morris-hover-point' style='color: #5c5c5c'>"+"К-сть: "+data.count;+"</div>";
                    return content;
                }
            });

        }

        if ($('#morris_line_1').length) {
            const element = document.getElementById("morris_line_1")
            Morris.Line({
                element: 'morris_line_1',
                behaveLikeLine: true,
                data: JSON.parse(element.dataset.data),
                xkey: 'x',
                ykeys: JSON.parse(element.dataset.ykeys),
                labels: JSON.parse(element.dataset.labels),
                lineColors: JSON.parse(element.dataset.colors),
                trendLineColors: JSON.parse(element.dataset.colors),
                resize: true,
                hideHover: 'auto',
                gridTextSize: '14px',
            });

        }

        if ($('#morris_line_2').length) {
            const element = document.getElementById("morris_line_2")
            Morris.Line({
                element: 'morris_line_2',
                behaveLikeLine: true,
                data: JSON.parse(element.dataset.data),
                xkey: 'x',
                ykeys: JSON.parse(element.dataset.ykeys),
                labels: JSON.parse(element.dataset.labels),
                lineColors: JSON.parse(element.dataset.colors),
                trendLineColors: JSON.parse(element.dataset.colors),
                resize: true,
                hideHover: 'auto',
                gridTextSize: '14px',
            });

        }

        if ($('#morris_line_3').length) {
            const element = document.getElementById("morris_line_3")
            Morris.Line({
                element: 'morris_line_3',
                behaveLikeLine: true,
                data: JSON.parse(element.dataset.data),
                xkey: 'x',
                ykeys: JSON.parse(element.dataset.ykeys),
                labels: JSON.parse(element.dataset.labels),
                lineColors: JSON.parse(element.dataset.colors),
                trendLineColors: JSON.parse(element.dataset.colors),
                resize: true,
                hideHover: 'auto',
                gridTextSize: '14px',
            });

        }

        if ($('#morris_line_4').length) {
            const element = document.getElementById("morris_line_4")
            Morris.Line({
                element: 'morris_line_4',
                behaveLikeLine: true,
                data: JSON.parse(element.dataset.data),
                xkey: 'x',
                ykeys: JSON.parse(element.dataset.ykeys),
                labels: JSON.parse(element.dataset.labels),
                lineColors: JSON.parse(element.dataset.colors),
                trendLineColors: JSON.parse(element.dataset.colors),
                resize: true,
                hideHover: 'auto',
                gridTextSize: '14px',
            });

        }

        if ($('#morris_line_with_count_1').length) {
            const element = document.getElementById("morris_line_with_count_1")
            Morris.Line({
                element: 'morris_line_with_count_1',
                behaveLikeLine: true,
                data: JSON.parse(element.dataset.data),
                xkey: 'x',
                ykeys: JSON.parse(element.dataset.ykeys),
                labels: JSON.parse(element.dataset.labels),
                lineColors: JSON.parse(element.dataset.colors),
                trendLineColors: JSON.parse(element.dataset.colors),
                resize: true,
                hideHover: 'auto',
                gridTextSize: '14px',
                hoverCallback: function(index, options, content) {
                    var data = options.data[index];
                    content += "<div class='morris-hover-point' style='color: #5c5c5c'>"+"К-сть: "+data.count;+"</div>";
                    return content;
                }
            });

        }

        if ($('#morris_line_with_count_2').length) {
            const element = document.getElementById("morris_line_with_count_2")
            Morris.Line({
                element: 'morris_line_with_count_2',
                behaveLikeLine: true,
                data: JSON.parse(element.dataset.data),
                xkey: 'x',
                ykeys: JSON.parse(element.dataset.ykeys),
                labels: JSON.parse(element.dataset.labels),
                lineColors: JSON.parse(element.dataset.colors),
                trendLineColors: JSON.parse(element.dataset.colors),
                resize: true,
                hideHover: 'auto',
                gridTextSize: '14px',
                hoverCallback: function(index, options, content) {
                    var data = options.data[index];
                    content += "<div class='morris-hover-point' style='color: #5c5c5c'>"+"К-сть: "+data.count;+"</div>";
                    return content;
                }
            });

        }

        if ($('#morris_line_with_count_3').length) {
            const element = document.getElementById("morris_line_with_count_3")
            Morris.Line({
                element: 'morris_line_with_count_3',
                behaveLikeLine: true,
                data: JSON.parse(element.dataset.data),
                xkey: 'x',
                ykeys: JSON.parse(element.dataset.ykeys),
                labels: JSON.parse(element.dataset.labels),
                lineColors: JSON.parse(element.dataset.colors),
                trendLineColors: JSON.parse(element.dataset.colors),
                resize: true,
                hideHover: 'auto',
                gridTextSize: '14px',
                hoverCallback: function(index, options, content) {
                    var data = options.data[index];
                    content += "<div class='morris-hover-point' style='color: #5c5c5c'>"+"К-сть: "+data.count;+"</div>";
                    return content;
                }
            });

        }

        if ($('#morris_line_with_count_4').length) {
            const element = document.getElementById("morris_line_with_count_4")
            Morris.Line({
                element: 'morris_line_with_count_4',
                behaveLikeLine: true,
                data: JSON.parse(element.dataset.data),
                xkey: 'x',
                ykeys: JSON.parse(element.dataset.ykeys),
                labels: JSON.parse(element.dataset.labels),
                lineColors: JSON.parse(element.dataset.colors),
                trendLineColors: JSON.parse(element.dataset.colors),
                resize: true,
                hideHover: 'auto',
                gridTextSize: '14px',
                hoverCallback: function(index, options, content) {
                    var data = options.data[index];
                    content += "<div class='morris-hover-point' style='color: #5c5c5c'>"+"К-сть: "+data.count;+"</div>";
                    return content;
                }
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
                lineColors: JSON.parse(element.dataset.colors),
                resize: true,
                hideHover: 'auto',
                gridTextSize: '14px',
                hoverCallback: function(index, options, content) {
                    var data = options.data[index];
                    content += "<div class='morris-hover-point' style='color: #5c5c5c'>"+"К-сть: "+data.count;+"</div>";
                    return content;
                }
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
                hideHover: 'auto',
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
                barColors: JSON.parse(element.dataset.colors),
                resize: true,
                hideHover: 'auto',
                gridTextSize: '14px',
                hoverCallback: function(index, options, content) {
                    var data = options.data[index];
                    content += "<div class='morris-hover-point' style='color: #5c5c5c'>"+"К-сть: "+data.count;+"</div>";
                    return content;
                }
            });
        }

        if ($('#morris_bar_1').length) {
            const element = document.getElementById("morris_bar_1")
            Morris.Bar({
                element: 'morris_bar_1',
                data: JSON.parse(element.dataset.data),
                xkey: 'x',
                ykeys: JSON.parse(element.dataset.ykeys),
                labels: JSON.parse(element.dataset.labels),
                barColors: JSON.parse(element.dataset.colors),
                resize: true,
                hideHover: 'auto',
                gridTextSize: '14px',
            });
        }

        if ($('#morris_bar_2').length) {
            const element = document.getElementById("morris_bar_2")
            Morris.Bar({
                element: 'morris_bar_2',
                data: JSON.parse(element.dataset.data),
                xkey: 'x',
                ykeys: JSON.parse(element.dataset.ykeys),
                labels: JSON.parse(element.dataset.labels),
                barColors: JSON.parse(element.dataset.colors),
                resize: true,
                hideHover: 'auto',
                gridTextSize: '14px',
            });
        }

        if ($('#morris_bar_3').length) {
            const element = document.getElementById("morris_bar_3")
            Morris.Bar({
                element: 'morris_bar_3',
                data: JSON.parse(element.dataset.data),
                xkey: 'x',
                ykeys: JSON.parse(element.dataset.ykeys),
                labels: JSON.parse(element.dataset.labels),
                barColors: JSON.parse(element.dataset.colors),
                resize: true,
                hideHover: 'auto',
                gridTextSize: '14px',
            });
        }

        if ($('#morris_bar_4').length) {
            const element = document.getElementById("morris_bar_4")
            Morris.Bar({
                element: 'morris_bar_4',
                data: JSON.parse(element.dataset.data),
                xkey: 'x',
                ykeys: JSON.parse(element.dataset.ykeys),
                labels: JSON.parse(element.dataset.labels),
                barColors: JSON.parse(element.dataset.colors),
                resize: true,
                hideHover: 'auto',
                gridTextSize: '14px',
            });
        }

        if ($('#morris_bar_with_count_1').length) {
            const element = document.getElementById("morris_bar_with_count_1")
            Morris.Bar({
                element: 'morris_bar_with_count_1',
                data: JSON.parse(element.dataset.data),
                xkey: 'x',
                ykeys: JSON.parse(element.dataset.ykeys),
                labels: JSON.parse(element.dataset.labels),
                barColors: JSON.parse(element.dataset.colors),
                resize: true,
                hideHover: 'auto',
                gridTextSize: '14px',
                hoverCallback: function(index, options, content) {
                    var data = options.data[index];
                    content += "<div class='morris-hover-point' style='color: #5c5c5c'>"+"К-сть: "+data.count;+"</div>";
                    return content;
                }
            });
        }

        if ($('#morris_bar_with_count_2').length) {
            const element = document.getElementById("morris_bar_with_count_2")
            Morris.Bar({
                element: 'morris_bar_with_count_2',
                data: JSON.parse(element.dataset.data),
                xkey: 'x',
                ykeys: JSON.parse(element.dataset.ykeys),
                labels: JSON.parse(element.dataset.labels),
                barColors: JSON.parse(element.dataset.colors),
                resize: true,
                hideHover: 'auto',
                gridTextSize: '14px',
                hoverCallback: function(index, options, content) {
                    var data = options.data[index];
                    content += "<div class='morris-hover-point' style='color: #5c5c5c'>"+"К-сть: "+data.count;+"</div>";
                    return content;
                }
            });
        }

        if ($('#morris_bar_with_count_3').length) {
            const element = document.getElementById("morris_bar_with_count_3")
            Morris.Bar({
                element: 'morris_bar_with_count_3',
                data: JSON.parse(element.dataset.data),
                xkey: 'x',
                ykeys: JSON.parse(element.dataset.ykeys),
                labels: JSON.parse(element.dataset.labels),
                barColors: JSON.parse(element.dataset.colors),
                resize: true,
                hideHover: 'auto',
                gridTextSize: '14px',
                hoverCallback: function(index, options, content) {
                    var data = options.data[index];
                    content += "<div class='morris-hover-point' style='color: #5c5c5c'>"+"К-сть: "+data.count;+"</div>";
                    return content;
                }
            });
        }

        if ($('#morris_bar_with_count_4').length) {
            const element = document.getElementById("morris_bar_with_count_4")
            Morris.Bar({
                element: 'morris_bar_with_count_4',
                data: JSON.parse(element.dataset.data),
                xkey: 'x',
                ykeys: JSON.parse(element.dataset.ykeys),
                labels: JSON.parse(element.dataset.labels),
                barColors: JSON.parse(element.dataset.colors),
                resize: true,
                hideHover: 'auto',
                gridTextSize: '14px',
                hoverCallback: function(index, options, content) {
                    var data = options.data[index];
                    content += "<div class='morris-hover-point' style='color: #5c5c5c'>"+"К-сть: "+data.count;+"</div>";
                    return content;
                }
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
                resize: true,
                hideHover: 'auto'
            });
        }
    });

    const BetProfitGraphLastProfitLineTab = document.getElementById("last-profit-line-tab");
    BetProfitGraphLastProfitLineTab.addEventListener('click', updateTab);

    const BetProfitGraphMonthProfitLineTab = document.getElementById("month-profit-line-tab");
    BetProfitGraphMonthProfitLineTab.addEventListener('click', updateTab);

    const BetProfitGraphYearProfitLineTab = document.getElementById("year-profit-line-tab");
    BetProfitGraphYearProfitLineTab.addEventListener('click', updateTab);

    const BetProfitGraphLastProfitBarTab = document.getElementById("last-profit-bar-tab");
    BetProfitGraphLastProfitBarTab.addEventListener('click', updateTab);

    const BetProfitGraphMonthProfitBarTab = document.getElementById("month-profit-bar-tab");
    BetProfitGraphMonthProfitBarTab.addEventListener('click', updateTab);

    const BetProfitGraphYearProfitBarTab = document.getElementById("year-profit-bar-tab");
    BetProfitGraphYearProfitBarTab.addEventListener('click', updateTab);

    function updateTab(){
        setTimeout(function() { window.dispatchEvent(new Event('resize')); }, 500);
    };


})(window, document, window.jQuery);