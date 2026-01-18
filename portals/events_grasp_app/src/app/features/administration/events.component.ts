import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { ApiService } from '../../core/api.service';

@Component({
  selector: 'app-admin-events',
  standalone: true,
  imports: [CommonModule, RouterModule],
  styles: [`
    .events-container {
      padding: 0;
    }
    .page-header {
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      padding: 2rem 2rem 4rem;
      color: white;
      margin: 0;
    }
    .header-content {
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .page-title {
      font-size: 1.75rem;
      font-weight: 700;
      margin-bottom: 0.25rem;
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }
    .page-subtitle {
      opacity: 0.9;
      font-size: 1rem;
    }
    .btn-new-event {
      background: white;
      color: #667eea;
      border: none;
      border-radius: 12px;
      padding: 0.75rem 1.5rem;
      font-size: 0.95rem;
      font-weight: 600;
      display: flex;
      align-items: center;
      gap: 0.5rem;
      text-decoration: none;
      transition: all 0.2s;
    }
    .btn-new-event:hover {
      transform: translateY(-2px);
      box-shadow: 0 5px 20px rgba(255,255,255,0.3);
      color: #667eea;
    }
    .content-area {
      padding: 0 2rem 2rem;
      margin-top: -2.5rem;
    }
    .events-card {
      background: white;
      border-radius: 16px;
      box-shadow: 0 4px 20px rgba(0,0,0,0.1);
      overflow: hidden;
    }
    .events-header {
      padding: 1.25rem 1.5rem;
      border-bottom: 1px solid #eee;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .events-count {
      font-weight: 600;
      color: #333;
      font-size: 1rem;
    }
    .events-count span {
      color: #667eea;
    }
    .loading-state, .error-state {
      padding: 3rem;
      text-align: center;
    }
    .loading-state {
      color: #888;
    }
    .error-state {
      color: #dc3545;
    }
    .empty-state {
      text-align: center;
      padding: 4rem 2rem;
      color: #888;
    }
    .empty-icon {
      font-size: 4rem;
      margin-bottom: 1rem;
      opacity: 0.5;
    }
    .empty-text {
      font-size: 1.2rem;
      margin-bottom: 0.5rem;
      color: #555;
    }
    .empty-hint {
      font-size: 0.95rem;
      color: #888;
      margin-bottom: 1.5rem;
    }
    .btn-create-first {
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      color: white;
      border: none;
      border-radius: 12px;
      padding: 0.75rem 1.5rem;
      font-size: 0.95rem;
      font-weight: 600;
      text-decoration: none;
      display: inline-flex;
      align-items: center;
      gap: 0.5rem;
      transition: all 0.2s;
    }
    .btn-create-first:hover {
      transform: translateY(-2px);
      box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4);
      color: white;
    }
    .events-list {
      list-style: none;
      margin: 0;
      padding: 0;
    }
    .event-item {
      display: flex;
      align-items: center;
      padding: 1rem 1.5rem;
      border-bottom: 1px solid #f0f0f0;
      text-decoration: none;
      color: inherit;
      transition: all 0.2s;
    }
    .event-item:last-child {
      border-bottom: none;
    }
    .event-item:hover {
      background: linear-gradient(135deg, rgba(102,126,234,0.03) 0%, rgba(118,75,162,0.03) 100%);
    }
    .event-icon {
      width: 48px;
      height: 48px;
      border-radius: 12px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 1.5rem;
      background: linear-gradient(135deg, rgba(102,126,234,0.1), rgba(118,75,162,0.1));
      margin-right: 1rem;
      flex-shrink: 0;
    }
    .event-info {
      flex: 1;
      min-width: 0;
    }
    .event-name {
      font-weight: 600;
      color: #333;
      font-size: 1rem;
      margin-bottom: 0.25rem;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }
    .event-meta {
      display: flex;
      flex-wrap: wrap;
      gap: 1rem;
      font-size: 0.85rem;
      color: #888;
    }
    .event-meta-item {
      display: flex;
      align-items: center;
      gap: 0.25rem;
    }
    .event-status {
      padding: 0.3rem 0.75rem;
      border-radius: 20px;
      font-size: 0.75rem;
      font-weight: 600;
      margin-left: auto;
    }
    .status-active {
      background: #d4edda;
      color: #155724;
    }
    .status-inactive {
      background: #f8d7da;
      color: #721c24;
    }
    .event-arrow {
      color: #ccc;
      font-size: 1.25rem;
      margin-left: 1rem;
    }
  `],
  template: `
    <div class="events-container">
      <!-- Header -->
      <div class="page-header">
        <div class="header-content">
          <div>
            <div class="page-title">
              <span>📄</span>
              Events
            </div>
            <p class="page-subtitle">Manage your scraped events and their configurations</p>
          </div>
          <a class="btn-new-event" routerLink="/administration/events/new">
            <span>➕</span>
            New Event
          </a>
        </div>
      </div>

      <div class="content-area">
        <div class="events-card">
          <!-- Header with count -->
          <div class="events-header" *ngIf="!loading && events.length > 0">
            <div class="events-count">
              Showing <span>{{ events.length }}</span> event{{ events.length !== 1 ? 's' : '' }}
            </div>
          </div>

          <!-- Loading State -->
          <div class="loading-state" *ngIf="loading">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">⏳</div>
            Loading events...
          </div>

          <!-- Error State -->
          <div class="error-state" *ngIf="error">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">⚠️</div>
            {{ error }}
          </div>

          <!-- Empty State -->
          <div class="empty-state" *ngIf="!loading && !error && events.length === 0">
            <div class="empty-icon">📄</div>
            <div class="empty-text">No events yet</div>
            <div class="empty-hint">Create your first event to start scraping and indexing content</div>
            <a class="btn-create-first" routerLink="/administration/events/new">
              <span>🚀</span>
              Create Your First Event
            </a>
          </div>

          <!-- Events List -->
          <ul class="events-list" *ngIf="!loading && !error && events.length > 0">
            <a *ngFor="let event of events"
               class="event-item"
               [routerLink]="['/administration/events', event.event_id]">
              <div class="event-icon">📄</div>
              <div class="event-info">
                <div class="event-name">{{ event.event_name }}</div>
                <div class="event-meta">
                  <span class="event-meta-item" *ngIf="event.source_url">
                    <span>🔗</span>
                    {{ truncateUrl(event.source_url) }}
                  </span>
                  <span class="event-meta-item" *ngIf="event.source_location_type">
                    <span>📍</span>
                    {{ formatSourceType(event.source_location_type) }}
                  </span>
                  <span class="event-meta-item" *ngIf="event.created_at">
                    <span>📅</span>
                    {{ formatDate(event.created_at) }}
                  </span>
                </div>
              </div>
              <span class="event-status" [ngClass]="event.is_active ? 'status-active' : 'status-inactive'">
                {{ event.is_active ? 'Active' : 'Inactive' }}
              </span>
              <span class="event-arrow">→</span>
            </a>
          </ul>
        </div>
      </div>
    </div>
  `
})
export class AdminEventsComponent implements OnInit {
  events: any[] = [];
  loading = false;
  error: string | null = null;

  constructor(private api: ApiService) {}

  ngOnInit() {
    this.load();
  }

  async load() {
    this.loading = true;
    this.error = null;
    try {
      const res = await this.api.getEvents();
      this.events = Array.isArray(res) ? res : [];
    } catch (err: any) {
      console.error(err);
      this.error = err?.message || 'Failed to load events';
    } finally {
      this.loading = false;
    }
  }

  truncateUrl(url: string): string {
    if (!url) return '';
    try {
      const urlObj = new URL(url);
      return urlObj.hostname + (urlObj.pathname !== '/' ? urlObj.pathname.slice(0, 20) + '...' : '');
    } catch {
      return url.length > 40 ? url.slice(0, 40) + '...' : url;
    }
  }

  formatSourceType(type: string): string {
    switch (type) {
      case 'http_url': return 'Web URL';
      case 'local_folder': return 'Local Folder';
      case 'aws_s3': return 'AWS S3';
      default: return type;
    }
  }

  formatDate(dateStr: string): string {
    if (!dateStr) return '';
    try {
      const date = new Date(dateStr);
      return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
    } catch {
      return dateStr;
    }
  }
}
