
function loadValuation(){


    var http = new XMLHttpRequest();
    var url = '../api/trade_data/valuation';
    var params = '';
    http.open('POST', url, true);

    //Send the proper header information along with the request
    http.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');

    http.onreadystatechange = function() {//Call a function when the state changes.
        if(http.readyState == 4 && http.status == 200) {

            const res = JSON.parse(http.responseText)
            document.querySelector('#value').textContent = "£" + (parseInt(res['value'])/100).toFixed(2);
            
            document.querySelector('#return').textContent = (res['return'] != 0 ? (res['return'] > 0 ? "↑ " : "↓ ") : "") + res['return'] + "%";
            document.querySelector('#return').classList.add(res['return'] >= 0 ? "text-success" : "text-danger");

            document.querySelector('#valuation-spinner').classList.add('d-none');
        }
    }
    http.send(params);
}
function loadTrades(){

    var http = new XMLHttpRequest();
    var url = '../api/trade_data/trades';
    var params = '';
    http.open('POST', url, true);

    //Send the proper header information along with the request
    http.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');

    http.onreadystatechange = function() {//Call a function when the state changes.
        if(http.readyState == 4 && http.status == 200) {

            const res = JSON.parse(http.responseText);

            res.forEach(trade => {
                
                document.querySelector('#trades-spinner').classList.add('d-none');
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
                div3.textContent = trade.hour + ':' + trade.minute;

                // Add the three divs to the row div
                divRow.appendChild(div1);
                divRow.appendChild(div2);
                divRow.appendChild(div3);

                // Add the row div to the list item
                li.appendChild(divRow);

                document.querySelector('#recent-trades').appendChild(li);

            });
        }
    }
    http.send(params);
}

loadValuation();
loadTrades();