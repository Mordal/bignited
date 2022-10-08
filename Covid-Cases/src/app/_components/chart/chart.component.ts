import { Component, OnInit, Input } from '@angular/core';
import { ChartDataset, ChartOptions } from 'chart.js';
import { DateModel } from 'src/app/_models/dateModel';
import { Country } from 'src/app/_models/country';

@Component({
  selector: 'app-chart',
  templateUrl: './chart.component.html',
  styleUrls: ['./chart.component.css']
})
export class ChartComponent implements OnInit {
  @Input() country!: Country

  chartData: ChartDataset[] = [];
  chartLabels: string[] = []
  chartOptions: ChartOptions = {};

  constructor() { }

  ngOnInit(): void {
    this.chartOptions = { 
      responsive: true,
      maintainAspectRatio: false,
      plugins: { 
      title: { 
        display : true,
        position: "top",
        text: (DateModel.getMonthName(this.country.month) + " 2020") ,
        font: {
          size: 16
        }
      },
      legend: {
        display: true
      }},
      scales: {
        y: {
          type: 'linear',
          display: true,
          position: 'left',
        },
        y1: {
          type: 'linear',
          display: true,
          position: 'right',
          ticks: {
            //this formats the right y-axis labels
            callback: function(value) {
              return Number(value).toPrecision(2) + " %";
            }
          },
          grid: {
            drawOnChartArea: false, 
          }
        }
    }}

    this.chartData = [
      {
        data: this.country.confirmedCases,
        label: 'Confirmed Cases',
        yAxisID: 'y'
      },
      {
        data:  this.getPercentageOfConfirmedCasesForPopulation(this.country),
        label: 'Relative cases',
        yAxisID: 'y1'
      }

    ];
    this.chartLabels = this.getLabelsForMonth(this.country)

  }

  // ## FUNCTIONS ## //
  getLabelsForMonth(country: Country): Array<string>{
    let indexes = new Array<any>;
    country.confirmedCases.forEach((_value, index) => {
      indexes.push((Number(index)+1) + " "+ DateModel.getMonthName(this.country.month))
    })
    return indexes
  }

  getPercentageOfConfirmedCasesForPopulation(country: Country): Array<number>{
    let percentages = new Array<any>;
    for (var cases of country.confirmedCases){
      percentages.push(cases/Number(country.population)*100)
    }
    return percentages
  }
}

