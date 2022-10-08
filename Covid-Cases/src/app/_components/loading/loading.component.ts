import { Component, Input, OnInit } from '@angular/core';
import { Progress } from 'src/app/_models/progress';

@Component({
  selector: 'app-loading',
  templateUrl: './loading.component.html',
  styleUrls: ['./loading.component.css']
})
export class LoadingComponent implements OnInit {
  @Input() progress!: Progress
  
  constructor() { }

  ngOnInit(): void {
  }

}
