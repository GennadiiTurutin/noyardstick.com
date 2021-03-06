import { Component, OnInit } from '@angular/core';
import { FormGroup, Validators, FormBuilder } from '@angular/forms';
import { MatDialog, MatDialogRef } from '@angular/material';
import { ApiService } from 'src/app/services/api.service';
import { Router } from '@angular/router';
import { ToastrService } from 'ngx-toastr';
import { Title } from '@angular/platform-browser';


@Component({
  selector: 'app-subscription',
  templateUrl: './subscription.component.html'
})
export class SubscriptionComponent implements OnInit {
  userSubscribe: FormGroup;
  providers: [ApiService];
  loading: boolean = false;

  constructor(private fb: FormBuilder,
              public DialogRef: MatDialogRef<SubscriptionComponent>,
              public dialog: MatDialog,
              private api: ApiService,
              private router: Router,
              private toastr: ToastrService,
              private titleService: Title
              ) { 
    this.userSubscribe = this.fb.group({
      email: ['', [Validators.required, Validators.email] ],
    });
  }

  ngOnInit() { }

  
  subscribeUser() {
    this.loading = true;
    this.api.postSubscriber(this.userSubscribe.value).subscribe(
      response => {
        console.log("You've successfully subscribed!");
        this.toastr.success('Subscription', "You've successfully subscribed!" );
        
        this.router.navigate(['/']);
        this.Close(); 
      },
      error => {
        this.loading = false;
        console.log('error', error);
        this.toastr.error('Error', error.error.email);
      }
    )
  }

  Close(): void {
    this.DialogRef.close();
  }

}
