import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ApiService } from '../../core/api.service';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="container py-5">
      <div class="row align-items-center">
        <div class="col-lg-6">
          <!-- Removed redundant H1; header already shows the application name -->
          <p class="lead text-muted">A small control panel for scraping, indexing and exploring event content (RAG-ready).</p>

          <div class="d-flex gap-2 mt-4">
            <button class="btn btn-primary btn-lg" (click)="runScraper()" [disabled]="scrapeRunning">
              <span *ngIf="!scrapeRunning">Run Scraper</span>
              <span *ngIf="scrapeRunning">Running…</span>
            </button>

            <button class="btn btn-outline-secondary btn-lg" (click)="createVectorStore()" [disabled]="vectorRunning">
              <span *ngIf="!vectorRunning">Create/Update Vector DB</span>
              <span *ngIf="vectorRunning">Working…</span>
            </button>
          </div>

          <div class="mt-3">
            <div *ngIf="lastStatus" class="alert" [ngClass]="statusClass" role="alert">
              {{ lastStatus }}
            </div>
          </div>

        </div>

        <div class="col-lg-5 offset-lg-1">
          <div class="card shadow-sm">
            <div class="card-body">
              <h5 class="card-title">Latest Scraped Content</h5>
              <p class="card-text text-muted">No scrapes run yet. Use the Run Scraper button to fetch AWS re:Invent announcements and create a local dataset.</p>
              <a class="btn btn-sm btn-outline-primary" href="#">Open datasets folder</a>
            </div>
          </div>
        </div>
      </div>

      <hr class="my-5" />

      <div class="row">
        <div class="col-12">
          <h3>Getting started</h3>
          <p class="text-muted">Follow the README and first-time setup instructions to configure Python, OpenAI keys and AWS CLI profile before running scraping & indexing.</p>
        </div>
      </div>
    </div>
  `
})
export class HomeComponent {
  scrapeRunning = false;
  vectorRunning = false;
  lastStatus: string | null = null;
  statusClass = 'alert-info';

  constructor(private api: ApiService) {}

  async runScraper() {
    this.scrapeRunning = true;
    this.lastStatus = null;
    this.statusClass = 'alert-info';
    try {
      const res = await this.api.postScrape({ refresh: false });
      this.lastStatus = 'Scraper started successfully.';
      this.statusClass = 'alert-success';
      console.log('scrape response', res);
    } catch (e: any) {
      this.lastStatus = 'Failed to start scraper: ' + (e?.message || e?.body || 'unknown');
      this.statusClass = 'alert-danger';
      console.error(e);
    } finally {
      this.scrapeRunning = false;
    }
  }

  async createVectorStore() {
    this.vectorRunning = true;
    this.lastStatus = null;
    this.statusClass = 'alert-info';
    try {
      const res = await this.api.postVectorCreate({});
      this.lastStatus = 'Vector DB create/update requested.';
      this.statusClass = 'alert-success';
      console.log('vector create response', res);
    } catch (e: any) {
      this.lastStatus = 'Failed to create/update vector DB: ' + (e?.message || e?.body || 'unknown');
      this.statusClass = 'alert-danger';
      console.error(e);
    } finally {
      this.vectorRunning = false;
    }
  }
}
