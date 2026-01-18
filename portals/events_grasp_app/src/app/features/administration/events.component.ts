import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { ApiService } from '../../core/api.service';

@Component({
  selector: 'app-admin-events',
  standalone: true,
  imports: [CommonModule, RouterModule],
  template: `
    <div class="row">
      <div class="col-md-9">
        <div class="d-flex justify-content-between align-items-center mb-3">
          <h4 class="mb-0">Events</h4>
          <a class="btn btn-sm btn-primary" routerLink="/administration/events/new">+ New Event</a>
        </div>

        <div *ngIf="loading" class="text-muted">Loading events...</div>
        <div *ngIf="error" class="text-danger">{{ error }}</div>

        <div class="list-group" *ngIf="!loading">
          <a *ngFor="let e of events"
             class="list-group-item list-group-item-action"
             [routerLink]="['/administration/events', e.event_id]">
            {{ e.event_name }}
          </a>
        </div>
      </div>
    </div>
  `
})
export class AdminEventsComponent {
  events: any[] = [];
  loading = false;
  error: string | null = null;

  constructor(private api: ApiService) {
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
}
