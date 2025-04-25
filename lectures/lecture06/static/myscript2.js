"use strict";

import { createApp, ref, watch } from "https://cdnjs.cloudflare.com/ajax/libs/vue/3.5.13/vue.esm-browser.min.js";

let config = {};
config.setup = function() { 
    let number = parseInt(Math.random()*100);
    let guess = ref(0);
    return { number, guess };
 };
config.methods = {};

config.methods.range = function(start, end) {
    const result = [];
    for (let i = start; i < end; i++) {
      result.push(i);
    }
    return result;
};

let myapp = createApp(config).mount("#myapp");

window.myapp = myapp;

