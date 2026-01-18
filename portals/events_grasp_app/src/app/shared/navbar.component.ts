import { Component } from '@angular/core';
import { RouterLink, RouterModule } from '@angular/router';
import { CommonModule } from '@angular/common';
import { Router, NavigationEnd } from '@angular/router';
import { AuthService } from '../core/auth.service';
import { filter } from 'rxjs/operators';

@Component({
  selector: 'app-navbar',
  standalone: true,
  imports: [CommonModule, RouterModule, RouterLink],
  styles: [`
    .nav-link.active-highlight {
      position: relative;
    }
    .nav-link.active-highlight::after {
      content: '';
      position: absolute;
      bottom: -2px;
      left: 50%;
      transform: translateX(-50%);
      width: 20px;
      height: 3px;
      background: white;
      border-radius: 2px;
    }
  `],
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
            <li class="nav-item" *ngIf="!isLoggedIn()">
              <a class="nav-link" routerLink="/" routerLinkActive="active-highlight" [routerLinkActiveOptions]="{ exact: true }">
                <i class="bi bi-house-door-fill me-1"></i>
                Home
              </a>
            </li>
            <!-- Show Dashboard for logged in users -->
            <li class="nav-item" *ngIf="isLoggedIn()">
              <a class="nav-link" routerLink="/dashboard" routerLinkActive="active-highlight" [routerLinkActiveOptions]="{ exact: true }">
                <i class="bi bi-grid-fill me-1"></i>
                Dashboard
              </a>
            </li>
            <li class="nav-item">
              <a class="nav-link" [class.active-highlight]="isRouteActive('/conversations')" (click)="navigateOrLogin('/conversations')" style="cursor: pointer;">
                <i class="bi bi-chat-dots-fill me-1"></i>
                Conversations
              </a>
            </li>
            <li class="nav-item">
              <a class="nav-link" [class.active-highlight]="isRouteActive('/administration')" (click)="navigateOrLogin('/administration')" style="cursor: pointer;">
                <i class="bi bi-gear-fill me-1"></i>
                Administration
              </a>
            </li>
            <li class="nav-item">
              <a class="nav-link" [class.active-highlight]="isRouteActive('/settings')" (click)="navigateOrLogin('/settings')" style="cursor: pointer;">
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
  private currentUrl: string = '';

  constructor(private auth: AuthService, private router: Router) {
    // Subscribe to route changes to track current URL
    this.currentUrl = this.router.url;
    this.router.events.pipe(
      filter(event => event instanceof NavigationEnd)
    ).subscribe((event: any) => {
      this.currentUrl = event.urlAfterRedirects || event.url;
    });
  }

  isLoggedIn(): boolean {
    return this.auth.isAuthenticated();
  }

  isRouteActive(path: string): boolean {
    return this.currentUrl.startsWith(path);
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
