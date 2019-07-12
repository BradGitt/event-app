import { Component, OnInit } from '@angular/core';

//Import API Service here
//Access app directory level then apis folder
import { EventApiService } from './../../../apis/event-api.service';

//A class that allows us to access the data coming
// our web service asynchronously
import { Observable } from 'rxjs';
import { isEmpty, subscribeOn } from 'rxjs/operators';
import { LoadingController } from '@ionic/angular';
import { ActivatedRoute, Router } from '@angular/router';
import { appInitialize } from '@ionic/angular/dist/app-initialize';
import { async } from 'q';
import {Location} from '@angular/common';  //for delete
import { NavController, AlertController } from '@ionic/angular'; //for alert 



@Component({
  selector: 'app-list',
  templateUrl: './list.page.html',
  styleUrls: ['./list.page.scss'],
})
export class ListPage implements OnInit {

  results: Observable<any>;
  searchTerm = '';

  // added eventAPiService to the constructor so that it automaically recieves
  // a copy of an instance (i.e "dependency injection") which is something ionic
  // does for us hence no need to worry about it
  constructor(private eventApiService: EventApiService, private loadingController: LoadingController, private router: Router, private route: ActivatedRoute,
    private location: Location, public navCtrl: NavController, private alertCtrl: AlertController) {
    // call getEvents() and store in results: Observable<any> class variable 
    // which is accesible on the page
    
    //this.results = this.eventApiService.getEvents();

    // This is how we would invoke the add method
     this.eventApiService.addEvent({description: "hello world!"});

   }

  ngOnInit() {
    this.getEvents();
  }

  async getEvents() {
    const loading = await this.loadingController.create({
      message: 'Loading...'
    });
    await loading.present();
    await this.eventApiService.getEvents()
    .subscribe(results => {
      this.results = this.eventApiService.getEvents();
      console.log(results);
      loading.dismiss();
    },err => {
      console.log(err);
      loading.dismiss();
    });
  }

  searchChanged(){
    this.results = this.eventApiService.searchData(this.searchTerm);
    //  if ( this.eventApiService.searchData(this.searchTerm) !=  undefined || null ) {
    //   this.results = this.eventApiService.searchData(this.searchTerm);
    //   } else {
    //    this.results = this.eventApiService.getEvents();
    //   }


      

    };

      //This allows you to delete an event from the list of events.
      //If you want the delete to be called on another page copy these two methods below
      //and call the deleteConfirm method in the html file 
  async delete(id) {
    const loading = await this.loadingController.create({
      message: 'Deleting'
    });
    await loading.present();
    await this.eventApiService.deleteEvent(id)
      .subscribe(res => {
        loading.dismiss();
        this.location.back();
      }, err => {
        console.log(err);
        loading.dismiss();
      });
  }
   //Used to provide delte confirmation message
  async deleteConfirm(id) {
    let alert = await this.alertCtrl.create({
      message: 'Are you sure you want to delete this event?',
      buttons: [
        {
          text: 'Cancel',
          role: 'cancel',
          cssClass:'icon-color',
          handler: () => {
            this.router.navigate(['list']);
          }
        },
        {
          text: 'Ok',
          cssClass:'icon-color',
          handler: data => {
            this.delete(id)
          }
        }
      ]
    });
    await alert.present();
  }

}
