import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, RouterModule } from '@angular/router';
import { ApiService } from '../../core/api.service';
import { EventProvidersComponent } from './event-providers.component';

@Component({
  selector: 'app-event-detail',
  standalone: true,
  imports: [CommonModule, RouterModule, EventProvidersComponent],
  template: `
    <div class="container py-3">
      <a class="btn btn-sm btn-link mb-3" routerLink="/administration/events">← Back to Events</a>

      <div *ngIf="loading" class="text-muted">Loading event...</div>
      <div *ngIf="error" class="text-danger">{{ error }}</div>

      <div *ngIf="!loading">
        <h3>Event: {{ title }}</h3>
        <p class="text-muted">Source URL: <a [href]="sourceUrl" target="_blank">{{ sourceUrl }}</a></p>

        <div class="mt-3 mb-3">
          <button class="btn btn-outline-primary me-2" (click)="runScraper()" [disabled]="scrapeRunning">Run Scraper</button>
          <button class="btn btn-outline-success me-2" (click)="createVectorStore()" [disabled]="vectorRunning">Create Vector Store</button>
          <button class="btn btn-outline-secondary me-2" (click)="toggleProviders()">Setup Providers</button>
          <button class="btn btn-warning" (click)="publish()" [disabled]="publishing">Publish Scraper Data To Event Stores</button>
        </div>

        <div *ngIf="publishResults">
          <h6>Publish results:</h6>
          <ul>
            <li *ngFor="let r of publishResults">Provider {{ r.provider_id }} — {{ r.status }} — {{ r.message }}</li>
          </ul>
        </div>

        <div *ngIf="showProviders">
          <app-event-providers [eventId]="eventId"></app-event-providers>
        </div>

        <h5 class="mt-4">Vector Stores</h5>
        <div class="list-group mb-4">
          <div *ngFor="let vs of vectorStores" class="list-group-item">{{ vs.name }} — {{ vs.provider }} — <span class="badge bg-success">{{ vs.status }}</span></div>
        </div>

        <h5>Scraping Logs</h5>
        <p class="text-muted">No logs yet.</p>
      </div>

    </div>
  `
})
export class EventDetailComponent {
  title = 'Event';
  sourceUrl = '';
  loading = false;
  error: string | null = null;
  scrapeRunning = false;
  vectorRunning = false;
  vectorStores: any[] = [];
  eventId: number | null = null;
  showProviders = false;
  publishing = false;
  publishResults: any[] | null = null;

  constructor(route: ActivatedRoute, private api: ApiService) {
    const id = route.snapshot.paramMap.get('id');
    if (id) {
      this.eventId = Number(id);
      this.load(this.eventId);
    }
  }

  toggleProviders() {
    this.showProviders = !this.showProviders;
  }

  async load(id: number) {
    this.loading = true;
    this.error = null;
    try {
      const res = await this.api.getEvent(id);
      this.title = res.event_name;
      this.sourceUrl = res.source_url;
      // placeholder for vector stores if backend returns them
      this.vectorStores = res.vector_stores || [];
    } catch (err: any) {
      console.error(err);
      this.error = err?.message || 'Failed to load event';
    } finally {
      this.loading = false;
    }
  }

  async runScraper() {
    this.scrapeRunning = true;
    try {
      await this.api.postScrape({ refresh: true });
      // ideally refresh logs or show a toast
    } catch (e) {
      console.error(e);
    } finally {
      this.scrapeRunning = false;
    }
  }

  async createVectorStore() {
    this.vectorRunning = true;
    try {
      await this.api.postVectorCreate({});
    } catch (e) {
      console.error(e);
    } finally {
      this.vectorRunning = false;
    }
  }

  async publish() {
    if (!this.eventId) return;
    this.publishing = true;
    this.publishResults = null;
    try {
      const res = await this.api.publishEvent(this.eventId);
      this.publishResults = Array.isArray(res) ? res : [];
    } catch (e: any) {
      console.error(e);
      this.publishResults = [{ provider_id: 0, status: 'error', message: e?.message || 'failed' }];
    } finally {
      this.publishing = false;
    }
  }
}
