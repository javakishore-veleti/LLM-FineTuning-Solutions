import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ApiService } from './api.service';
import { AuthService } from './auth.service';
import { ToastService } from './toast.service';

@NgModule({
  imports: [CommonModule],
  providers: [ApiService, AuthService, ToastService]
})
export class CoreModule {}
