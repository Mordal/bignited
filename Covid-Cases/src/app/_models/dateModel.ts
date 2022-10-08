      //It is hard to transform the local-time-zoned Date() to an ISO format
    //using the .toISOdate() methode because of the timezone offset.
    //I opted to construct the ISO format myself
    
//methods are self explanatory
export class DateModel {
    static lastDayOfMonth(month: number) : number {
        return new Date(2020,Number(month)+1,0).getDate()
    }
    
    static monthNumberToString(month: number): string {
        return (month < 9 ) ? "0"+(Number(month)+1) : (Number(month)+1).toString()
    }

    static firstDayOfMonthISOFormat(month: number) : string {
        return "2020-"+this.monthNumberToString(month)+"-01T00:00:00Z"
    }

    static lastDayOfMonthISOFormat(month : number) : string {
        return "2020-"+this.monthNumberToString(month)+"-"+this.lastDayOfMonth(month)+"T00:00:00Z"
      }
    
      static dayOfMonthISOFormat(month: number, day: number){
        let dayString = (day < 10) ? "0"+day : day
        return "2020-"+this.monthNumberToString(month)+"-"+dayString+"T00:00:00Z"
      }

      static getMonthList():string[]{
        let monthList = new Array();
        for (let i =0; i <12 ; i++){
          monthList.push(this.getMonthName(i))
        }
        return monthList;
      }

      static getMonthName(month: number): string {
        return new Date(2022, month).toLocaleString('en', { month: 'long' })
      }

}