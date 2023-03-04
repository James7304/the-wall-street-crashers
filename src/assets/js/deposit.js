function deposit(){
    const amount = document.querySelector('#deposit-amount').value;

    if(amount == ""){
        document.querySelector('#missing-details').classList.remove('d-none');
        return;
    }

    window.location.href = "./pay?amount=" + (amount*100).toFixed(0);
}