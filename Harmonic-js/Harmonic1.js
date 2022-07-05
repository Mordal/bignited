//import harmonic from './harmonic.js';
//import askInput from './askinput.js';
const fs = require('fs');
const expect = require('chai').expect;
var readline = require('readline');
var rl = readline.createInterface(process.stdin, process.stdout);
var test = require('unit.js');


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
//didn't find a working way of having the tests in a seperate file and calling the harmonic function in this file
// so, needed to include the tests in the same .js (tried jquery, and other angles but no luck)

//run with 'mocha Harmonic'
describe('UNIT tests on the harmonic function', function () {
  it("testCases.txt exists", function(){
  expect(fs.existsSync('testCases.txt')).to.be.true
  });

  fs.readFile('./testCases.txt', 'utf8', (err, data) => {
    if (err) throw err;
    var testCases = new Map(eval(data));
    describe('Test cases from file:', function () {
    testCases.forEach((expectedResult, testValue ) =>{      
      it('Passing '+ testValue + ' results in "' + expectedResult+'"', function(){
        var result = harmonic(testValue);
        test.assert.equal(result, expectedResult);
        });
      }); 
    });
  });


  describe('Test cases from file:', function () {
    askInput()
    it('askInput() is working', askInput(), result => {    //NOT WORKING - function runs synchronous and not asynchronous as it should. didn't find solution yet. tried: Promises, awaits, done, ..

        test.number(result);
        console.log(result);
        //done()
        //};
        
    
      })
    })
  })
