import { Injectable } from '@angular/core';

import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';

import { Storage } from '@ionic/storage';
import { ToastrManager } from 'ng6-toastr-notifications';
import { NavController} from '@ionic/angular';





@Injectable({
  providedIn: 'root'
})
export class MyApiService {
	isLoggedin: false;
	token:any;
	
	constructor(private http:HttpClient,
	private storage: Storage,
	public navCtrl: NavController,
	public toastr: ToastrManager){}
	
	login(username:String, password:String)
	{
		//console.log("hello there");
		
		//return this.http.get("http://127.0.0.1:5000/login").pipe(map(results => results));
		
		const headers = new HttpHeaders({
      'Authorization': 'Basic ' + btoa(username+":"+password)
    });
	
		console.log(username + " " + password);
		console.log(btoa(username+":"+password));
		return this.http.get('http://127.0.0.1:5000/login',{headers});
	}
		
	logout () {
		this.storage.remove("ACCESS_TOKEN");
		this.isLoggedin = false;
		console.log("removed");
		
	}
	
	getToken() {
		return this.storage.get("ACCESS_TOKEN").then( (val) => {
			if (val == null) {
				console.log("Empty");
				this.navCtrl.navigateForward('/login');
				this.toastr.errorToastr('UNAUTHORIZED! Please Login');
			} else {
				console.log ("still there");
				
			}
		});
	}
      
}
