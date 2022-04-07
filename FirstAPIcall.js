const superagent = require('superagent');

superagent.get('localhost:3000/posts')
.then(response => { 
  const rawBody = response.text;
  const responseCode = response.statusCode;
  console.log(rawBody); 
  console.log(responseCode);
  describe("test",()=>{test("check ResponseCode", () => {const input = responseCode})});
  const output = 200;
})



  
  



   
   


  
