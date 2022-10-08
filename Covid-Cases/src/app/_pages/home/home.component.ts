
import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { ConfirmedCasesService } from 'src/app/services/confirmedCases.service';
import { CountriesService } from 'src/app/services/countries.service';
import { VaccinesService } from 'src/app/services/vaccines.service';
import { Country } from 'src/app/_models/country';
import { DateModel } from 'src/app/_models/dateModel';
import { Progress } from 'src/app/_models/progress';



@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {

  formCovidCases!: FormGroup
  countryList!: string[]
  months!: string[]
  country!: Country
  errorMessage!: string
  confirmedCasesByDayToBeSorted !: Map<string, number>
  checkExecutionAllWeeks !: number
  readyForChart !: Boolean
  progress !: Progress
  
  
  constructor(
    private formBuilder: FormBuilder,
    private countriesService: CountriesService,
    private countryCSV: VaccinesService,
    private confirmedCases: ConfirmedCasesService,
    ) { }



  ngOnInit(): void {
    //validators for the inputfields
    this.formCovidCases = this.formBuilder.group({
      'country':['',Validators.required],
      'month' : ['',Validators.required]
    })

    //getting all countries from endpoint
    this.countriesService.getCountries().subscribe({
      next: (rawCountries) => {
        let countryList = new Array();
        for (let i = 0; i<rawCountries.length; i++){
          countryList.push(JSON.parse(JSON.stringify(rawCountries[i])).name);
        }
        this.countryList = countryList;
      }
    })
    
    //getting all months in a year
    this.months = DateModel.getMonthList();

    //initiating this.country
    this.country = {} as Country
    //initiating this.progress
    this.progress = {} as Progress
  }

  onSubmit(){
    //validating inputfields before all other actions
    if (this.formCovidCases.invalid)
      return;
    
    //reset
    this.readyForChart = false
    this.errorMessage = ""

    //setting given values in this.country
    this.country.name = this.formCovidCases.get(["country"])?.value
    this.country.month = this.formCovidCases.get(["month"])?.value

    //Set currently used vaccines
    this.setCurrentlyUsedVaccines(this.country.name)
    
    //Set population
    this.setPopulation(this.country.name)

    //Set confirmed cases by country and month
    this.setConfirmedCasesByCountryAndMonth(this.country.name,this.country.month)
  }


// ## FUNCTIONS ## //

setCurrentlyUsedVaccines(country: string){
  this.countryCSV.getVaccines(country).subscribe({
    next:(csvFile) => {
      //response is in csv-string-format
        // all lines in the string are separated in the lines[] array
      let lines = csvFile.split("\n"); 
        // headers are extracted from first line
      let headers = lines[0].split(",")
        // for extensibility reasons, the index number of the column with header 'vaccine' is retrieved
         // rather than hardcoded
      let vaccineIndex = 0
      headers.forEach((header:string, index:number) =>{
        if (header === "vaccine"){
          vaccineIndex = index
        }
      })
      // from the last line and in column 'vaccineIndex' we extract the last used vaccines
      let usedVaccines = this.splitCsvRow(lines[lines.length - 2])
      // vaccines are split to become a list
      this.country.vaccinesUsed = usedVaccines[vaccineIndex].split(",")
    },
    error: (err:any) => {
      //when API call returns an error
      this.country.vaccinesUsed = ["NO DATA"]
    }
  })
}

setPopulation(country: string){
  this.countriesService.getPopulationByCountry(country).subscribe({
    next:(rawPopulation) => {
      this.country.population = JSON.parse(JSON.stringify(rawPopulation[0])).population
    }
  })
}

setConfirmedCasesByCountryAndMonth(country: string, month: number){
  this.confirmedCases.getConfirmedCasesByCountryAndMonth(country,month).subscribe({
    next:(response) => {
      // parsing to readable JSON object
      let allObjects = JSON.parse(JSON.stringify(response))
      this.progress.total = allObjects.length
      //values of the returned Map() are loaded in country.confirmedCases
      this.country.confirmedCases = [...this.getConfirmedCasesFromObjects(allObjects).values()]
      //allowing to initiate the chart.html component
      this.readyForChart = true
    },
    // when API call returns an error
    error: (err:any) => {
      let errorMessage = JSON.parse(JSON.stringify(err)).error.message
      //some countries have restrictions on certain months with the folowing error as response
      if (errorMessage == "for performance reasons, please specify a province or a date range up to a week"){
        //this error-cases are is handled in the following function (example: USA november and december)
        this.confirmedCasesByWeek()
      }else{
        this.errorMessage = errorMessage
      }
    }
  }) 
}

//for some countries (USA for example) we need to retrieve the data week by week
confirmedCasesByWeek(){
  // all calls are done at the same time, the responses can be in a wrong order, 
    // the date-key is used to sort the data
  this.confirmedCasesByDayToBeSorted = new Map<string, number>()
  let lastDayOfMonth = DateModel.lastDayOfMonth(this.country.month)
  this.checkExecutionAllWeeks = 0
  
  // for each week in the month -> get the confirmed cases
  for (let i = 0 ; i < lastDayOfMonth; i+=8){
    //first day of first week = 1, first days of other weeks = i+8
    let firstDay = (i < 8) ? (i+1) : i
    //last day of each week = i+7 except for last day of the month
    let lastDay = (i+7 > lastDayOfMonth) ? lastDayOfMonth : (i+7)

    //getting confirmed Covid cases
    this.confirmedCases.getConfirmedCasesByCountryAndDays(this.country.name,DateModel.dayOfMonthISOFormat(this.country.month,firstDay),DateModel.dayOfMonthISOFormat(this.country.month,lastDay))
    .subscribe({
      next:(response) => {
        // parsing to readable JSON object
        let allObjects = JSON.parse(JSON.stringify(response))
        //adding all returned (from this.getConfirmedCasesFromObjects()) records to this.confirmedCasesByDayToBeSorted
        this.confirmedCasesByDayToBeSorted = new Map<string, number>([...this.confirmedCasesByDayToBeSorted,...this.getConfirmedCasesFromObjects(allObjects)])
        //when all requests have returned a response, checkExecutionsAllWeeks is now = 3 (there are always 4 weeks in a month)
        if(this.checkExecutionAllWeeks == 3){
          //sorting all entries before populating the country.confirmedCases
          this.confirmedCasesByDayToBeSorted = new Map([...this.confirmedCasesByDayToBeSorted.entries()].sort())
          this.country.confirmedCases = [...this.confirmedCasesByDayToBeSorted.values()]
          //allowing to initiate the chart.html component
          this.readyForChart = true
        }
        this.checkExecutionAllWeeks +=1
      }
    })
  }
}

getConfirmedCasesFromObjects(allObjects:any){
  // for some countries (example: China) the returned array has multiple objects for 1 day
    // I needed to add a key (with date info) to the data
    // this key is used to determine if data needs to be added to data of the same day
  
  //this.progress is for visualising the progress
  this.progress.total = allObjects.length
  //initialise new Map to be filled in the forEach loop
  let totalConfirmedCases = new Map<string, number>()
  allObjects.forEach((day: { Cases: number; Date: string }, index: number) => {
    if (totalConfirmedCases.has(day.Date)){
      this.progress.date = day.Date
      this.progress.currentProccessing = index
      //adding cases to cases of the same day
      let totalCases = Number(totalConfirmedCases.get(day.Date)) + day.Cases
      totalConfirmedCases.delete(day.Date)
      totalConfirmedCases.set(day.Date, totalCases)
    } else{
      //if date doesn't exist yet, new record is created
      totalConfirmedCases.set(day.Date, day.Cases)
    }
  });
  return totalConfirmedCases
}

  splitCsvRow(row: string):string[]{
    //splitting is done by first replacing the "," characters by "|", but only those 
    // which are not in between quotes; these "," need to stay intact.
    let string = ""
    let quotes = false
    for(let character of row){
      if (character == "," && !quotes){
        character = "|"
      }
      if (character == '"'){
        character = ""
        quotes = !quotes
      }
      string += character
    }
  return string.split("|")
  }

}