"use strict";

let game = (function () {

    let t = 0;

    let alive_aliens = [1, 1, 1, 1, 1];
    let game_screen = document.getElementById("game");  
    let bullets = [];  

    function makeAliens() {
        for(let k=0; k<5; k++) {
            game_screen.innerHTML += '<img src="img/alien.png" class="alien" id="alien' + k +'" />';
        }
    }

    function positionAlien(i) {
        return 80 + 120*i + 80 * Math.cos(t / 10 * 6.28);
    }

    function moveEverything() {
        t = t + 0.1;

        for(let k=0; k<5; k++) {
            let alien = document.getElementById("alien" + k);
            let x = positionAlien(k);
            alien.style.top = "20px"
            alien.style.left = x+"px";
            if (alive_aliens[k] != 1) {
                alien.style.opacity = 0.3;
            }
        }
        for(let k=0; k<bullets.length; k++)
        {
            let bullet_obj = bullets[k];
            bullet_obj.y -= t * 3;
            let x = bullet_obj.x;
            let y = bullet_obj.y;
            let bullet = document.getElementById("bullet"+ k);
            if (y > 0) {
                bullet.style.left = x + "px";
                bullet.style.top = y + "px";                
                bullets_to_keep.push(bullet);
            } else {
                bullet.style.display = "none";                
                // delete bullet
            }
            // handle collision
        }        
    }

    function mouseMoved(event) {
        let gun = document.getElementById("gun");
        gun.style.left = (event.offsetX - 10) + "px";
    }

    function fire(event) {
        console.log(event);
        let k = bullets.length;
        game_screen.innerHTML += '<div class="bullet" id="bullet' + k +'"></div>';
        bullets.push({x: event.offsetX, y: 600});
    }

    function start() {
        makeAliens();
        setInterval(moveEverything, 100);

        game_screen.onmousemove = mouseMoved    
        game_screen.onclick = fire
    }

    return {
        start: start,
        bullets: bullets,
        fire: fire,
        positionAlien, positionAlien
    };
})();

game.start();
