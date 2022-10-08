import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';


@Injectable({
  providedIn: 'root'
})
export class CountriesService {

  private endpointCountries = "https://restcountries.com/v2/all?fields=name"
  private endpointPopulation = 'https://restcountries.com/v3.1/name/'

  constructor(private http: HttpClient) {}

  getCountries(): Observable<Array<string>>{
    return this.http.get<Array<string>>(`${this.endpointCountries}`)
  }

  getPopulationByCountry(country: string): Observable<Array<string>>{
    return this.http.get<Array<string>>(`${this.endpointPopulation}${country}?fields=population`)
  } 

}

