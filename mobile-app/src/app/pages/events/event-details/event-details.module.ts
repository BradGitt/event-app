import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { Routes, RouterModule } from '@angular/router';
// import { ComponentsModule } from '../../../components/components.module';

import { IonicModule } from '@ionic/angular';

import { EventDetailsPage } from './event-details.page';

const routes: Routes = [
  {
    path: '',
    component: EventDetailsPage
  }
];

@NgModule({
  imports: [
    CommonModule,
    FormsModule,
    ReactiveFormsModule,
    IonicModule,
    RouterModule.forChild(routes)
  ],
  declarations: [EventDetailsPage]
})
export class EventDetailsPageModule {}
