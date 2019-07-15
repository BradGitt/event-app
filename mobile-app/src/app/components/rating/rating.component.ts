// import { Component, OnInit } from '@angular/core';

// @Component({
//   selector: 'app-rating',
//   templateUrl: './rating.component.html',
//   styleUrls: ['./rating.component.scss'],
// })
// export class RatingComponent implements OnInit {

//   constructor() { }

//   ngOnInit() {}

// }

import { Component, Input, EventEmitter ,Output} from "@angular/core";
import { IonicModule } from '@ionic/angular';
import { RouterModule } from '@angular/router';
import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

import { StarRating } from 'ionic4-star-rating';
import { EventDetailsPage } from 'src/app/pages/events/event-details/event-details.page';
@Component({
  selector: "rating",
  templateUrl: "./rating.component.html"
})

@NgModule({
  declarations: [ StarRating],
  imports: [
    IonicModule,
    CommonModule,
    FormsModule,
    RouterModule.forChild([{ path: '', component: EventDetailsPage}])
  ],
  exports: [ StarRating ]
}) 




export class RatingComponent {
  @Input() rating: number ;

  @Output() ratingChange: EventEmitter<number> = new EventEmitter();

  constructor() {}

  rate(index: number) {
      // function used to change the value of our rating 
      // triggered when user, clicks a star to change the rating
      this.rating = index;
      this.ratingChange.emit(this.rating);
   }

  getColor(index: number) {
      /* function to return the color of a star based on what
       index it is. All stars greater than the index are assigned
       a grey color , while those equal or less than the rating are
       assigned a color depending on the rating. Using the following criteria:
    
            1-2 stars: red
            3 stars  : yellow
            4-5 stars: green 
      */
     if (this.isAboveRating(index)) {
       return COLORS.GREY;
     }
     switch (this.rating) {
       case 1:
        case 2:
          return COLORS.RED;
        case 3:
          return COLORS.YELLOW;
        case 4:
        case 5:
          return COLORS.GREEN;
        default:
          return COLORS.GREY;
     }
    }

  isAboveRating(index: number): boolean {
    // returns whether or not the selected index is above ,the current rating
    // function is called from the getColor function.
    return index > this.rating;
  }
  logRatingChange(rating){
    console.log("changed rating: ",rating);
    // do your stuff
}

}

enum COLORS {
  GREY = "#E0E0E0",
  GREEN = "#76FF03",
  YELLOW = "#FFCA28",
  RED = "DD2C00"
}