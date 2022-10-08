import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class VaccinesService {

  private endpointVaccines = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/country_data"

  constructor(private http: HttpClient) { }

  getVaccines(country: string): Observable<any>{
    return this.http.get(`${this.endpointVaccines}/${country}.csv`, {responseType: 'text'})
  }


}
