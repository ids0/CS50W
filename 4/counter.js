let counter = 0;
function count(){
    counter++;
    const heading = document.querySelector('h1');
    heading.innerHTML = counter;
    // alert(`Hey ${heading}`)
    // heading.innerHTML == 2 ? heading.innerHTML = 1 : heading.innerHTML = 2;

}

document.addEventListener('DOMContentLoaded', () => document.querySelector('button').onclick = count);
