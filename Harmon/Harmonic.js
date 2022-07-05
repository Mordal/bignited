var readline = require('readline');
var rl = readline.createInterface(process.stdin, process.stdout);
var test = require('unit.js');

//didn't find a working way of having the tests in a seperate file and calling the harmonic function in this file
// so, needed to include the tests in the same .js (tried jquery, and other angles but no luck)

function harmonic(number){
    result = 0;
    //numbers until 50M are accepted
    if (number < 50000001) {
        //numbers are rounded to nearest integer
        //result is calculated
        for(i=1; i <= Math.round(number); i++){
            result += (1/i);
        }
    }
    else if (number > 50000000){
        console.log("Maximum 50.000.000 alowed")
    }
    else{
        console.log("Unsuported input")
    }
    return result.toFixed(4);
};

function askInput(){
    rl.question('Geef een getal: ', getal=>{
        //result = harmonic(getal);
        //return new Promise((result)) 
        return  harmonic(getal)    
    });
};

//run with 'mocha Harmonic'
describe('UNIT tests on the harmonic function', function(){
    it('Passing 5 results in "2.2833"', function(){
      var result = harmonic(5);
      test.assert.equal(result, 2.2833);
    });

    it('Passing 20 results in "3.5977"', function(){
        var result = harmonic(20);
        test.assert.equal(result, 3.5977);
      });

      it('5.4 is rounded to 5', function(){
        var result = harmonic(5.2);
        test.assert.equal(result, 2.2833);
      });

      it('5.5 is rounded to 6', function(){
        var result = harmonic(5.5);
        test.assert.equal(result, 2.4500);
      });

      it('Passing 50000000 results in "18.3047"', function(){
        var result = harmonic(50000000);
        test.assert.equal(result, 18.3047);
      });

      it('Passing 50000001 results in "0"', function(){
        var result = harmonic(50000001);
        test.assert.equal(result, 0);
      });

      it('Passing 0 results in "0"', function(){
        var result = harmonic(0);
        test.assert.equal(result, 0);
      });

      it('Passing negative number results in "0"', function(){
        var result = harmonic(0);
        test.assert.equal(result, 0);
      });

      it('Passing string results in "0"', function(){
        var result = harmonic("test");
        test.assert.equal(result, 0);
      });

    it('askInput() is working', function(done){    //NOT WORKING - function runs synchronous and not asynchronous as it should. didn't find solution yet. tried: Promises, awaits, done, ..
           var result = askInput()
            test.number(result)
    })    
})