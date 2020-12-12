

if ( ! localStorage.getItem('counter') ) {
    localStorage.setItem('counter',0);
}
let counter = localStorage.getItem('counter');



function count(){
    counter++;
    const heading = document.querySelector('h1');
    heading.innerHTML = counter;
    localStorage.setItem('counter',counter);
    // alert(`Hey ${heading}`)
    // heading.innerHTML == 2 ? heading.innerHTML = 1 : heading.innerHTML = 2;

}

document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('h1').innerHTML = counter;
    document.querySelector('button').onclick = count;
    // setInterval(count,1000);

    });
