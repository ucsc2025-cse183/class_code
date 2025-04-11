function game() {
    let number = parseInt(Math.floor(Math.random() * 1000));
    console.log(document.getElementById("submit-button"));
    let button = document.getElementById("submit-button");
    let input = document.getElementById("game-guess");
    let game = document.getElementById("game-output");

    function make_guess() {
        let guess = parseInt(input.value);
        if (guess == number) {
            game.innerHTML = "<div>You won!</div>";
        } else if (guess < number) {
            game.innerHTML = "<div style='color:red'>" + guess + " is too low</div>";
        } else {
            game.innerHTML = "<div style='color:red'>" + guess + " is too high</div>";
        }
    };

    button.onclick = make_guess;
}

game();
