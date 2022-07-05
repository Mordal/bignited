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
  });
  