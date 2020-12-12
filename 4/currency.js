document.addEventListener('DOMContentLoaded', function() {

    document.querySelector('form').onsubmit = function(){

        const currency = document.querySelector('#currency').value.toUpperCase();

        fetch('https://api.exchangeratesapi.io/latest?base=USD')
        .then(response => response.json()) // Return respond.json()
        .then(data => {
            if (data.rates[currency]){
                const rate = data.rates[currency].toFixed(3);
                document.querySelector('#result').innerHTML = `1 USD is equal to ${rate} ${currency}`;
                document.querySelector('#currency').value = '';
            } else{
                document.querySelector('#result').innerHTML = `${currency} is not a supported currency`;
            }

        })
        .catch(error =>{
            console.log(error);
        });

        return false;
    };



});
