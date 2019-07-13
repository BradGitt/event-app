import { Injectable } from '@angular/core';

import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { NativeStorage } from '@ionic-native/native-storage/ngx';

@Injectable({
  providedIn: 'root'
})
export class MyApiService {
	token:any;
	
	constructor(private http:HttpClient,  
	private storage: NativeStorage){}
	
	login(username:String, password:String)
	{
		//console.log("hello there");
		
		//return this.http.get("http://127.0.0.1:5000/login").pipe(map(results => results));
		
		const headers = new HttpHeaders({
      'Authorization': 'Basic ' + btoa(username+":"+password)
    });
	
		console.log(username + " " + password);
		console.log(btoa(username+":"+password));
		return this.http.get('http://127.0.0.1:5000/login',{headers}).subscribe((res)=>{
            console.log(res.token);
			
			this.storage.setItem('token', res.token);
			this.storage.getItem('token').then(
			data => console.log(data),
			error => console.error(error))
        });
		
		
	}
			
	
}
