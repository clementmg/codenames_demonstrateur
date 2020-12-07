var colorList = ["Crimson", "DeepSkyBlue", "Linen", "DimGrey"]
var startColor;
var gameRevealed = false;
var gameEnded = false;
var size = 25;
var currentColor;

function newGame(){
    gameRevealed = false;
    gameEnded = false;
    words = getRandomWords(); //return the 25 words that will be used
    distribution = getDistribution(words); //indicating blue words, red words, assassin, neutral words
    currentColor = startColor;

    // starting annoucement
    var annonce = document.getElementById("titleH");
    if (startColor == 0){
        annonce.innerHTML = "Les rouges commencent";
        annonce.style.color = colorList[0];
    } else{
        annonce.innerHTML = "Les bleus commencent";
        annonce.style.color = colorList[1];
    }
    
    //display footer
    var hiddenContent = document.getElementsByClassName("hidden");
    for (var i = 0; i < hiddenContent.length; i++){
        hiddenContent[i].style.display = "block";
    }
    // hiddenContent.style.display = "block";
    
    createGrid();
}

//get random words in wordlist
function getRandomWords(){
    list = [];
    wordsClone = wordList.slice(0);

    for (i=0; i<25; i++){
        let rdn = Math.floor(Math.random() * Math.floor(wordsClone.length -1));
        list.push(wordsClone[rdn]);
        wordsClone.splice(rdn, 1);
    }
    return list;
}

//indicating blue words, red words, assassin, neutral words
function getDistribution(words){
    wordL = words.slice(0);
    //also return start color
    // 0 : red / 1 : blue / 2 : neutral / 3 : assassin
    //dict : word[color][revealed]
    let rdn1 = Math.floor(Math.random() * Math.floor(2));
    startColor = rdn1;
    let secondColor;
    if (startColor == 0) secondColor = 1;
    else if (startColor == 1) secondColor = 0;

    var dict = {};
    for (i = 0; i < 9; i++){
        let rdn = Math.floor(Math.random() * Math.floor(wordL.length-1));
        dict[wordL[rdn]] = [startColor, false];
        wordL.splice(rdn, 1);
    }
    for (i = 0; i < 8; i++){
        let rdn = Math.floor(Math.random() * Math.floor(wordL.length-1));
        dict[wordL[rdn]] = [secondColor, false];
        wordL.splice(rdn, 1);
    }

    let rdn = Math.floor(Math.random() * Math.floor(wordL.length-1));
    dict[wordL[rdn]] = [3, false];
    wordL.splice(rdn, 1);

    wordL.forEach(word => dict[word] = [2, false]);

    return dict;
}

function createGrid(){
    
    var table = document.getElementById('gridTable');
    table.innerHTML = ""; // reseting grid

    for (let i = 0; i < size; i++){

        let word = words[i];
        let color = distribution[word][0];
        if(i % 5 == 0){
            tr = table.insertRow();
        }
        var td = tr.insertCell();
        
        td.innerHTML = "<span class='btn'>" + word + "</span>";

        if (distribution[word][1] == true){
            td.style.background = colorList[color];
        }
        else td.style.backgroundColor = "white";

        //click function
        td.onclick = (function(){
            return function(){
                if(distribution[word][1] == true) return; // si la carte est déjà révélée

                if (gameEnded == true){
                    alert("Cette partie est terminée."); return;
                }
                this.style.backgroundColor = colorList[color];
                distribution[word][1] = true;

                if(color != currentColor && (color != 3)){
                    // currentColor = color;
                    swapAnnonce(color);
                }

                gameRules();
            }
        })();   
    }
}

function swapAnnonce(color){
    if (currentColor == 0) currentColor = 1;
    else if (currentColor == 1) currentColor = 0;
    
    var annonce = document.getElementById("titleH");
    if(currentColor == 0){
        annonce.innerHTML = "Tour des rouges";
        annonce.style.color = colorList[0];
    } else if (currentColor == 1){
        annonce.innerHTML = "Tour des bleus";
        annonce.style.color = colorList[1];
    }
}

function gameRules(){ 
    //check if assassin is discovered, if red or blue has won etc
    let blueCount = 0;
    let redCount = 0;
    var annonce = document.getElementById("titleH");

    for (let j = 0; j < size; j++){
        let word = words[j];
        if (distribution[word][1] == true){
            if(distribution[word][0] == 3){
                alert("L'assassin a été trouvé ! La partie est terminée."); gameEnded = true;
                annonce.innerHTML = "L'assassin a gagné."
            }
            else if (distribution[word][0] == 0){
                redCount += 1;
            } else if (distribution[word][0] == 1){
                blueCount += 1;            }
        }
    }

    if((startColor == 0 && redCount >= 9) || (startColor == 1 && redCount >= 8)){
        alert("Les rouges gagnent !"); gameEnded = true;
        annonce.innerHTML = "Les rouges ont gagné";
        annonce.style.color = colorList[0];
    }else if((startColor == 0 && blueCount >= 8) || (startColor == 1 && blueCount >= 9)){
        alert("Les bleus gagnent !"); gameEnded = true;
        annonce.innerHTML = "Les bleus ont gagné";
        annonce.style.color = colorList[1];
    }
}

// spymaster view / player view
function reveal_hide_Color(){
    if (gameRevealed) {
        gameRevealed = false;
        createGrid();
        return;
    }

    var table = document.getElementById('gridTable');
    table.innerHTML = ""; // reseting

    for (let i = 0; i < size; i++){

        let word = words[i];
        let color = distribution[word][0];
        if(i % 5 == 0){
            tr = table.insertRow();
        }
        var td = tr.insertCell();
        
        td.innerHTML = "<span class='btn'>" + word + "</span>";
        td.style.backgroundColor = colorList[color];
        //click function
        td.onclick = (function(){
            return function(){
                alert("Impossible d'interagir en espion")
            }
        })();
    }
    gameRevealed = true;
}

//
function pass(){
    swapAnnonce(currentColor);
}

//----------------------------------------------------

function callAI(color){
    var AIdiv = document.getElementById("AIHintArea");
    var newP = document.createElement("p");

    //TODO : send distribution to AI
    // send info
    // if (gameEnded){
    //     alert("La partie est terminée"); return;
    // }
    // fetch('/hello', {
    //     headers: {
    //       'Content-Type': 'application/json'
    //     },
    //     method: 'POST',
    //     body: JSON.stringify({
    //         distribution, color
    //     })
    // }).then(function (response) {
    //     return response.text();

    // // result
    // }).then(function (result) {
    //     console.log('POST response: ');

    //     newP.innerHTML = result;
    //     AIdiv.appendChild(newP);
    //     // alert(result);
    // });
    
    newP.innerHTML = "test"
    AIdiv.insertBefore(newP, AIdiv.childNodes[0]);
}
