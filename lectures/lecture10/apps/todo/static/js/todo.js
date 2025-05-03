"use strict";

import { createApp, ref, watch } from "https://cdnjs.cloudflare.com/ajax/libs/vue/3.5.13/vue.esm-browser.min.js";

let config = {};
config.setup = function() { 
    let new_todo = ref("");
    let todo_items = ref([]);
    return { new_todo, todo_items};
 };
config.methods = {};
config.methods.submit_new_todo = function() {
    // this.todo_items.push(this.new_todo);
    // this.new_todo = "";
    const options = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({description: this.new_todo })
    };
    fetch('/todo/record_todo', options).then(
        config.methods.update_todos            
    )
};
config.methods.update_todos = function() {
    fetch('/todo/list_todos')
    .then(function(response) { return response.json(); })
    .then(function(json) {
        myapp.todo_items = json.rows;
    });    
}

let myapp = createApp(config).mount("#myapp");

window.myapp = myapp;
myapp.update_todos();



