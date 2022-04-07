const superagent = require('superagent');
//const res =""

superagent.get('localhost:3000').then(response => { const rawBody = response.text;console.log(rawBody);});

