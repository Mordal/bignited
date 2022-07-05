var readline = require('readline');
var rl = readline.createInterface(process.stdin, process.stdout);

function harmonic(number){
    result = 0;
    for(i=1; i <= Math.round(number); i++){
        result += (1/i);
    }
    return result.toFixed(4);
};

function askInput(){
    rl.question('Geef een getal: ', getal=>{
        //result = harmonic(getal);
        //return new Promise((result)) 
        console.log(harmonic(getal))
        return  harmonic(getal)    
    });
};

askInput()