
function login(event){

    event.preventDefault();
    
    var http = new XMLHttpRequest();
    var url = './api/auth/login/';
    var params = 'email=' + document.querySelector('#email') + '&password=' + document.querySelector('#password');
    http.open('POST', url, true);

    //Send the proper header information along with the request
    http.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');

    http.onreadystatechange = function() {//Call a function when the state changes.
        if(http.readyState == 4 && http.status == 200) {
            alert(http.responseText);
        }
    }
    http.send(params);

    return false;
}
