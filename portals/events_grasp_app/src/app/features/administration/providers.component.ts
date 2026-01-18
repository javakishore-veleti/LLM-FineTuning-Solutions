import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormBuilder, Validators, FormGroup } from '@angular/forms';
import { ApiService } from '../../core/api.service';

@Component({
  selector: 'app-admin-providers',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  template: `
    <div class="container py-3">
      <div class="d-flex justify-content-between align-items-center mb-3">
        <h4>Vector Store Providers</h4>
      </div>

      <div class="card mb-3">
        <div class="card-body">
          <form [formGroup]="form" (ngSubmit)="create()" class="row g-2">
            <div class="col-md-3">
              <input class="form-control" formControlName="display_name" placeholder="Display name" />
            </div>
            <div class="col-md-3">
              <input class="form-control" formControlName="provider_type" placeholder="Provider type (openai, pinecone...)" />
            </div>
            <div class="col-md-4">
              <input class="form-control" formControlName="credentials_json" placeholder='Credentials JSON' />
            </div>
            <div class="col-md-2">
              <button class="btn btn-primary w-100" type="submit" [disabled]="submitting">Add Provider</button>
            </div>
          </form>
        </div>
      </div>

      <div *ngIf="loading" class="text-muted">Loading providers...</div>
      <div *ngIf="!loading" class="list-group">
        <div *ngFor="let p of providers" class="list-group-item d-flex justify-content-between align-items-center">
          <div>
            <strong>{{ p.display_name }}</strong> <small class="text-muted">({{ p.provider_type }})</small>
          </div>
          <div>
            <button class="btn btn-sm btn-outline-danger" (click)="delete(p.provider_id)">Delete</button>
          </div>
        </div>
      </div>
    </div>
  `
})
export class AdminProvidersComponent {
  providers: any[] = [];
  loading = false;
  submitting = false;

  form!: FormGroup;

  constructor(private api: ApiService, private fb: FormBuilder) {
    // initialize the form after FormBuilder is available
    this.form = this.fb.group({
      display_name: ['', Validators.required],
      provider_type: ['', Validators.required],
      credentials_json: ['']
    });
    this.load();
  }

  async load() {
    this.loading = true;
    try {
      const res = await this.api.getProviders();
      this.providers = Array.isArray(res) ? res : [];
    } catch (e) {
      console.error(e);
    } finally {
      this.loading = false;
    }
  }

  async create() {
    if (this.form.invalid) return;
    this.submitting = true;
    try {
      await this.api.createProvider(this.form.value);
      this.form.reset();
      this.load();
    } catch (e) {
      console.error(e);
    } finally {
      this.submitting = false;
    }
  }

  async delete(id: number) {
    if (!confirm('Delete provider?')) return;
    try {
      await this.api.deleteProvider(id);
      this.load();
    } catch (e) {
      console.error(e);
    }
  }
}
