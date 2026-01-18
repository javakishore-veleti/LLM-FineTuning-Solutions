import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-settings',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="container py-4">
      <h4>Settings</h4>
      <p class="text-muted">Application-wide settings and API keys management (placeholder).</p>
    </div>
  `
})
export class SettingsComponent {}
