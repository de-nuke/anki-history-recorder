window.myBar = null;
// let color = Chart.helpers.color;
let cursorX;
let cursorY;
let hideTooltipRadius = null;
let hideTooltipX = null;
let hideTooltipY = null;
let maxValue = 0;
let radiusOffset = 0;
let ratio = 1;
let offsetPercentage = 0.25
const primaryColor = "#457b9d";
const secondaryColor = "#a8dadc";
const textColor = "#1d3557";
const backgroundColor = "#F1FAEE";
const contrastColor = "#E63946";
let loaderVisible = true;

function hideLoader() {
    if (loaderVisible) {
        document.querySelector(".loader-container").classList.add('hidden');
        loaderVisible = false;
    }
}


/**
 * Word Cloud
 * @param data
 */
function createWordCloud(data) {
    // create a tag cloud chart
    let chart = anychart.tagCloud(data);

    chart.angles([0])
    chart.colorScale(anychart.scales.linearColor(secondaryColor, primaryColor));

    // display chart
    chart.container("word-cloud");
    chart.draw();
}


/**
 * Answers Clock
 * @param data
 */

Chart.defaults.global.tooltips.custom = function(tooltip) {
    // Tooltip Element
    var tooltipEl = document.getElementById('chartjs-tooltip');

    // Hide if no tooltip
    if (tooltip.opacity === 0) {
        tooltipEl.style.opacity = 0;
        return;
    }

    // Set caret Position
    tooltipEl.classList.remove('above', 'below', 'no-transform');
    if (tooltip.yAlign) {
        tooltipEl.classList.add(tooltip.yAlign);
    } else {
        tooltipEl.classList.add('no-transform');
    }

    function getBody(bodyItem) {
        return bodyItem.lines;
    }

    // Set Text
    if (tooltip.body) {
        var titleLines = tooltip.title || [];
        var bodyLines = tooltip.body.map(getBody);

        var innerHtml = '<thead>';

        titleLines.forEach(function(title) {
            innerHtml += '<tr><th>' + title + '</th></tr>';
        });
        innerHtml += '</thead><tbody>';

        let prevBody = null;
        bodyLines.forEach(function(body, i) {
            var style = 'background:' + primaryColor;
            style += '; border-color:' + secondaryColor;
            style += '; border-width: 2px';
            var span = '<span class="chartjs-tooltip-key" style="' + style + '"></span>';
            if (body[0] !== prevBody) {
                innerHtml += '<tr><td>' + span + body + '</td></tr>';
                prevBody = body[0];
            }
        });
        innerHtml += '</tbody>';

        var tableRoot = tooltipEl.querySelector('table');
        tableRoot.innerHTML = innerHtml;
    }

    var positionY = this._chart.canvas.offsetTop;
    var positionX = this._chart.canvas.offsetLeft;

    // Display, position, and set styles for font
    let a = Math.abs(cursorX-hideTooltipX);
    let b = Math.abs(cursorY-hideTooltipY);
    let c = Math.sqrt(a*a + b*b);
    if (c > hideTooltipRadius){
        tooltipEl.style.opacity = "1";
        tooltipEl.style.left = positionX + tooltip.caretX + 'px';
        tooltipEl.style.top = positionY + tooltip.caretY + 'px';
        tooltipEl.style.fontFamily = tooltip._bodyFontFamily;
        tooltipEl.style.fontSize = tooltip.bodyFontSize;
        tooltipEl.style.fontStyle = tooltip._bodyFontStyle;
        tooltipEl.style.padding = tooltip.yPadding + 'px ' + tooltip.xPadding + 'px';
    } else {
        tooltipEl.style.opacity = "0";
    }
};


function getMousePos(canvas, evt) {
    let rect = canvas.getBoundingClientRect();
    return {
        x: evt.clientX - rect.left,
        y: evt.clientY - rect.top
    };
}

function createChart(data) {
    let canvas = document.getElementById('canvas-clock');
    let ctx = canvas.getContext('2d');

    canvas.addEventListener('mousemove', function(evt) {
        let mousePos = getMousePos(canvas, evt);
        cursorX = mousePos.x;
        cursorY = mousePos.y;
    }, false);

    window.myBar = new Chart(ctx, {
        type: 'polarArea',
        data: data,

        options: {
            aspectRatio: 1,
            legend: false,
            tooltips: {
                enabled: false,
                callbacks: {
                    label: function (item) {
                        let val = (data.datasets[0].data[item.index] - radiusOffset) / ratio;
                        return Math.round(val).toString() + " cards";
                    }
                }
            },
            layout: {
                padding: {
                    left: 20,
                    right: 20,
                    top: 20,
                    bottom: 20
                }
            },
            scale: {
                gridLines: false,
                ticks: {
                    display: false
                }
            },
            hover: {
                animationDuration: 0,
            },
            animation: {
                onComplete: function(animation){
                    let chart = animation.chart;
                    let meta = chart.controller.getDatasetMeta(0);
                    ctx.textAlign = "center";
                    ctx.fillStyle = textColor;
                    ctx.lineWidth = 1;
                    ctx.font = "14px sans-serif";
                    meta.data.forEach(function (bar, index) {
                        let angle = bar._model.startAngle;
                        let text = bar._model.label;
                        let height = 14;
                        let xpoint = bar._model.x + (Math.cos(angle) * (parseFloat(bar._chart.outerRadius) + 10));
                        let ypoint = bar._model.y + (Math.sin(angle) * (parseFloat(bar._chart.outerRadius) + 10)) + height / 2;
                        ctx.fillText(text, xpoint, ypoint);
                    });
                    let x = meta.data[0]._model.x;
                    let y = meta.data[0]._model.y;
                    let radius = meta.data[0]._chart.outerRadius * offsetPercentage;
                    ctx.beginPath();
                    ctx.arc(x, y, radius, 0, 2 * Math.PI);
                    ctx.fillStyle = backgroundColor;
                    ctx.strokeStyle = backgroundColor;
                    ctx.fill();
                    ctx.stroke();
                    ctx.closePath();

                    ctx.beginPath();
                    ctx.arc(x, y, radius/2, 0, 2 * Math.PI);
                    ctx.strokeStyle = primaryColor;
                    ctx.lineWidth = 4;
                    ctx.stroke();
                    ctx.closePath();

                    ctx.beginPath();
                    ctx.moveTo(x, y);
                    ctx.lineTo(x, y - radius/3);
                    ctx.moveTo(x, y);
                    ctx.lineTo(x + radius*0.2, y + radius*0.2);
                    ctx.closePath();
                    ctx.stroke();

                    hideTooltipRadius = radius;
                    hideTooltipX = x;
                    hideTooltipY = y;

                    hideLoader();
                }
            }
        },
    });
}


function makeChartData(data) {
    return {
        labels: data.labels,
        datasets: [{
            label: data.label,
            backgroundColor: primaryColor,
            borderColor: "white",
            borderWidth: 1,
            data: data.data.map(i => i*ratio + radiusOffset)
        },
        {
            backgroundColor: secondaryColor,
            data: Array(data.data.length).fill(maxValue).map(i => i)
        }]
    }
}

function createAnswersClock(data) {
    maxValue = Math.max(...data.data);
    radiusOffset = Math.round(offsetPercentage * maxValue);
    ratio = (maxValue - radiusOffset)/maxValue;

    if (window.myBar) {
        window.myBar.data = makeChartData(data);
        window.myBar.update()
    } else {
        createChart(makeChartData(data));
    }
}


