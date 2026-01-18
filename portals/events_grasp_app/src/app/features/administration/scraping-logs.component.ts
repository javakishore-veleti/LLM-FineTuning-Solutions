import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ApiService, EventSummary, ScrapingLog, ScrapedFile } from '../../core/api.service';

@Component({
  selector: 'app-admin-scraping-logs',
  standalone: true,
  imports: [CommonModule, FormsModule],
  styles: [`
    .scraping-container {
      padding: 0;
    }
    .page-header {
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      padding: 2rem 2rem 4rem;
      color: white;
      margin: 0;
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
    .content-area {
      padding: 0 2rem 2rem;
      margin-top: -2.5rem;
    }
    .selector-card {
      background: white;
      border-radius: 16px;
      padding: 1.5rem;
      box-shadow: 0 4px 20px rgba(0,0,0,0.1);
      margin-bottom: 1.5rem;
    }
    .selector-label {
      font-weight: 600;
      color: #333;
      margin-bottom: 0.75rem;
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }
    .event-select {
      width: 100%;
      padding: 0.875rem 1rem;
      border: 2px solid #e8e8e8;
      border-radius: 12px;
      font-size: 1rem;
      background: #fafafa;
      cursor: pointer;
      transition: all 0.2s;
    }
    .event-select:focus {
      border-color: #667eea;
      background: white;
      outline: none;
      box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.1);
    }
    .event-stats {
      display: flex;
      gap: 2rem;
      margin-top: 1rem;
      padding-top: 1rem;
      border-top: 1px solid #eee;
    }
    .stat-item {
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }
    .stat-icon {
      width: 36px;
      height: 36px;
      border-radius: 10px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 1rem;
    }
    .stat-icon.scrapes { background: linear-gradient(135deg, rgba(102,126,234,0.15), rgba(118,75,162,0.15)); }
    .stat-icon.files { background: linear-gradient(135deg, rgba(17,153,142,0.15), rgba(56,239,125,0.15)); }
    .stat-icon.date { background: linear-gradient(135deg, rgba(255,153,102,0.15), rgba(255,94,98,0.15)); }
    .stat-value {
      font-weight: 700;
      color: #333;
      font-size: 1.1rem;
    }
    .stat-label {
      font-size: 0.8rem;
      color: #888;
    }
    .tabs-container {
      background: white;
      border-radius: 16px;
      box-shadow: 0 4px 20px rgba(0,0,0,0.1);
      overflow: hidden;
    }
    .tabs-header {
      display: flex;
      border-bottom: 1px solid #eee;
    }
    .tab-btn {
      flex: 1;
      padding: 1rem 1.5rem;
      border: none;
      background: none;
      font-size: 0.95rem;
      font-weight: 500;
      color: #666;
      cursor: pointer;
      transition: all 0.2s;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 0.5rem;
    }
    .tab-btn:hover {
      background: #f5f7fb;
    }
    .tab-btn.active {
      color: #667eea;
      background: linear-gradient(135deg, rgba(102,126,234,0.05) 0%, rgba(118,75,162,0.05) 100%);
      border-bottom: 3px solid #667eea;
    }
    .tab-content {
      padding: 1.5rem;
    }
    .empty-state {
      text-align: center;
      padding: 3rem;
      color: #888;
    }
    .empty-icon {
      font-size: 3rem;
      margin-bottom: 1rem;
      opacity: 0.5;
    }
    .empty-text {
      font-size: 1.1rem;
      margin-bottom: 0.5rem;
    }
    .empty-hint {
      font-size: 0.9rem;
      color: #aaa;
    }
    /* Files Grid */
    .files-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
      gap: 1rem;
    }
    .file-card {
      background: #fafafa;
      border-radius: 12px;
      padding: 1rem;
      border: 1px solid #e8e8e8;
      transition: all 0.2s;
    }
    .file-card:hover {
      border-color: #667eea;
      box-shadow: 0 4px 15px rgba(102, 126, 234, 0.1);
    }
    .file-icon {
      width: 40px;
      height: 40px;
      border-radius: 10px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 1.25rem;
      background: linear-gradient(135deg, #667eea, #764ba2);
      margin-bottom: 0.75rem;
    }
    .file-name {
      font-weight: 600;
      color: #333;
      font-size: 0.9rem;
      word-break: break-all;
      margin-bottom: 0.5rem;
    }
    .file-meta {
      display: flex;
      flex-wrap: wrap;
      gap: 0.5rem;
      font-size: 0.8rem;
      color: #888;
    }
    .file-badge {
      padding: 0.2rem 0.5rem;
      border-radius: 6px;
      font-size: 0.7rem;
      font-weight: 500;
    }
    .badge-uploaded { background: #d4edda; color: #155724; }
    .badge-pending { background: #fff3cd; color: #856404; }
    /* Logs Timeline */
    .logs-timeline {
      position: relative;
    }
    .log-item {
      display: flex;
      gap: 1rem;
      padding: 1rem 0;
      border-bottom: 1px solid #eee;
    }
    .log-item:last-child {
      border-bottom: none;
    }
    .log-status-icon {
      width: 44px;
      height: 44px;
      border-radius: 12px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 1.25rem;
      flex-shrink: 0;
    }
    .log-status-icon.completed { background: linear-gradient(135deg, rgba(17,153,142,0.15), rgba(56,239,125,0.15)); }
    .log-status-icon.in_progress { background: linear-gradient(135deg, rgba(79,172,254,0.15), rgba(0,242,254,0.15)); }
    .log-status-icon.failed { background: linear-gradient(135deg, rgba(255,94,98,0.15), rgba(255,153,102,0.15)); }
    .log-content {
      flex: 1;
    }
    .log-header {
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      margin-bottom: 0.5rem;
    }
    .log-date {
      font-weight: 600;
      color: #333;
    }
    .log-status-badge {
      padding: 0.25rem 0.75rem;
      border-radius: 20px;
      font-size: 0.75rem;
      font-weight: 600;
    }
    .status-completed { background: #d4edda; color: #155724; }
    .status-in_progress { background: #cce5ff; color: #004085; }
    .status-failed { background: #f8d7da; color: #721c24; }
    .log-details {
      display: flex;
      flex-wrap: wrap;
      gap: 1rem;
      font-size: 0.85rem;
      color: #666;
    }
    .log-detail {
      display: flex;
      align-items: center;
      gap: 0.25rem;
    }
    .log-error {
      margin-top: 0.5rem;
      padding: 0.5rem;
      background: #f8d7da;
      border-radius: 6px;
      color: #721c24;
      font-size: 0.85rem;
    }
    .loading-spinner {
      text-align: center;
      padding: 2rem;
      color: #888;
    }
  `],
  template: `
    <div class="scraping-container">
      <!-- Header -->
      <div class="page-header">
        <div class="page-title">
          <span>🔍</span>
          Scraping Results
        </div>
        <p class="page-subtitle">View scraped files and execution history for your events</p>
      </div>

      <div class="content-area">
        <!-- Event Selector -->
        <div class="selector-card">
          <label class="selector-label">
            <span>📄</span>
            Select an Event
          </label>
          <select
            class="event-select"
            [(ngModel)]="selectedEventId"
            (change)="onEventChange()">
            <option [ngValue]="null">-- Choose an event to view scraping results --</option>
            <option *ngFor="let event of events" [ngValue]="event.event_id">
              {{ event.event_name }}
            </option>
          </select>

          <!-- Event Stats -->
          <div class="event-stats" *ngIf="selectedEvent">
            <div class="stat-item">
              <div class="stat-icon scrapes">🔄</div>
              <div>
                <div class="stat-value">{{ selectedEvent.total_scrapes }}</div>
                <div class="stat-label">Total Scrapes</div>
              </div>
            </div>
            <div class="stat-item">
              <div class="stat-icon files">📁</div>
              <div>
                <div class="stat-value">{{ selectedEvent.total_files }}</div>
                <div class="stat-label">Files Generated</div>
              </div>
            </div>
            <div class="stat-item" *ngIf="selectedEvent.last_scrape_date">
              <div class="stat-icon date">📅</div>
              <div>
                <div class="stat-value">{{ formatDate(selectedEvent.last_scrape_date) }}</div>
                <div class="stat-label">Last Scrape</div>
              </div>
            </div>
          </div>
        </div>

        <!-- Tabs Section -->
        <div class="tabs-container" *ngIf="selectedEventId">
          <div class="tabs-header">
            <button
              class="tab-btn"
              [class.active]="activeTab === 'files'"
              (click)="activeTab = 'files'">
              <span>📁</span>
              Scraped Files
              <span *ngIf="scrapedFiles.length">({{ scrapedFiles.length }})</span>
            </button>
            <button
              class="tab-btn"
              [class.active]="activeTab === 'history'"
              (click)="activeTab = 'history'">
              <span>📋</span>
              Execution History
              <span *ngIf="scrapingLogs.length">({{ scrapingLogs.length }})</span>
            </button>
          </div>

          <div class="tab-content">
            <!-- Loading State -->
            <div class="loading-spinner" *ngIf="loading">
              ⏳ Loading...
            </div>

            <!-- Files Tab -->
            <div *ngIf="!loading && activeTab === 'files'">
              <div class="empty-state" *ngIf="scrapedFiles.length === 0">
                <div class="empty-icon">📁</div>
                <div class="empty-text">No files scraped yet</div>
                <div class="empty-hint">Run the scraper on this event to generate files</div>
              </div>

              <div class="files-grid" *ngIf="scrapedFiles.length > 0">
                <div class="file-card" *ngFor="let file of scrapedFiles">
                  <div class="file-icon">📄</div>
                  <div class="file-name">{{ file.file_display_name || file.file_name }}</div>
                  <div class="file-meta">
                    <span *ngIf="file.file_size_display">{{ file.file_size_display }}</span>
                    <span class="file-badge" [ngClass]="file.uploaded_flag ? 'badge-uploaded' : 'badge-pending'">
                      {{ file.uploaded_flag ? 'Indexed' : 'Pending' }}
                    </span>
                  </div>
                </div>
              </div>
            </div>

            <!-- History Tab -->
            <div *ngIf="!loading && activeTab === 'history'">
              <div class="empty-state" *ngIf="scrapingLogs.length === 0">
                <div class="empty-icon">📋</div>
                <div class="empty-text">No scraping history</div>
                <div class="empty-hint">Scraping executions will appear here</div>
              </div>

              <div class="logs-timeline" *ngIf="scrapingLogs.length > 0">
                <div class="log-item" *ngFor="let log of scrapingLogs">
                  <div class="log-status-icon" [ngClass]="log.status">
                    {{ getStatusIcon(log.status) }}
                  </div>
                  <div class="log-content">
                    <div class="log-header">
                      <div class="log-date">{{ formatDateTime(log.start_time) }}</div>
                      <span class="log-status-badge" [ngClass]="'status-' + log.status">
                        {{ formatStatus(log.status) }}
                      </span>
                    </div>
                    <div class="log-details">
                      <div class="log-detail">
                        <span>📁</span>
                        <span>{{ log.files_scraped }} files</span>
                      </div>
                      <div class="log-detail" *ngIf="log.duration">
                        <span>⏱️</span>
                        <span>{{ log.duration }}</span>
                      </div>
                      <div class="log-detail">
                        <span>📍</span>
                        <span>{{ log.source_location_type }}</span>
                      </div>
                    </div>
                    <div class="log-error" *ngIf="log.error_message">
                      ⚠️ {{ log.error_message }}
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- No Event Selected -->
        <div class="tabs-container" *ngIf="!selectedEventId && !loadingEvents">
          <div class="tab-content">
            <div class="empty-state">
              <div class="empty-icon">👆</div>
              <div class="empty-text">Select an event to view its scraping results</div>
              <div class="empty-hint">Choose from the dropdown above to see scraped files and execution history</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  `
})
export class AdminScrapingLogsComponent implements OnInit {
  events: EventSummary[] = [];
  selectedEventId: number | null = null;
  selectedEvent: EventSummary | null = null;

