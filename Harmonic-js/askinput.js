export default
    function askInput(){
        var readline = require('readline');
        var rl = readline.createInterface(process.stdin, process.stdout);  
            rl.question('Geef een getal: ', getal=>{
                //result = harmonic(getal);
                //return new Promise((result)) 
                return  harmonic(getal)    
            });
        };