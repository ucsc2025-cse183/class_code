"use script";

import { createApp, ref, watch } from "https://cdnjs.cloudflare.com/ajax/libs/vue/3.5.13/vue.esm-browser.min.js";

// convenience class to store setups and methods
let config = {};

// function that retruns the object with vue variables
config.setup = function() {
  let t = ref(0.0);
  let aliens = ref([]);
  for(let k=0; k<5; k++) {
    aliens.value.push({alive:true, x:10 + 110*k, y:20}); 
  }
  let bullets = ref([]);
  let gun = ref({x: 0});
  // return reactive vars
  return { t, aliens, bullets, gun };
};

// convenience container for methods
config.methods = {};

// a method that can move everything
config.methods.moveEverything = function() {
  this.t += 0.1;
  for(let k=0; k<this.aliens.length; k++)
  {
    this.aliens[k].x = 80 + 120*k + 80 * Math.cos(this.t / 10 * 6.28);
  }
  for(let k=0; k<this.bullets.length; k++)
  {
    this.bullets[k].y -= 3 * this.t;
  }
  // TODO: check collisions
  // TODO: delete bullets when out of window
};

// method to fire aka create a new bullet
config.methods.fire = function() {
  this.bullets.push({x:this.gun.x,y:550});
};

// method called when we move mouse
config.methods.move = function(event) {
  this.gun.x = event.clientX;
};

// create the app and control the div#game
window.game = createApp(config).mount("#game");

// periodically moveEverything
setInterval(window.game.moveEverything, 100);
