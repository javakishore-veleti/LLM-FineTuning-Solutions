import { Component } from '@angular/core';
import { RouterLink, RouterModule } from '@angular/router';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { AuthService } from '../core/auth.service';

@Component({
  selector: 'app-navbar',
  standalone: true,
  imports: [CommonModule, RouterModule, RouterLink],
  template: `
    <nav class="navbar navbar-expand-lg navbar-dark navbar-custom shadow-sm">
      <div class="container-fluid">
        <a class="navbar-brand d-flex align-items-center gap-2" [routerLink]="isLoggedIn() ? '/dashboard' : '/'">
          <img src="/assets/images/logo.svg" alt="logo" width="36" height="36"/>
          <span class="brand-title">Events Grasp</span>
        </a>

        <button
          class="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarSupportedContent"
          aria-controls="navbarSupportedContent"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span class="navbar-toggler-icon"></span>
        </button>

        <div class="collapse navbar-collapse" id="navbarSupportedContent">
          <ul class="navbar-nav ms-auto mb-2 mb-lg-0 align-items-lg-center">
            <!-- Show Home for non-logged in users -->
            <li class="nav-item" *ngIf="!isLoggedIn()" routerLinkActive="active-top" [routerLinkActiveOptions]="{ exact: true }">
              <a class="nav-link" routerLink="/">
                <i class="bi bi-house-door-fill me-1"></i>
                Home
              </a>
            </li>
            <!-- Show Dashboard for logged in users -->
            <li class="nav-item" *ngIf="isLoggedIn()" routerLinkActive="active-top" [routerLinkActiveOptions]="{ exact: true }">
              <a class="nav-link" routerLink="/dashboard">
                <i class="bi bi-grid-fill me-1"></i>
                Dashboard
              </a>
            </li>
            <li class="nav-item" [class.active-top]="false">
              <a class="nav-link" (click)="navigateOrLogin('/conversations')" style="cursor: pointer;">
                <i class="bi bi-chat-dots-fill me-1"></i>
                Conversations
              </a>
            </li>
            <li class="nav-item" routerLinkActive="active-top" [routerLinkActiveOptions]="{ exact: false }">
              <a class="nav-link" (click)="navigateOrLogin('/administration')" style="cursor: pointer;">
                <i class="bi bi-gear-fill me-1"></i>
                Administration
              </a>
            </li>
            <li class="nav-item" routerLinkActive="active-top" [routerLinkActiveOptions]="{ exact: false }">
              <a class="nav-link" (click)="navigateOrLogin('/settings')" style="cursor: pointer;">
                <i class="bi bi-sliders me-1"></i>
                Settings
              </a>
            </li>
            <!-- Login/Logout -->
            <li class="nav-item ms-lg-2" *ngIf="!isLoggedIn()">
              <a class="nav-link btn btn-outline-light btn-sm px-3" routerLink="/login">
                Sign In
              </a>
            </li>
            <li class="nav-item ms-lg-2" *ngIf="isLoggedIn()">
              <a class="nav-link btn btn-outline-light btn-sm px-3" (click)="logout()" style="cursor: pointer;">
                Sign Out
              </a>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  `
})
export class NavbarComponent {
  constructor(private auth: AuthService, private router: Router) {}

  isLoggedIn(): boolean {
    return this.auth.isAuthenticated();
  }

  navigateOrLogin(path: string) {
    if (this.auth.isAuthenticated()) {
      this.router.navigateByUrl(path);
    } else {
      this.router.navigate(['/login'], { queryParams: { redirect: path } });
    }
  }

  async logout() {
    await this.auth.logout();
    this.router.navigateByUrl('/');
  }
}
