import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';

@Component({
  selector: 'app-admin-layout',
  standalone: true,
  imports: [CommonModule, RouterModule],
  template: `
    <div class="container-fluid mt-3">
      <div class="row">
        <nav class="col-md-3 col-lg-2 d-md-block bg-white sidebar collapse show p-3">
          <h5>Administration</h5>
          <ul class="nav flex-column">
            <li class="nav-item">
              <a class="nav-link" routerLink="/administration/events" routerLinkActive="active" [routerLinkActiveOptions]="{ exact: false }">Events</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" routerLink="/administration/vector-stores" routerLinkActive="active" [routerLinkActiveOptions]="{ exact: false }">Vector Stores</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" routerLink="/administration/scraping-logs" routerLinkActive="active" [routerLinkActiveOptions]="{ exact: false }">Scraping Logs</a>
            </li>
          </ul>
        </nav>

        <main class="col-md-9 ms-sm-auto col-lg-10 px-md-4">
          <div class="pt-3">
            <router-outlet></router-outlet>
          </div>
        </main>
      </div>
    </div>
  `
})
export class AdminLayoutComponent {}