  scrapedFiles: ScrapedFile[] = [];
  scrapingLogs: ScrapingLog[] = [];

  activeTab: 'files' | 'history' = 'files';
  loading = false;
  loadingEvents = true;

  constructor(private api: ApiService) {}

  async ngOnInit() {
    await this.loadEvents();
  }

  async loadEvents() {
    this.loadingEvents = true;
    try {
      const response = await this.api.getEventsWithScrapingSummary();
      if (response.success && response.events) {
        this.events = response.events;
      }
    } catch (error) {
      console.error('Failed to load events', error);
    } finally {
      this.loadingEvents = false;
    }
  }

  async onEventChange() {
    if (!this.selectedEventId) {
      this.selectedEvent = null;
      this.scrapedFiles = [];
      this.scrapingLogs = [];
      return;
    }

    this.selectedEvent = this.events.find(e => e.event_id === this.selectedEventId) || null;
    await this.loadEventData();
  }

  async loadEventData() {
    if (!this.selectedEventId) return;

    this.loading = true;
    try {
      const [filesResponse, logsResponse] = await Promise.all([
        this.api.getScrapedFilesForEvent(this.selectedEventId),
        this.api.getScrapingLogsForEvent(this.selectedEventId)
      ]);

      if (filesResponse.success && filesResponse.scraped_files) {
        this.scrapedFiles = filesResponse.scraped_files;
      }

      if (logsResponse.success && logsResponse.scraping_logs) {
        this.scrapingLogs = logsResponse.scraping_logs;
      }
    } catch (error) {
      console.error('Failed to load event data', error);
    } finally {
      this.loading = false;
    }
  }

  formatDate(dateStr: string | undefined): string {
    if (!dateStr) return 'N/A';
    try {
      const date = new Date(dateStr);
      return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
    } catch {
      return dateStr;
    }
  }

  formatDateTime(dateStr: string | undefined): string {
    if (!dateStr) return 'N/A';
    try {
      const date = new Date(dateStr);
      return date.toLocaleString('en-US', {
        month: 'short',
        day: 'numeric',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      });
    } catch {
      return dateStr;
    }
  }

  formatStatus(status: string): string {
    switch (status) {
      case 'completed': return 'Completed';
      case 'in_progress': return 'In Progress';
      case 'failed': return 'Failed';
      default: return status;
    }
  }

  getStatusIcon(status: string): string {
    switch (status) {
      case 'completed': return '✅';
      case 'in_progress': return '⏳';
      case 'failed': return '❌';
      default: return '📋';
    }
  }
}
