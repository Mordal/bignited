import { NgModule } from '@angular/core';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { HomeComponent } from './_pages/home/home.component';
import { InfoComponent } from './_components/info/info.component';

import { HttpClientModule} from '@angular/common/http';
import { NgChartsModule } from 'ng2-charts';
import { ChartComponent } from './_components/chart/chart.component';
import { LoadingComponent } from './_components/loading/loading.component';




@NgModule({
  declarations: [
    AppComponent,
    HomeComponent,
    InfoComponent,
    ChartComponent,
    LoadingComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    FormsModule,
    ReactiveFormsModule,
    HttpClientModule,
    NgChartsModule,

  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
