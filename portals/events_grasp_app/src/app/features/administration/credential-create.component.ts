import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router, RouterModule } from '@angular/router';
import { ApiService, CredentialProvider, AuthType, ProviderSchemaField } from '../../core/api.service';

@Component({
  selector: 'app-credential-create',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterModule],
  styles: [`
    .create-container {
      padding: 0;
    }
    .page-header {
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      padding: 2rem 2rem 4rem;
      color: white;
    }
    .header-content {
      display: flex;
      justify-content: space-between;
      align-items: center;
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
    .btn-back {
      background: rgba(255,255,255,0.2);
      color: white;
      border: none;
      border-radius: 10px;
      padding: 0.6rem 1.2rem;
      font-size: 0.9rem;
      cursor: pointer;
      text-decoration: none;
      display: flex;
      align-items: center;
      gap: 0.5rem;
      transition: all 0.2s;
    }
    .btn-back:hover {
      background: rgba(255,255,255,0.3);
      color: white;
    }
    .content-area {
      padding: 0 2rem 2rem;
      margin-top: -2.5rem;
    }
    .wizard-card {
      background: white;
      border-radius: 16px;
      box-shadow: 0 4px 20px rgba(0,0,0,0.1);
      overflow: hidden;
    }
    .wizard-steps {
      display: flex;
      border-bottom: 1px solid #eee;
      padding: 1.5rem;
      gap: 2rem;
    }
    .wizard-step {
      display: flex;
      align-items: center;
      gap: 0.75rem;
      color: #aaa;
    }
    .wizard-step.active {
      color: #667eea;
    }
    .wizard-step.completed {
      color: #28a745;
    }
    .step-number {
      width: 32px;
      height: 32px;
      border-radius: 50%;
      background: #eee;
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: 600;
      font-size: 0.9rem;
    }
    .wizard-step.active .step-number {
      background: linear-gradient(135deg, #667eea, #764ba2);
      color: white;
    }
    .wizard-step.completed .step-number {
      background: #28a745;
      color: white;
    }
    .step-label {
      font-weight: 500;
      font-size: 0.95rem;
    }
    .wizard-content {
      padding: 2rem;
    }
    .provider-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
      gap: 1rem;
    }
    .provider-card {
      border: 2px solid #e8e8e8;
      border-radius: 12px;
      padding: 1.25rem;
      cursor: pointer;
      transition: all 0.2s;
      text-align: center;
    }
    .provider-card:hover {
      border-color: #667eea;
      box-shadow: 0 4px 15px rgba(102, 126, 234, 0.15);
    }
    .provider-card.selected {
      border-color: #667eea;
      background: linear-gradient(135deg, rgba(102,126,234,0.05), rgba(118,75,162,0.05));
    }
    .provider-card.coming-soon {
      opacity: 0.5;
      cursor: not-allowed;
    }
    .provider-icon {
      width: 50px;
      height: 50px;
      border-radius: 12px;
      margin: 0 auto 0.75rem;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 1.5rem;
    }
    .provider-icon.aws { background: linear-gradient(135deg, #ff9900, #ff6600); color: white; }
    .provider-icon.azure { background: linear-gradient(135deg, #0078d4, #00bcf2); color: white; }
    .provider-icon.gcp { background: linear-gradient(135deg, #4285f4, #34a853); color: white; }
    .provider-icon.neo4j { background: linear-gradient(135deg, #018bff, #0056b3); color: white; }
    .provider-icon.mongodb { background: linear-gradient(135deg, #00684a, #13aa52); color: white; }
    .provider-icon.elasticsearch { background: linear-gradient(135deg, #fed10a, #00bfb3); }
    .provider-icon.redis { background: linear-gradient(135deg, #dc382d, #a41e11); color: white; }
    .provider-icon.postgresql { background: linear-gradient(135deg, #336791, #0064a5); color: white; }
    .provider-icon.pinecone { background: linear-gradient(135deg, #000000, #333333); color: white; }
    .provider-icon.custom { background: linear-gradient(135deg, #667eea, #764ba2); color: white; }
    .provider-name {
      font-weight: 600;
      color: #333;
      font-size: 0.9rem;
    }
    .provider-status {
      font-size: 0.7rem;
      color: #888;
      margin-top: 0.25rem;
    }

    /* Auth Type Selection */
    .auth-types {
      display: flex;
      flex-direction: column;
      gap: 0.75rem;
      max-width: 500px;
    }
    .auth-type-card {
      border: 2px solid #e8e8e8;
      border-radius: 10px;
      padding: 1rem;
      cursor: pointer;
      transition: all 0.2s;
    }
    .auth-type-card:hover {
      border-color: #667eea;
    }
    .auth-type-card.selected {
      border-color: #667eea;
      background: rgba(102,126,234,0.05);
    }
    .auth-type-label {
      font-weight: 600;
      color: #333;
      margin-bottom: 0.25rem;
    }
    .auth-type-desc {
      font-size: 0.85rem;
      color: #888;
    }

    /* Form Styles */
    .config-form {
      max-width: 600px;
    }
    .form-section {
      margin-bottom: 2rem;
    }
    .section-title {
      font-size: 1rem;
      font-weight: 600;
      color: #333;
      margin-bottom: 1rem;
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }
    .form-group {
      margin-bottom: 1.25rem;
    }
    .form-label {
      display: block;
      font-weight: 500;
      color: #444;
      margin-bottom: 0.35rem;
      font-size: 0.9rem;
    }
    .form-label .required {
      color: #dc3545;
    }
    .form-control {
      width: 100%;
      padding: 0.75rem 1rem;
      border: 1.5px solid #e0e0e0;
      border-radius: 10px;
      font-size: 0.95rem;
      transition: all 0.2s;
    }
    .form-control:focus {
      outline: none;
      border-color: #667eea;
      box-shadow: 0 0 0 3px rgba(102,126,234,0.15);
    }
    textarea.form-control {
      min-height: 120px;
      font-family: monospace;
      font-size: 0.85rem;
    }
    .form-hint {
      font-size: 0.8rem;
      color: #888;
      margin-top: 0.35rem;
    }

    /* Coming Soon */
    .coming-soon-container {
      text-align: center;
      padding: 4rem 2rem;
    }
    .coming-soon-icon {
      font-size: 5rem;
      margin-bottom: 1.5rem;
    }
    .coming-soon-title {
      font-size: 1.5rem;
      font-weight: 600;
      color: #333;
      margin-bottom: 0.75rem;
    }
    .coming-soon-message {
      font-size: 1rem;
      color: #666;
    }

    /* Actions */
    .wizard-actions {
      display: flex;
      justify-content: space-between;
      padding: 1.5rem 2rem;
      border-top: 1px solid #eee;
      background: #fafafa;
    }
    .btn-secondary {
      background: #f0f0f0;
      color: #666;
      border: none;
      border-radius: 10px;
      padding: 0.75rem 1.5rem;
      font-size: 0.95rem;
      font-weight: 500;
      cursor: pointer;
      transition: all 0.2s;
    }
    .btn-secondary:hover {
      background: #e0e0e0;
    }
    .btn-primary {
      background: linear-gradient(135deg, #667eea, #764ba2);
      color: white;
      border: none;
      border-radius: 10px;
      padding: 0.75rem 1.5rem;
      font-size: 0.95rem;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.2s;
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }
    .btn-primary:hover:not(:disabled) {
      transform: translateY(-2px);
      box-shadow: 0 5px 20px rgba(102,126,234,0.4);
    }
    .btn-primary:disabled {
      opacity: 0.6;
      cursor: not-allowed;
    }
    .loading-state {
      text-align: center;
      padding: 3rem;
      color: #888;
    }
  `],
  template: `
    <div class="create-container">
      <!-- Header -->
      <div class="page-header">
        <div class="header-content">
          <div>
            <div class="page-title">
              <span>🔐</span>
              Add Credential
            </div>
            <p class="page-subtitle">Configure credentials for your provider integrations</p>
          </div>
          <a class="btn-back" routerLink="/administration/credentials">
            <span>←</span>
            Back to Credentials
          </a>
        </div>
      </div>

      <div class="content-area">
        <div class="wizard-card">
          <!-- Wizard Steps -->
          <div class="wizard-steps">
            <div class="wizard-step" [class.active]="currentStep === 1" [class.completed]="currentStep > 1">
              <div class="step-number">{{ currentStep > 1 ? '✓' : '1' }}</div>
              <div class="step-label">Select Provider</div>
            </div>
            <div class="wizard-step" [class.active]="currentStep === 2" [class.completed]="currentStep > 2">
              <div class="step-number">{{ currentStep > 2 ? '✓' : '2' }}</div>
              <div class="step-label">Auth Type</div>
            </div>
            <div class="wizard-step" [class.active]="currentStep === 3">
              <div class="step-number">3</div>
              <div class="step-label">Configure</div>
            </div>
          </div>

          <!-- Loading -->
          <div class="loading-state" *ngIf="loading">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">⏳</div>
            Loading...
          </div>

          <!-- Step 1: Select Provider -->
          <div class="wizard-content" *ngIf="!loading && currentStep === 1">
            <div class="provider-grid">
              <div *ngFor="let provider of providers"
                   class="provider-card"
                   [class.selected]="selectedProvider?.provider_type === provider.provider_type"
                   [class.coming-soon]="provider.status === 'coming_soon'"
                   (click)="selectProvider(provider)">
                <div class="provider-icon" [ngClass]="provider.icon">
                  {{ getProviderEmoji(provider.icon) }}
                </div>
                <div class="provider-name">{{ provider.name }}</div>
                <div class="provider-status" *ngIf="provider.status === 'coming_soon'">Coming Soon</div>
              </div>
            </div>
          </div>

          <!-- Step 2: Auth Type -->
          <div class="wizard-content" *ngIf="!loading && currentStep === 2">
            <div class="section-title">
              <span>🔑</span>
              Select Authentication Type for {{ selectedProvider?.name }}
            </div>
            <div class="auth-types">
              <div *ngFor="let authType of authTypes"
                   class="auth-type-card"
                   [class.selected]="selectedAuthType?.value === authType.value"
                   (click)="selectAuthType(authType)">
                <div class="auth-type-label">{{ authType.label }}</div>
                <div class="auth-type-desc">{{ authType.description }}</div>
              </div>
            </div>
          </div>

          <!-- Step 3: Configure -->
          <div class="wizard-content" *ngIf="!loading && currentStep === 3">
            <div class="config-form">
              <div class="form-section">
                <div class="section-title">
                  <span>📝</span>
                  Credential Details
                </div>
                <div class="form-group">
                  <label class="form-label">
                    Credential Name <span class="required">*</span>
                  </label>
                  <input type="text" class="form-control"
                         [(ngModel)]="credentialName"
                         placeholder="My AWS Credentials">
                  <div class="form-hint">A friendly name to identify this credential</div>
                </div>
                <div class="form-group">
                  <label class="form-label">Description</label>
                  <input type="text" class="form-control"
                         [(ngModel)]="description"
                         placeholder="Optional description">
                </div>
              </div>

              <div class="form-section" *ngIf="schemaFields.length > 0">
                <div class="section-title">
                  <span>⚙️</span>
                  {{ selectedAuthType?.label }} Configuration
                </div>
                <div *ngFor="let field of schemaFields" class="form-group">
                  <label class="form-label">
                    {{ field.label }}
                    <span class="required" *ngIf="field.required">*</span>
                  </label>

                  <input *ngIf="field.type === 'text'"
                         type="text"
                         class="form-control"
                         [(ngModel)]="configValues[field.name]"
                         [placeholder]="field.placeholder || ''">

                  <input *ngIf="field.type === 'password'"
                         type="password"
                         class="form-control"
                         [(ngModel)]="configValues[field.name]"
                         [placeholder]="field.placeholder || ''">

                  <input *ngIf="field.type === 'number'"
                         type="number"
                         class="form-control"
                         [(ngModel)]="configValues[field.name]"
                         [placeholder]="field.placeholder || ''">

                  <select *ngIf="field.type === 'select'"
                          class="form-control"
                          [(ngModel)]="configValues[field.name]">
                    <option value="">Select...</option>
                    <option *ngFor="let opt of field.options" [value]="opt.value">
                      {{ opt.label }}
                    </option>
                  </select>

                  <textarea *ngIf="field.type === 'textarea'"
                            class="form-control"
                            [(ngModel)]="configValues[field.name]"
                            [placeholder]="field.placeholder || ''"></textarea>

                  <div *ngIf="field.type === 'checkbox'" style="display: flex; align-items: center; gap: 0.5rem;">
                    <input type="checkbox"
                           [(ngModel)]="configValues[field.name]"
                           [id]="'field-' + field.name">
                    <label [for]="'field-' + field.name" style="margin: 0; font-weight: normal;">
                      {{ field.description }}
                    </label>
                  </div>

                  <div class="form-hint" *ngIf="field.description && field.type !== 'checkbox'">
                    {{ field.description }}
                  </div>
                </div>
              </div>

              <div *ngIf="schemaFields.length === 0" style="text-align: center; padding: 2rem; color: #888;">
                <div style="font-size: 3rem; margin-bottom: 1rem;">✨</div>
                <div>No additional configuration required for this authentication type.</div>
                <div style="font-size: 0.9rem; margin-top: 0.5rem;">The system will use default credentials.</div>
              </div>
            </div>
          </div>

          <!-- Actions -->
          <div class="wizard-actions" *ngIf="!loading">
            <button class="btn-secondary"
                    *ngIf="currentStep > 1"
                    (click)="goToStep(currentStep - 1)">
              ← Back
            </button>
            <div *ngIf="currentStep === 1"></div>

            <button class="btn-primary"
                    *ngIf="currentStep === 1"
                    [disabled]="!selectedProvider || selectedProvider.status === 'coming_soon'"
                    (click)="goToStep(2)">
              Continue →
            </button>

            <button class="btn-primary"
                    *ngIf="currentStep === 2"
                    [disabled]="!selectedAuthType"
                    (click)="goToStep(3)">
              Continue →
            </button>

            <button class="btn-primary"
                    *ngIf="currentStep === 3"
                    [disabled]="!isFormValid() || creating"
                    (click)="createCredential()">
              <span *ngIf="!creating">🔐</span>
              <span *ngIf="creating">⏳</span>
              {{ creating ? 'Creating...' : 'Create Credential' }}
            </button>
          </div>
        </div>
      </div>
    </div>
  `
})
export class CredentialCreateComponent implements OnInit {
  loading = false;
  creating = false;
  currentStep = 1;

