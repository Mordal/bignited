import { Component, Input, OnInit} from '@angular/core';
import { Country } from 'src/app/_models/country';



@Component({
  selector: 'app-info',
  templateUrl: './info.component.html',
  styleUrls: ['./info.component.css']
})

export class InfoComponent implements OnInit {
  @Input() country!: Country

  constructor() { }

  ngOnInit(): void {
  }
}

