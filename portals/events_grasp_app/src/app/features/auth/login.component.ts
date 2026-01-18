import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router, RouterModule } from '@angular/router';
import { AuthService } from '../../core/auth.service';
import { ToastService } from '../../core/toast.service';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterModule],
  template: `
  <div class="d-flex justify-content-center align-items-center" style="min-height:60vh">
    <div class="card p-4" style="width:360px">
      <h4 class="mb-3">Sign in</h4>
      <form (ngSubmit)="onSubmit()">
        <div class="mb-2">
          <label class="form-label">Username</label>
          <input class="form-control" [(ngModel)]="username" name="username" required />
        </div>
        <div class="mb-3">
          <label class="form-label">Password</label>
          <input type="password" class="form-control" [(ngModel)]="password" name="password" required />
        </div>
        <div class="d-flex justify-content-end gap-2">
          <button type="submit" class="btn btn-primary">Sign in</button>
        </div>
      </form>
    </div>
  </div>
  `
})
export class LoginComponent {
  username = '';
  password = '';

  constructor(private auth: AuthService, private router: Router, private toast: ToastService) {}

  async onSubmit() {
    const ok = await this.auth.login(this.username, this.password);
    if (ok) {
      this.toast.success('Signed in');
      this.router.navigateByUrl('/');
    } else {
      this.toast.error('Login failed');
    }
  }
}
