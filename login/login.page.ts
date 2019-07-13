import { Component, OnInit } from '@angular/core';
import { NavController } from '@ionic/angular';
import { RegisterPage } from '../register/register.page';
import { NgForm } from '@angular/forms';
import { Observable } from 'rxjs';
import { MyApiService } from '../../apis/my-api.service';
@Component({
  selector: 'app-login',
  templateUrl: './login.page.html',
  styleUrls: ['./login.page.scss'],
})
export class LoginPage {
	
	results: Observable<any>;
	
	constructor(private myApiService: MyApiService) { }

	login(form: NgForm) {
	  this.myApiService.login(form.value.username, form.value.password);
	}
	
	//goRegister(){
		//this.navCtrl.navigateForward('/register');
		//this.router.navigateByUrl('/register');
	//}

}