  providers: CredentialProvider[] = [];
  selectedProvider: CredentialProvider | null = null;
  authTypes: AuthType[] = [];
  selectedAuthType: AuthType | null = null;
  schemaFields: ProviderSchemaField[] = [];

  credentialName = '';
  description = '';
  configValues: { [key: string]: any } = {};

  constructor(
    private api: ApiService,
    private router: Router
  ) {}

  async ngOnInit() {
    await this.loadProviders();
  }

  async loadProviders() {
    this.loading = true;
    try {
      const resp = await this.api.getCredentialProviders();
      if (resp.success) {
        this.providers = resp.providers;
      }
    } catch (e) {
      console.error('Failed to load providers', e);
    } finally {
      this.loading = false;
    }
  }

  selectProvider(provider: CredentialProvider) {
    if (provider.status === 'coming_soon') return;
    this.selectedProvider = provider;
    this.authTypes = provider.auth_types || [];
    this.selectedAuthType = null;
  }

  selectAuthType(authType: AuthType) {
    this.selectedAuthType = authType;
  }

  async goToStep(step: number) {
    if (step === 3 && this.selectedProvider && this.selectedAuthType) {
      // Load schema for selected auth type
      this.loading = true;
      try {
        const resp = await this.api.getCredentialSchema(
          this.selectedProvider.provider_type,
          this.selectedAuthType.value
        );
        if (resp.success) {
          this.schemaFields = resp.schema.fields || [];
          this.initializeDefaults();
        }
      } catch (e) {
        console.error('Failed to load schema', e);
      } finally {
        this.loading = false;
      }
    }
    this.currentStep = step;
  }

