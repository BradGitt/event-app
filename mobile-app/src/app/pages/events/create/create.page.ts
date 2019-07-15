import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, FormControl, Validators } from '@angular/forms';
import {ReactiveFormsModule} from '@angular/forms';
import { Event } from 'src/app/event';
import {Observable} from 'rxjs';
import { EventApiService } from 'src/app/apis/event-api.service';

@Component({
  selector: 'app-create',
  templateUrl: './create.page.html',
  styleUrls: ['./create.page.scss'],
})

// export class FormsPage {
//   form = {}
//   onSubmit() {
//     console.log(this.form)
//   }
// }
export class CreatePage implements OnInit {
  eventForm: FormGroup;

  constructor(private formbuilder:FormBuilder,private myApi: EventApiService) { 
    this.eventForm = formbuilder.group({
      title: new FormControl(''),
      name: new FormControl(''),
      category: new FormControl(''),
      start_date: new FormControl(''),
      start_time: new FormControl(''),
      end_date: new FormControl(''),
      end_time: new FormControl(''),
      cost: new FormControl(),
      venue: new FormControl(''),
      description: new FormControl(''),
      
    }
    )
  }

  ngOnInit() {
  }
  onSubmit(): void{
    let event = new Event()
    event.title=this.eventForm.controls.title.value;
    event.name=this.eventForm.controls.name.value;
    event.category=this.eventForm.controls.category.value;
    event.start_date=this.eventForm.controls.start_date.value;
    event.start_time=this.eventForm.controls.start_time.value;
    event.end_date=this.eventForm.controls.end_date.value;
    event.end_time=this.eventForm.controls.end_time.value;
    event.cost=this.eventForm.controls.cost.value;
    event.venue=this.eventForm.controls.venue.value;
    event.description=this.eventForm.controls.description.value;
   
    this.myApi.createEvent(event).subscribe((response)=>console.log('response',response));
  }

  // export class FormsPage {
//   form = {}
//   onSubmit() {
//     console.log(this.form)
//   }
// }

}
