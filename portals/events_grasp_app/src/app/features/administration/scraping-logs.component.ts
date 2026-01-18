import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-admin-scraping-logs',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div>
      <h4>Scraping Logs</h4>
      <p class="text-muted">No logs yet. Run a scrape from the Home page or Events detail.</p>
    </div>
  `
})
export class AdminScrapingLogsComponent {}
