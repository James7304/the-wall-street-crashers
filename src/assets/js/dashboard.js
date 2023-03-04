
var alphaHistoryChart = "";
function loadAlphaValuation(){


    var http = new XMLHttpRequest();
    var url = '../api/trade_data/alpha_valuation';
    var params = '';
    http.open('POST', url, true);

    //Send the proper header information along with the request
    http.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');

    http.onreadystatechange = function() {//Call a function when the state changes.
        if(http.readyState == 4 && http.status == 200) {

            const res = JSON.parse(http.responseText)
            document.querySelector('#alpha-value').textContent = "£" + (parseInt(res['value'])/100).toFixed(2);
            
            document.querySelector('#alpha-return').textContent = (parseFloat(res['return']) != 0 ? (parseFloat(res['return']) > 0 ? "↑ " : "↓ ") : "") + res['return'] + "%";
            document.querySelector('#alpha-return').classList.add(parseFloat(res['return']) >= 0 ? "text-success" : "text-danger");

            document.querySelector('#alpha-valuation-spinner').classList.add('d-none');
        }
    }
    http.send(params);
}
function loadAlphaTrades(chartTime){

    var http = new XMLHttpRequest();
    var url = '../api/trade_data/alpha_trades';
    var params = 'chartTime=' + chartTime;
    http.open('POST', url, true);

    //Send the proper header information along with the request
    http.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');

    http.onreadystatechange = function() {//Call a function when the state changes.
        if(http.readyState == 4 && http.status == 200) {

            const res = JSON.parse(http.responseText);

            res.forEach(trade => {
                
                document.querySelector('#alpha-trades-spinner').classList.add('d-none');
                // Create the list item element
                const li = document.createElement('li');
                li.classList.add('list-group-item');

                // Create the div element with class "row"
                const divRow = document.createElement('div');
                divRow.classList.add('row');

                // Create the first div element
                const div1 = document.createElement('div');
                div1.classList.add('col-3', 'p-0', 'ps-2');
                const b = document.createElement('b');
                b.textContent = trade.ticker;
                div1.appendChild(b);

                // Create the second div element
                const div2 = document.createElement('div');
                div2.classList.add('col-6', 'p-0');
                div2.style.textAlign = 'center';
                div2.innerHTML = "<i class='" + (trade.type == 'BUY' ? 'text-success' : 'text-danger') + "'>" + trade.type + "</i> @ £" + (parseInt(trade.price)/100).toFixed(2);

                // Create the third div element
                const div3 = document.createElement('div');
                div3.classList.add('col-3', 'p-0', 'pe-2');
                div3.style.textAlign = 'right';
                div3.textContent = trade.hour + ':' + (trade.minute.length == 1 ? "0" + trade.minute : trade.minute);

                // Add the three divs to the row div
                divRow.appendChild(div1);
                divRow.appendChild(div2);
                divRow.appendChild(div3);

                // Add the row div to the list item
                li.appendChild(divRow);

                document.querySelector('#alpha-recent-trades').appendChild(li);

            });
        }
    }
    http.send(params);
}
function loadAlphaHistory(){

    var http = new XMLHttpRequest();
    var url = '../api/trade_data/alpha_history';
    var params = '';
    http.open('POST', url, true);

    //Send the proper header information along with the request
    http.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');

    http.onreadystatechange = function() {//Call a function when the state changes.
        if(http.readyState == 4 && http.status == 200) {

            document.querySelector('#alpha-history-spinner').classList.add('d-none');

            const res = JSON.parse(http.responseText);

            var data = [];

            res.forEach(point => {
                
                data.push(
                    {
                        x: point.time,
                        y: (parseInt(point.valuation)/100000).toFixed(2) - 100
                    }
                );

            });
    
            const ctx = document.getElementById('alphaHistoryChart');
            if(alphaHistoryChart != "") alphaHistoryChart.destroy();

            alphaHistoryChart = new Chart(ctx, {
                type: 'line',
                data: {
                    datasets: [{
                        data: data
                    }],
                },
                options: {
                    plugins: {
                        legend: {
                            display: false
                        },
                    },
                    scales: {
                        y: {
                            ticks: {
                                // Include a dollar sign in the ticks
                                callback: function(value, index, ticks) {
                                    return value + "%";
                                }
                            }
                        }
                    }
                }
            });
        }
    }
    http.send(params);
}

loadAlphaValuation();
loadAlphaTrades();
loadAlphaHistory();
