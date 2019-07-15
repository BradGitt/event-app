import { Component, OnInit } from '@angular/core';
import { EventApiService } from 'src/app/apis/event-api.service';
import { Observable } from 'rxjs';
import { LoadingController } from '@ionic/angular';
import { ActivatedRoute, Router } from '@angular/router';
import { FormControl, FormGroupDirective, FormBuilder, FormGroup, NgForm, Validators } from '@angular/forms';
import { Review } from '../../../review';


@Component({
  selector: 'app-event-details',
  templateUrl: './event-details.page.html',
  styleUrls: ['./event-details.page.scss'],
})
export class EventDetailsPage implements OnInit {
    information:any;
    myId=null;
    reviews:any;
    // res: Observable<any>;

    reviewForm: FormGroup;
    email:string ='';
    rating:number=null;
    comment:string ='';

  constructor(private activatedRoute: ActivatedRoute, private eventApiService: EventApiService,public loadingController: LoadingController,
    public router: Router, private route: ActivatedRoute, private formBuilder: FormBuilder) { }

  ngOnInit() {

    this.reviewForm= this.formBuilder.group({
      'email' : [null,Validators.required],
      'rating' : [null,Validators.required],
      'comment' : [null,Validators.required]
    });

    
   //let id = this.activatedRoute.snapshot.paramMap.get('id');
   this.myId=this.activatedRoute.snapshot.paramMap.get('myid');
   this.getRev(this.myId);

   this.eventApiService.getDetails(this.myId).subscribe(result => {
     console.log('details: ', result);
     this.information = result['event'];
     //console.log(this.myId);
     //console.log(this.information.event);

    

   });
  }

  async getRev(id) {
    const loading = await this.loadingController.create({
      message: 'Loading...'
    });
    await loading.present();
    await this.eventApiService.getReviews(id)
      .subscribe(res => {
        this.reviews = res;
        // console.log(this.reviews);
        // console.log(res);
        loading.dismiss();
      }, err => {
        console.log(err);
        loading.dismiss();
      });
  }

  async onFormSubmit(form:NgForm) {
    const loading = await this.loadingController.create({
      message: 'Loading...'
    });
    await loading.present();
    await this.eventApiService.addReview(form,this.myId)
      .subscribe(res => {//res is from json in api
          let id =this.myId
          loading.dismiss();
          // return to list of events
          this.router.navigate(['/details/'+`${id}`])
          console.log(this.router);
          //this.router.navigate(['/details/'+`${id}`])
         
        }, (err) => {
          console.log(err);
          loading.dismiss();
        });
  }

  
  }


