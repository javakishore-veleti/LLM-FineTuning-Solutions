import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormBuilder, Validators, FormGroup } from '@angular/forms';
import { Router, RouterModule } from '@angular/router';
import { ApiService } from '../../core/api.service';

@Component({
  selector: 'app-event-create',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, RouterModule],
  template: `
    <div class="container py-3">
      <div class="card shadow-sm">
        <div class="card-body">
          <div class="d-flex align-items-center mb-3">
            <i class="bi bi-calendar-plus-fill fs-3 text-primary me-2"></i>
            <div>
              <h3 class="mb-0">Create Event</h3>
              <small class="text-muted">Define the source and settings for a new event.</small>
            </div>
          </div>

          <form [formGroup]="form" (ngSubmit)="onSubmit()" novalidate>
            <div class="mb-3">
              <label class="form-label">Event Name</label>
              <div class="input-group">
                <span class="input-group-text form-icon"><i class="bi bi-card-heading"></i></span>
                <input class="form-control" formControlName="event_name" placeholder="e.g. AWS re:Invent 2025" />
              </div>
              <div *ngIf="f['event_name'].touched && f['event_name'].invalid" class="text-danger small mt-1">
                Event name is required.
              </div>
            </div>

            <div class="mb-3">
              <label class="form-label">Description</label>
              <div class="input-group">
                <span class="input-group-text form-icon"><i class="bi bi-card-text"></i></span>
                <textarea class="form-control" rows="3" formControlName="event_description" placeholder="Short summary"></textarea>
              </div>
            </div>

            <div class="mb-3">
              <label class="form-label">Source URL / Location</label>
              <div class="input-group">
                <span class="input-group-text form-icon"><i class="bi bi-link-45deg"></i></span>
                <input class="form-control" formControlName="source_url" placeholder="https://... or /path/to/folder" />
              </div>
              <div *ngIf="f['source_url'].touched && f['source_url'].invalid" class="text-danger small mt-1">
                A valid URL or path is required.
              </div>
            </div>

            <div class="row">
              <div class="col-md-6 mb-3">
                <label class="form-label">Source Type</label>
                <div class="input-group">
                  <span class="input-group-text form-icon"><i class="bi bi-folder2-open"></i></span>
                  <select class="form-select" formControlName="source_location_type">
                    <option value="http_url">HTTP URL</option>
                    <option value="local_folder">Local Folder</option>
                    <option value="aws_s3">AWS S3</option>
                  </select>
                </div>
              </div>

              <div class="col-md-6 mb-3 d-flex align-items-center">
                <div class="form-check ms-2">
                  <input class="form-check-input" type="checkbox" formControlName="is_active" id="isActive" />
                  <label class="form-check-label d-flex align-items-center" for="isActive">
                    <i class="bi bi-toggle-on text-success me-2"></i> Active
                  </label>
                </div>
              </div>
            </div>

            <div class="d-flex gap-2">
              <button class="btn btn-primary" type="submit" [disabled]="submitting"><i class="bi bi-save me-1"></i> Create</button>
              <button class="btn btn-outline-secondary" type="button" (click)="cancel()" [disabled]="submitting">Cancel</button>
            </div>

            <div *ngIf="message" class="mt-3 alert" [ngClass]="messageClass">{{ message }}</div>
          </form>
        </div>
      </div>
    </div>
  `
})
export class EventCreateComponent {
  public form!: FormGroup;

  submitting = false;
  message: string | null = null;
  messageClass = 'alert-info';

  constructor(private fb: FormBuilder, private api: ApiService, private router: Router) {
    // initialize form after FormBuilder is available
    this.form = this.fb.group({
      event_name: ['', Validators.required],
      event_description: [''],
      source_url: ['', [Validators.required]],
      source_location_type: ['http_url', Validators.required],
      is_active: [true]
    });
  }

  // public getter for template access
  public get f() { return this.form.controls; }

  async onSubmit() {
    if (this.form.invalid) {
      (this.form as any).markAllAsTouched();
      return;
    }
    this.submitting = true;
    this.message = null;
    try {
      const payload = this.form.value;
      await this.api.postEvent(payload);
      this.message = 'Event created successfully.';
      this.messageClass = 'alert-success';
      // navigate back to events list after a short delay
      setTimeout(() => this.router.navigate(['/administration/events']), 800);
    } catch (err: any) {
      console.error(err);
      this.message = 'Failed to create event: ' + (err?.message || 'unknown');
      this.messageClass = 'alert-danger';
    } finally {
      this.submitting = false;
    }
  }

  cancel() {
    this.router.navigate(['/administration/events']);
  }
}
