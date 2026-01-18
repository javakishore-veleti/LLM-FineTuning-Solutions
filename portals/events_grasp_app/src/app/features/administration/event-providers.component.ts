import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ApiService } from '../../core/api.service';

@Component({
  selector: 'app-event-providers',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="card mb-3">
      <div class="card-body">
        <h6>Setup Providers for this Event</h6>
        <div *ngIf="loading" class="text-muted">Loading providers...</div>
        <div *ngIf="!loading">
          <div *ngFor="let p of providers" class="form-check">
            <input class="form-check-input" type="checkbox" [id]="'p-'+p.provider_id" [checked]="selectedIds.has(p.provider_id)" (change)="toggle(p)" />
            <label class="form-check-label" [for]="'p-'+p.provider_id">{{ p.display_name }} ({{ p.provider_type }})</label>
          </div>

          <div class="mt-2">
            <button class="btn btn-sm btn-primary" (click)="save()" [disabled]="saving">Save</button>
          </div>
        </div>
      </div>
    </div>
  `
})
export class EventProvidersComponent {
  @Input() eventId!: number | null;
  providers: any[] = [];
  selectedIds = new Set<number>();
  loading = false;
  saving = false;

  constructor(private api: ApiService) {}

  async ngOnInit() {
    await this.load();
  }

  async load() {
    if (!this.eventId) {
      // nothing to load for missing event
      this.providers = [];
      this.selectedIds = new Set<number>();
      return;
    }

    this.loading = true;
    try {
      const [all, assigned] = await Promise.all([this.api.getProviders(), this.api.listEventProviders(this.eventId)]);
      this.providers = Array.isArray(all) ? all : [];
      const assignedArr = Array.isArray(assigned) ? assigned : [];
      this.selectedIds = new Set(assignedArr.map((a: any) => a.provider_id));
    } catch (e) {
      console.error(e);
    } finally {
      this.loading = false;
    }
  }

  toggle(p: any) {
    if (this.selectedIds.has(p.provider_id)) {
      this.selectedIds.delete(p.provider_id);
    } else {
      this.selectedIds.add(p.provider_id);
    }
  }

  async save() {
    if (!this.eventId) return;
    this.saving = true;
    try {
      // remove all existing and re-add selected for simplicity
      const existing = await this.api.listEventProviders(this.eventId);
      for (const ex of existing) {
        await this.api.removeEventProvider(this.eventId, ex.id);
      }
      for (const pid of Array.from(this.selectedIds)) {
        await this.api.addProviderToEvent(this.eventId, { provider_id: pid });
      }
      await this.load();
    } catch (e) {
      console.error(e);
    } finally {
      this.saving = false;
    }
  }
}
