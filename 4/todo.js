const todo_list = [];

function update_task(task) {

    // for (let i = 0 ; i<todo_list.length ; i++) {
    //     let list_element = document.createElement("LI");
    //     let task_element = document.createTextNode(todo_list[i]);
    //     list_element.appendChild(task_element);
    //     document.querySelector('#task').appendChild(list_element);
    // }
    // return false;
    let li = document.createElement("li");
    li.innerHTML = task;

    document.querySelector('#task').appendChild(li);
}


document.addEventListener('DOMContentLoaded', function(){

    document.querySelector('form').onsubmit = function () {
        const new_task = document.querySelector('#todo').value;
        if (new_task){
            todo_list.push(new_task);
            update_task(new_task);
        }

        document.querySelector('#todo').value = '';
        // Stop form from submitting
        return false;
    };
});


// document.addEventListener('DOMContentLoaded', () => document.querySelector('button').onclick = count);
