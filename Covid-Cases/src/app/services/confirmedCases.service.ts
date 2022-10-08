import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { DateModel } from '../_models/dateModel';


@Injectable({
  providedIn: 'root'
})

export class ConfirmedCasesService {

  private endpointConfirmedCasses = "https://api.covid19api.com/country"

  constructor(private http: HttpClient) { }
  
  getConfirmedCasesByCountryAndMonth(country: string, month : number){
    const firstDay = DateModel.firstDayOfMonthISOFormat(month)
    const lastDay = DateModel.lastDayOfMonthISOFormat(month)
    return this.getConfirmedCasesByCountryAndDays(country,firstDay,lastDay)
  
  }

  getConfirmedCasesByCountryAndDays(country: string, firstDay: string, lastDay: string){
    return this.http.get(`${this.endpointConfirmedCasses}/${country}/status/confirmed/live?from=${firstDay}&to=${lastDay}`, {responseType: 'json'})
  }
  
}
