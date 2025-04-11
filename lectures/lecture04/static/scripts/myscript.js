
function game(max_number) {
    let number = Math.floor(Math.random() * max_number);

    let output = document.getElementById("game-output");
    function myprint(text) {
        output.innerHTML = output.innerHTML + text;
    }

    while(true) {
        let guess = parseInt(prompt("make a guess"));
        if (guess < 0)
        {
            myprint("you quit the game");
            break;
        }
        if (guess == number)
        {
            myprint("you won!");
            break;
        }
        if (guess < number)
        {
            myprint("your guess " + guess + " is too low");
        }
        else
        {
            myprint("your guess " + guess + " is too high");
        }
    }
}