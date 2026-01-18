import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';

@Component({
  selector: 'app-admin-layout',
  standalone: true,
  imports: [CommonModule, RouterModule],
  styles: [`
    .admin-container {
      min-height: calc(100vh - 60px);
      display: flex;
      background: #f5f7fb;
    }
    .admin-sidebar {
      width: 280px;
      background: white;
      border-right: 1px solid #e8e8e8;
      padding: 0;
      flex-shrink: 0;
      position: sticky;
      top: 60px;
      height: calc(100vh - 60px);
      overflow-y: auto;
    }
    .sidebar-header {
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      padding: 1.5rem;
      color: white;
    }
    .sidebar-title {
      font-size: 1.25rem;
      font-weight: 700;
      margin: 0;
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }
    .sidebar-subtitle {
      font-size: 0.85rem;
      opacity: 0.9;
      margin-top: 0.25rem;
    }
    .nav-section {
      padding: 1rem 0;
    }
    .nav-section-title {
      font-size: 0.7rem;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      color: #999;
      padding: 0.5rem 1.5rem;
      margin: 0;
    }
    .nav-menu {
      list-style: none;
      padding: 0;
      margin: 0;
    }
    .nav-menu-item {
      margin: 0.25rem 0.75rem;
    }
    .nav-menu-link {
      display: flex;
      align-items: center;
      gap: 0.75rem;
      padding: 0.75rem 1rem;
      border-radius: 10px;
      color: #555;
      text-decoration: none;
      font-weight: 500;
      transition: all 0.2s;
      font-size: 0.95rem;
    }
    .nav-menu-link:hover {
      background: #f5f7fb;
      color: #667eea;
    }
    .nav-menu-link.active {
      background: linear-gradient(135deg, rgba(102,126,234,0.1) 0%, rgba(118,75,162,0.1) 100%);
      color: #667eea;
      font-weight: 600;
    }
    .nav-menu-link.active .nav-icon {
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    .nav-icon {
      width: 36px;
      height: 36px;
      border-radius: 10px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 1.1rem;
      background: #f0f0f0;
      flex-shrink: 0;
    }
    .nav-text {
      flex: 1;
    }
    .nav-badge {
      font-size: 0.7rem;
      padding: 0.2rem 0.5rem;
      border-radius: 10px;
      background: #667eea;
      color: white;
      font-weight: 600;
    }
    .admin-content {
      flex: 1;
      min-width: 0;
      overflow-x: hidden;
    }
    @media (max-width: 991px) {
      .admin-container {
        flex-direction: column;
      }
      .admin-sidebar {
        width: 100%;
        height: auto;
        position: relative;
        top: 0;
        border-right: none;
        border-bottom: 1px solid #e8e8e8;
      }
      .nav-section {
        padding: 0.5rem 0;
      }
      .nav-menu {
        display: flex;
        flex-wrap: wrap;
        padding: 0 0.5rem;
      }
      .nav-menu-item {
        margin: 0.25rem;
      }
    }
  `],
  template: `
    <div class="admin-container">
      <!-- Sidebar -->
      <aside class="admin-sidebar">
        <div class="sidebar-header">
          <h2 class="sidebar-title">
            <span>⚙️</span>
            Administration
          </h2>
          <p class="sidebar-subtitle">Manage your events & resources</p>
        </div>

        <nav class="nav-section">
          <p class="nav-section-title">Content Management</p>
          <ul class="nav-menu">
            <li class="nav-menu-item">
              <a class="nav-menu-link" routerLink="/administration/events" routerLinkActive="active" [routerLinkActiveOptions]="{ exact: false }">
                <span class="nav-icon">📄</span>
                <span class="nav-text">Events</span>
              </a>
            </li>
            <li class="nav-menu-item">
              <a class="nav-menu-link" routerLink="/administration/scraping-logs" routerLinkActive="active" [routerLinkActiveOptions]="{ exact: false }">
                <span class="nav-icon">🔍</span>
                <span class="nav-text">Scraping Results</span>
              </a>
            </li>
            <li class="nav-menu-item">
              <a class="nav-menu-link" routerLink="/administration/vector-stores" routerLinkActive="active" [routerLinkActiveOptions]="{ exact: false }">
                <span class="nav-icon">🗄️</span>
                <span class="nav-text">Vector Stores</span>
              </a>
            </li>
          </ul>
        </nav>
      </aside>

      <!-- Main Content -->
      <main class="admin-content">
        <router-outlet></router-outlet>
      </main>
    </div>
  `
})
export class AdminLayoutComponent {}
