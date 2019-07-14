import { Component, OnInit } from '@angular/core';
import { NavController, AlertController, LoadingController} from '@ionic/angular';
import { RegisterPage } from '../register/register.page';
import { NgForm } from '@angular/forms';
import { Observable } from 'rxjs';
import { MyApiService } from '../../apis/my-api.service';
import { ToastrManager } from 'ng6-toastr-notifications';
import { Storage } from '@ionic/storage';

//Import the page path to which you wish to navigate after person has logged in


@Component({
  selector: 'app-login',
  templateUrl: './login.page.html',
  styleUrls: ['./login.page.scss'],
})
export class LoginPage {
	
	//loading: Loading;
	results: Observable<any>;
	allowed: any;
	
	constructor(private myApiService: MyApiService,
	public navCtrl: NavController,
	private loadingCtrl: LoadingController,
	private alertCtrl: AlertController,
	public toastr: ToastrManager,
	private storage: Storage
	) { }

	login(form: NgForm) {
		this.myApiService.login(form.value.username, form.value.password).subscribe(
		data => {
			console.log(data);
			if (data.token) {
				this.storage.set("ACCESS_TOKEN", data.token);
			}
			//add path to events page
			this.navCtrl.navigateForward('/events');
			
			
			this.storage.get("ACCESS_TOKEN").then((val) => {
				console.log(val);
			});
			
		},
		error =>
		{
		   console.log("Ther awas an error");
		   this.toastr.errorToastr('Username or password is incorrect')
		  
		}
		)
	}
	
	

}