  initializeDefaults() {
    for (const field of this.schemaFields) {
      if (field.default !== undefined && this.configValues[field.name] === undefined) {
        this.configValues[field.name] = field.default;
      }
    }
  }

  isFormValid(): boolean {
    if (!this.credentialName?.trim()) return false;

    for (const field of this.schemaFields) {
      if (field.required) {
        const value = this.configValues[field.name];
        if (value === undefined || value === null || value === '') {
          return false;
        }
      }
    }
    return true;
  }

  async createCredential() {
    if (!this.selectedProvider || !this.selectedAuthType) return;

    this.creating = true;
    try {
      const result = await this.api.createCredential({
        credential_name: this.credentialName,
        provider_type: this.selectedProvider.provider_type,
        auth_type: this.selectedAuthType.value,
        config: this.configValues,
        description: this.description
      });

      if (result.success) {
        await this.router.navigateByUrl('/administration/credentials');
      } else {
        alert(result.message || 'Failed to create credential');
      }
    } catch (e: any) {
      console.error('Failed to create credential', e);
      alert(e?.message || 'Failed to create credential');
    } finally {
      this.creating = false;
    }
  }

  getProviderEmoji(icon: string): string {
    const mapping: { [key: string]: string } = {
      'aws': '☁️',
      'azure': '☁️',
      'gcp': '☁️',
      'neo4j': '🔷',
      'mongodb': '🍃',
      'elasticsearch': '🔍',
      'redis': '🔴',
      'postgresql': '🐘',
      'pinecone': '🌲',
      'custom': '⚙️'
    };
    return mapping[icon] || '🔐';
  }
}
