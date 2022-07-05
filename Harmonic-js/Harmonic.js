export default
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
  