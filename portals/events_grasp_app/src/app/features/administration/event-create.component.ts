import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormBuilder, Validators, FormGroup } from '@angular/forms';
import { Router, RouterModule } from '@angular/router';
import { ApiService } from '../../core/api.service';

@Component({
  selector: 'app-event-create',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, RouterModule],
  styles: [`
    .create-event-container {
      min-height: calc(100vh - 60px);
      background: #f5f7fb;
    }
    .page-header {
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      padding: 2.5rem 0;
      color: white;
      margin-bottom: -3rem;
    }
    .page-title {
      font-size: 2rem;
      font-weight: 700;
      margin-bottom: 0.5rem;
      display: flex;
      align-items: center;
      gap: 0.75rem;
    }
    .page-title-icon {
      font-size: 2.5rem;
    }
    .page-subtitle {
      font-size: 1.1rem;
      opacity: 0.9;
    }
    .form-card {
      background: white;
      border-radius: 20px;
      padding: 2.5rem;
      box-shadow: 0 10px 40px rgba(0,0,0,0.1);
      position: relative;
      z-index: 10;
      margin-bottom: 2rem;
    }
    .form-section {
      margin-bottom: 2rem;
    }
    .form-section-title {
      font-size: 1.1rem;
      font-weight: 600;
      color: #333;
      margin-bottom: 1rem;
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }
    .form-section-title .icon {
      width: 32px;
      height: 32px;
      border-radius: 8px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 1rem;
    }
    .form-section-title .icon.purple { background: linear-gradient(135deg, #667eea, #764ba2); }
    .form-section-title .icon.green { background: linear-gradient(135deg, #11998e, #38ef7d); }
    .form-section-title .icon.orange { background: linear-gradient(135deg, #ff9966, #ff5e62); }
    .form-section-title .icon.blue { background: linear-gradient(135deg, #4facfe, #00f2fe); }
    .modern-input {
      border: 2px solid #e8e8e8;
      border-radius: 12px;
      padding: 0.875rem 1rem;
      font-size: 1rem;
      transition: all 0.2s;
      background: #fafafa;
    }
    .modern-input:focus {
      border-color: #667eea;
      background: white;
      box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.1);
      outline: none;
    }
    .modern-input::placeholder {
      color: #aaa;
    }
    .modern-input.is-invalid {
      border-color: #dc3545;
    }
    .modern-textarea {
      min-height: 120px;
      resize: vertical;
    }
    .modern-select {
      cursor: pointer;
    }
    .input-label {
      font-weight: 500;
      color: #555;
      margin-bottom: 0.5rem;
      font-size: 0.95rem;
    }
    .input-hint {
      font-size: 0.8rem;
      color: #888;
      margin-top: 0.35rem;
    }
    .error-text {
      color: #dc3545;
      font-size: 0.8rem;
      margin-top: 0.35rem;
      display: flex;
      align-items: center;
      gap: 0.25rem;
    }
    .source-type-cards {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 1rem;
    }
    .source-type-card {
      border: 2px solid #e8e8e8;
      border-radius: 12px;
      padding: 1.25rem;
      text-align: center;
      cursor: pointer;
      transition: all 0.2s;
      background: #fafafa;
    }
    .source-type-card:hover {
      border-color: #667eea;
      background: white;
    }
    .source-type-card.selected {
      border-color: #667eea;
      background: linear-gradient(135deg, rgba(102,126,234,0.05) 0%, rgba(118,75,162,0.05) 100%);
      box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.1);
    }
    .source-type-icon {
      font-size: 2rem;
      margin-bottom: 0.5rem;
    }
    .source-type-name {
      font-weight: 600;
      color: #333;
      font-size: 0.95rem;
    }
    .source-type-desc {
      font-size: 0.75rem;
      color: #888;
      margin-top: 0.25rem;
    }
    .toggle-switch {
      display: flex;
      align-items: center;
      gap: 0.75rem;
      padding: 1rem 1.25rem;
      background: #fafafa;
      border-radius: 12px;
      border: 2px solid #e8e8e8;
      cursor: pointer;
      transition: all 0.2s;
    }
    .toggle-switch:hover {
      border-color: #667eea;
    }
    .toggle-switch.active {
      background: linear-gradient(135deg, rgba(17,153,142,0.1) 0%, rgba(56,239,125,0.1) 100%);
      border-color: #11998e;
    }
    .toggle-icon {
      font-size: 1.5rem;
    }
    .toggle-text {
      font-weight: 500;
      color: #333;
    }
    .toggle-desc {
      font-size: 0.8rem;
      color: #888;
    }
    .action-buttons {
      display: flex;
      gap: 1rem;
      margin-top: 2rem;
      padding-top: 2rem;
      border-top: 1px solid #eee;
    }
    .btn-create {
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      border: none;
      border-radius: 12px;
      padding: 0.875rem 2rem;
      font-size: 1rem;
      font-weight: 600;
      color: white;
      display: flex;
      align-items: center;
      gap: 0.5rem;
      transition: all 0.2s;
      cursor: pointer;
    }
    .btn-create:hover:not(:disabled) {
      transform: translateY(-2px);
      box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
    }
    .btn-create:disabled {
      opacity: 0.6;
      cursor: not-allowed;
    }
    .btn-cancel {
      background: white;
      border: 2px solid #e8e8e8;
      border-radius: 12px;
      padding: 0.875rem 1.5rem;
      font-size: 1rem;
      font-weight: 500;
      color: #666;
      display: flex;
      align-items: center;
      gap: 0.5rem;
      transition: all 0.2s;
      cursor: pointer;
    }
    .btn-cancel:hover:not(:disabled) {
      border-color: #ccc;
      background: #f5f5f5;
    }
    .alert-modern {
      border-radius: 12px;
      padding: 1rem 1.25rem;
      display: flex;
      align-items: center;
      gap: 0.75rem;
      margin-top: 1.5rem;
    }
    .alert-modern.success {
      background: linear-gradient(135deg, rgba(17,153,142,0.1) 0%, rgba(56,239,125,0.1) 100%);
      border: 1px solid #11998e;
      color: #0d7377;
    }
    .alert-modern.error {
      background: rgba(220, 53, 69, 0.1);
      border: 1px solid #dc3545;
      color: #dc3545;
    }
    .tips-card {
      background: linear-gradient(135deg, rgba(102,126,234,0.08) 0%, rgba(118,75,162,0.08) 100%);
      border-radius: 16px;
      padding: 1.5rem;
      margin-top: 1.5rem;
      border: 1px dashed #667eea;
    }
    .tips-title {
      font-weight: 600;
      color: #667eea;
      margin-bottom: 0.75rem;
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }
    .tip-item {
      display: flex;
      align-items: flex-start;
      gap: 0.5rem;
      color: #555;
      font-size: 0.9rem;
      margin-bottom: 0.5rem;
    }
    .tip-item:last-child {
      margin-bottom: 0;
    }
    @media (max-width: 768px) {
      .source-type-cards {
        grid-template-columns: 1fr;
      }
      .action-buttons {
        flex-direction: column;
      }
    }
  `],
  template: `
    <div class="create-event-container">
      <!-- Header -->
      <div class="page-header">
        <div class="container">
          <div class="page-title">
            <span class="page-title-icon">🚀</span>
            Create New Event
          </div>
          <p class="page-subtitle">Set up a new event to scrape and index with AI-powered insights</p>
        </div>
      </div>

      <!-- Form Card -->
      <div class="container">
        <div class="form-card">
          <form [formGroup]="form" (ngSubmit)="onSubmit()" novalidate>

            <!-- Basic Info Section -->
            <div class="form-section">
              <div class="form-section-title">
                <span class="icon purple">📝</span>
                Basic Information
              </div>

              <div class="row">
                <div class="col-md-12 mb-3">
                  <label class="input-label">Event Name *</label>
                  <input
                    type="text"
                    class="modern-input w-100"
                    [class.is-invalid]="isFieldInvalid('event_name')"
                    formControlName="event_name"
                    placeholder="e.g. AWS re:Invent 2025, Google I/O Conference" />
                  <div class="input-hint">Give your event a descriptive name for easy identification</div>
                  <div *ngIf="isFieldInvalid('event_name')" class="error-text">
                    ⚠️ Event name is required
                  </div>
                </div>

                <div class="col-md-12 mb-3">
                  <label class="input-label">Description</label>
                  <textarea
                    class="modern-input modern-textarea w-100"
                    formControlName="event_description"
                    placeholder="Brief description of the event, topics covered, key speakers, etc."></textarea>
                  <div class="input-hint">Optional: Add context to help identify this event later</div>
                </div>
              </div>
            </div>

            <!-- Source Configuration Section -->
            <div class="form-section">
              <div class="form-section-title">
                <span class="icon green">🔗</span>
                Source Configuration
              </div>

              <div class="mb-4">
                <label class="input-label">Source Type</label>
                <div class="source-type-cards">
                  <div
                    class="source-type-card"
                    [class.selected]="form.get('source_location_type')?.value === 'http_url'"
                    (click)="selectSourceType('http_url')">
                    <div class="source-type-icon">🌐</div>
                    <div class="source-type-name">HTTP URL</div>
                    <div class="source-type-desc">Web pages & APIs</div>
                  </div>
                  <div
                    class="source-type-card"
                    [class.selected]="form.get('source_location_type')?.value === 'local_folder'"
                    (click)="selectSourceType('local_folder')">
                    <div class="source-type-icon">📁</div>
                    <div class="source-type-name">Local Folder</div>
                    <div class="source-type-desc">Files on disk</div>
                  </div>
                  <div
                    class="source-type-card"
                    [class.selected]="form.get('source_location_type')?.value === 'aws_s3'"
                    (click)="selectSourceType('aws_s3')">
                    <div class="source-type-icon">☁️</div>
                    <div class="source-type-name">AWS S3</div>
                    <div class="source-type-desc">Cloud storage</div>
                  </div>
                </div>
              </div>

              <div class="mb-3">
                <label class="input-label">Source URL / Location *</label>
                <input
                  type="text"
                  class="modern-input w-100"
                  [class.is-invalid]="isFieldInvalid('source_url')"
                  formControlName="source_url"
                  [placeholder]="getSourcePlaceholder()" />
                <div class="input-hint">{{ getSourceHint() }}</div>
                <div *ngIf="isFieldInvalid('source_url')" class="error-text">
                  ⚠️ A valid URL or path is required
                </div>
              </div>
            </div>

            <!-- Settings Section -->
            <div class="form-section">
              <div class="form-section-title">
                <span class="icon blue">⚙️</span>
                Settings
              </div>

              <div
                class="toggle-switch"
                [class.active]="form.get('is_active')?.value"
                (click)="toggleActive()">
                <span class="toggle-icon">{{ form.get('is_active')?.value ? '✅' : '⭕' }}</span>
                <div>
                  <div class="toggle-text">{{ form.get('is_active')?.value ? 'Active' : 'Inactive' }}</div>
                  <div class="toggle-desc">{{ form.get('is_active')?.value ? 'Event will be processed immediately' : 'Event will be saved but not processed' }}</div>
                </div>
              </div>
            </div>

            <!-- Action Buttons -->
            <div class="action-buttons">
              <button class="btn-create" type="submit" [disabled]="submitting">
                <span>{{ submitting ? '⏳' : '🚀' }}</span>
                {{ submitting ? 'Creating...' : 'Create Event' }}
              </button>
              <button class="btn-cancel" type="button" (click)="cancel()" [disabled]="submitting">
                <span>←</span>
                Cancel
              </button>
            </div>

            <!-- Success/Error Messages -->
            <div *ngIf="message" class="alert-modern" [class.success]="messageClass === 'alert-success'" [class.error]="messageClass === 'alert-danger'">
              <span>{{ messageClass === 'alert-success' ? '✅' : '❌' }}</span>
              {{ message }}
            </div>
          </form>

          <!-- Tips Section -->
          <div class="tips-card">
            <div class="tips-title">
              <span>💡</span>
              Quick Tips
            </div>
            <div class="tip-item">
              <span>•</span>
              <span>For conference websites, use the main agenda or sessions page URL</span>
            </div>
            <div class="tip-item">
              <span>•</span>
              <span>The scraper will automatically discover and index linked pages</span>
            </div>
            <div class="tip-item">
              <span>•</span>
              <span>After creation, you can configure LLM providers and vector stores</span>
            </div>
          </div>
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
    this.form = this.fb.group({
      event_name: ['', Validators.required],
      event_description: [''],
      source_url: ['', [Validators.required]],
      source_location_type: ['http_url', Validators.required],
      is_active: [true]
    });
  }

  isFieldInvalid(fieldName: string): boolean {
    const control = this.form.get(fieldName);
    return !!(control && control.touched && control.invalid);
  }

  selectSourceType(type: string) {
    this.form.patchValue({ source_location_type: type });
  }

  toggleActive() {
    const current = this.form.get('is_active')?.value;
    this.form.patchValue({ is_active: !current });
  }

  getSourcePlaceholder(): string {
    const type = this.form.get('source_location_type')?.value;
    switch (type) {
      case 'http_url': return 'https://conference.example.com/agenda';
      case 'local_folder': return '/path/to/your/documents';
      case 'aws_s3': return 's3://bucket-name/path/to/files';
      default: return 'Enter source location';
    }
  }

  getSourceHint(): string {
    const type = this.form.get('source_location_type')?.value;
    switch (type) {
      case 'http_url': return 'Enter the URL of the webpage you want to scrape';
      case 'local_folder': return 'Enter the absolute path to the folder containing your files';
      case 'aws_s3': return 'Enter the S3 URI in the format s3://bucket/prefix';
      default: return '';
    }
  }

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
      this.message = 'Event created successfully! Redirecting...';
      this.messageClass = 'alert-success';
      setTimeout(() => this.router.navigate(['/administration/events']), 1200);
    } catch (err: any) {
      console.error(err);
      this.message = 'Failed to create event: ' + (err?.message || 'unknown error');
      this.messageClass = 'alert-danger';
    } finally {
      this.submitting = false;
    }
  }

  cancel() {
    this.router.navigate(['/administration/events']);
  }
}
