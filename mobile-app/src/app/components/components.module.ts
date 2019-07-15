import { NgModule } from '@angular/core';
import { RatingComponent } from './rating/rating.component';
import { IonicModule } from '@ionic/angular';
import { CommonModule } from "@angular/common";
import { StarRating } from 'ionic4-star-rating';

@NgModule({
    declarations: [RatingComponent ],
    imports: [ CommonModule, IonicModule.forRoot(),
    ],
    exports: [RatingComponent]
})

export class ComponentsModule{

}