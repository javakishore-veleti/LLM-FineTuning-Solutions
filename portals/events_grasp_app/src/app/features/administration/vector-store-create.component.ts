import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router, RouterModule } from '@angular/router';
import { ApiService, VectorStoreProvider, ProviderSchema, ProviderSchemaField } from '../../core/api.service';

@Component({
  selector: 'app-vector-store-create',
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
      grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
      gap: 1rem;
    }
    .category-section {
      margin-bottom: 2rem;
    }
    .category-title {
      font-size: 1.1rem;
      font-weight: 600;
      color: #333;
      margin-bottom: 1rem;
      padding-bottom: 0.5rem;
      border-bottom: 2px solid #eee;
    }
    .provider-card {
      border: 2px solid #e8e8e8;
      border-radius: 12px;
      padding: 1.25rem;
      cursor: pointer;
      transition: all 0.2s;
      position: relative;
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
      opacity: 0.6;
      cursor: not-allowed;
    }
    .provider-card.coming-soon:hover {
      border-color: #e8e8e8;
      box-shadow: none;
    }
    .provider-header {
      display: flex;
      align-items: center;
      gap: 0.75rem;
      margin-bottom: 0.75rem;
    }
    .provider-icon {
      width: 40px;
      height: 40px;
      border-radius: 10px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 1.25rem;
      background: linear-gradient(135deg, rgba(102,126,234,0.1), rgba(118,75,162,0.1));
    }
    .provider-icon.aws { background: linear-gradient(135deg, #ff9900, #ff6600); }
    .provider-icon.mongodb { background: linear-gradient(135deg, #00684a, #13aa52); }
    .provider-icon.neo4j { background: linear-gradient(135deg, #018bff, #0056b3); }
    .provider-icon.gcp { background: linear-gradient(135deg, #4285f4, #34a853); }
    .provider-icon.azure { background: linear-gradient(135deg, #0078d4, #00bcf2); }
    .provider-name {
      font-weight: 600;
      color: #333;
      font-size: 0.95rem;
    }
    .provider-description {
      font-size: 0.85rem;
      color: #666;
      line-height: 1.4;
    }
    .provider-status {
      position: absolute;
      top: 0.75rem;
      right: 0.75rem;
      font-size: 0.7rem;
      font-weight: 600;
      padding: 0.25rem 0.5rem;
      border-radius: 10px;
      text-transform: uppercase;
    }
    .status-available {
      background: #d4edda;
      color: #155724;
    }
    .status-coming_soon {
      background: #fff3cd;
      color: #856404;
    }
    .status-beta {
      background: #cce5ff;
      color: #004085;
    }

    /* Config Form Styles */
    .config-form {
      max-width: 700px;
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
    .form-hint {
      font-size: 0.8rem;
      color: #888;
      margin-top: 0.35rem;
    }
    .form-error {
      font-size: 0.8rem;
      color: #dc3545;
      margin-top: 0.35rem;
    }

    /* Coming Soon Page */
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
      max-width: 500px;
      margin: 0 auto 2rem;
      line-height: 1.6;
    }

    /* Action Buttons */
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
    .btn-test {
      background: #f8f9fa;
      color: #667eea;
      border: 1.5px solid #667eea;
      border-radius: 10px;
      padding: 0.6rem 1.2rem;
      font-size: 0.9rem;
      font-weight: 500;
      cursor: pointer;
      transition: all 0.2s;
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }
    .btn-test:hover {
      background: rgba(102,126,234,0.05);
    }

    /* Loading */
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
              <span>🗄️</span>
              Create Vector Store
            </div>
            <p class="page-subtitle">Configure a new vector database for semantic search</p>
          </div>
          <a class="btn-back" routerLink="/administration/vector-stores">
            <span>←</span>
            Back to Vector Stores
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
              <div class="step-label">Configure</div>
            </div>
            <div class="wizard-step" [class.active]="currentStep === 3">
              <div class="step-number">3</div>
              <div class="step-label">Review & Create</div>
            </div>
          </div>

          <!-- Loading -->
          <div class="loading-state" *ngIf="loading">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">⏳</div>
            Loading...
          </div>

          <!-- Step 1: Select Provider -->
          <div class="wizard-content" *ngIf="!loading && currentStep === 1">
            <div *ngFor="let category of categoryOrder">
              <div class="category-section" *ngIf="providerCategories[category]?.length">
                <div class="category-title">{{ category }}</div>
                <div class="provider-grid">
                  <div *ngFor="let provider of providerCategories[category]"
                       class="provider-card"
                       [class.selected]="selectedProvider?.provider_type === provider.provider_type"
                       [class.coming-soon]="provider.status === 'coming_soon'"
                       (click)="selectProvider(provider)">
                    <span class="provider-status" [ngClass]="'status-' + provider.status">
                      {{ formatStatus(provider.status) }}
                    </span>
                    <div class="provider-header">
                      <div class="provider-icon" [ngClass]="provider.icon">
                        {{ getProviderEmoji(provider.icon) }}
                      </div>
                      <div class="provider-name">{{ provider.name }}</div>
                    </div>
                    <div class="provider-description">{{ provider.description }}</div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Step 2: Configure -->
          <div class="wizard-content" *ngIf="!loading && currentStep === 2">
            <!-- Coming Soon -->
            <div class="coming-soon-container" *ngIf="providerSchema?.coming_soon">
              <div class="coming-soon-icon">🚀</div>
              <div class="coming-soon-title">{{ providerSchema?.provider_name }} is Coming Soon!</div>
              <div class="coming-soon-message">
                {{ providerSchema?.message || 'We\\'re working hard to bring you this integration. Please check back later!' }}
              </div>
              <button class="btn-secondary" (click)="goToStep(1)">
                ← Choose Another Provider
              </button>
            </div>

            <!-- Configuration Form -->
            <div class="config-form" *ngIf="!providerSchema?.coming_soon && providerSchema">
              <div class="form-section">
                <div class="section-title">
                  <span>📝</span>
                  Basic Information
                </div>
                <div class="form-group">
                  <label class="form-label">
                    Display Name <span class="required">*</span>
                  </label>
                  <input type="text" class="form-control"
                         [(ngModel)]="displayName"
                         placeholder="My Vector Store">
                  <div class="form-hint">A friendly name for this vector store</div>
                </div>

                <div class="form-group">
                  <label class="form-label">
                    Credentials <span class="required">*</span>
                  </label>
                  <select class="form-control" [(ngModel)]="selectedCredentialId" (change)="onCredentialChange()">
                    <option [ngValue]="null">Select credentials...</option>
                    <option *ngFor="let cred of availableCredentials" [ngValue]="cred.credential_id">
                      {{ cred.credential_name }} ({{ cred.auth_type }})
                    </option>
                  </select>
                  <div class="form-hint" *ngIf="availableCredentials.length > 0">
                    Select credentials to use for authentication
                  </div>
                  <div class="form-hint" *ngIf="availableCredentials.length === 0 && !loadingCredentials" style="color: #dc3545;">
                    No credentials found for this provider.
                    <a routerLink="/administration/credentials/new" style="color: #667eea;">Create one first</a>
                  </div>
                  <div class="form-hint" *ngIf="loadingCredentials">
                    Loading credentials...
                  </div>
                </div>
              </div>

              <div class="form-section">
                <div class="section-title">
                  <span>⚙️</span>
                  {{ providerSchema.provider_name }} Configuration
                </div>

                <div *ngFor="let field of providerSchema.fields" class="form-group"
                     [hidden]="!shouldShowField(field)">
                  <label class="form-label">
                    {{ field.label }}
                    <span class="required" *ngIf="field.required">*</span>
                  </label>

                  <!-- Text Input -->
                  <input *ngIf="field.type === 'text'"
                         type="text"
                         class="form-control"
                         [(ngModel)]="configValues[field.name]"
                         [placeholder]="field.placeholder || ''">

                  <!-- Password Input -->
                  <input *ngIf="field.type === 'password'"
                         type="password"
                         class="form-control"
                         [(ngModel)]="configValues[field.name]"
                         [placeholder]="field.placeholder || ''">

                  <!-- Number Input -->
                  <input *ngIf="field.type === 'number'"
                         type="number"
                         class="form-control"
                         [(ngModel)]="configValues[field.name]"
                         [attr.min]="field.min"
                         [attr.max]="field.max"
                         [placeholder]="field.placeholder || ''">

                  <!-- Select Input -->
                  <select *ngIf="field.type === 'select'"
                          class="form-control"
                          [(ngModel)]="configValues[field.name]">
                    <option *ngFor="let opt of field.options" [value]="opt.value">
                      {{ opt.label }}
                    </option>
                  </select>

                  <!-- Checkbox -->
                  <div *ngIf="field.type === 'checkbox'" style="display: flex; align-items: center; gap: 0.5rem;">
                    <input type="checkbox"
                           [(ngModel)]="configValues[field.name]"
                           [id]="'field-' + field.name"
                           style="width: auto;">
                    <label [for]="'field-' + field.name" style="margin: 0; font-weight: normal;">
                      {{ field.description }}
                    </label>
                  </div>

                  <div class="form-hint" *ngIf="field.description && field.type !== 'checkbox'">
                    {{ field.description }}
                  </div>
                </div>
              </div>

              <div style="display: flex; gap: 1rem; margin-top: 1.5rem;">
                <button class="btn-test" (click)="testConnection()" [disabled]="testing">
                  <span *ngIf="!testing">🔌</span>
                  <span *ngIf="testing">⏳</span>
                  {{ testing ? 'Testing...' : 'Test Connection' }}
                </button>
                <span *ngIf="connectionTestResult"
                      [style.color]="connectionTestResult.success ? '#28a745' : '#dc3545'"
                      style="display: flex; align-items: center; gap: 0.35rem;">
                  <span>{{ connectionTestResult.success ? '✓' : '✗' }}</span>
                  {{ connectionTestResult.message }}
                </span>
              </div>
            </div>
          </div>

          <!-- Step 3: Review & Create -->
          <div class="wizard-content" *ngIf="!loading && currentStep === 3">
            <div class="form-section">
              <div class="section-title">
                <span>📋</span>
                Review Configuration
              </div>

              <div style="background: #f8f9fa; border-radius: 12px; padding: 1.5rem; margin-bottom: 1.5rem;">
                <div style="margin-bottom: 1rem;">
                  <strong>Display Name:</strong> {{ displayName }}
                </div>
                <div style="margin-bottom: 1rem;">
                  <strong>Provider:</strong> {{ providerSchema?.provider_name || 'Unknown' }}
                </div>
                <div style="margin-bottom: 1rem;">
                  <strong>Credentials:</strong> {{ getSelectedCredentialName() }}
                </div>
                <div>
                  <strong>Configuration:</strong>
                  <pre style="background: white; padding: 1rem; border-radius: 8px; margin-top: 0.5rem; overflow-x: auto;">{{ getConfigSummary() }}</pre>
                </div>
                <div style="margin-top: 1rem; padding: 1rem; background: #fff3cd; border-radius: 8px; color: #856404;">
                  <strong>💡 Note:</strong> After creating this vector store, you can associate it with events from the Event Details page.
                </div>
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
                    *ngIf="currentStep === 2 && !providerSchema?.coming_soon"
                    [disabled]="!isStep2Valid()"
                    (click)="goToStep(3)">
              Review →
            </button>

            <button class="btn-primary"
                    *ngIf="currentStep === 3"
                    [disabled]="creating"
                    (click)="createVectorStore()">
              <span *ngIf="!creating">🚀</span>
              <span *ngIf="creating">⏳</span>
              {{ creating ? 'Creating...' : 'Create Vector Store' }}
            </button>
          </div>
        </div>
      </div>
    </div>
  `
})
export class VectorStoreCreateComponent implements OnInit {
  loading = false;
  currentStep = 1;

  // Provider selection
  providers: VectorStoreProvider[] = [];
  providerCategories: { [key: string]: VectorStoreProvider[] } = {};
  categoryOrder = ['AWS Native', 'Managed Cloud', 'Graph Database', 'Open Source', 'Database Extension', 'In-Memory', 'Search Engine', 'Azure', 'Google Cloud', 'Other'];
  selectedProvider: VectorStoreProvider | null = null;

  // Configuration
  providerSchema: ProviderSchema | null = null;
  displayName = '';
  configValues: { [key: string]: any } = {};

  // Credentials
  availableCredentials: any[] = [];
  selectedCredentialId: number | null = null;
  loadingCredentials = false;

  // Connection test
  testing = false;
  connectionTestResult: { success: boolean; message: string } | null = null;

  // Create
  creating = false;

  constructor(
    private api: ApiService,
    private router: Router
  ) {}

  async ngOnInit() {
    this.loading = true;
    try {
      // Load providers
      const providersResp = await this.api.getProviderCategories();
      if (providersResp.success) {
        this.providerCategories = providersResp.categories;
      }
    } catch (e) {
      console.error('Failed to load providers', e);
    } finally {
      this.loading = false;
    }
  }

  selectProvider(provider: VectorStoreProvider) {
    if (provider.status === 'coming_soon') return;
    this.selectedProvider = provider;
  }

  async goToStep(step: number) {
    if (step === 2 && this.selectedProvider) {
      // Load schema for selected provider
      this.loading = true;
      try {
        const resp = await this.api.getProviderSchema(this.selectedProvider.provider_type);
        if (resp.success) {
          this.providerSchema = resp.schema;
          // Initialize default values
          this.initializeDefaults();
        }
        // Load credentials for this provider
        await this.loadCredentialsForProvider();
      } catch (e) {
        console.error('Failed to load schema', e);
      } finally {
        this.loading = false;
      }
    }
    this.currentStep = step;
    this.connectionTestResult = null;
  }

  async loadCredentialsForProvider() {
    if (!this.selectedProvider) return;

    this.loadingCredentials = true;
    this.availableCredentials = [];
    this.selectedCredentialId = null;

    try {
      const resp = await this.api.getCredentialsForVectorStore(this.selectedProvider.provider_type);
      if (resp.success) {
        this.availableCredentials = resp.credentials || [];
      }
    } catch (e) {
      console.error('Failed to load credentials', e);
    } finally {
      this.loadingCredentials = false;
    }
  }

  onCredentialChange() {
    // Can be used to update UI based on selected credential
  }

  initializeDefaults() {
    if (!this.providerSchema?.fields) return;

    for (const field of this.providerSchema.fields) {
      if (field.default !== undefined && this.configValues[field.name] === undefined) {
        this.configValues[field.name] = field.default;
      }
    }
  }

  shouldShowField(field: ProviderSchemaField): boolean {
    if (!field.showIf) return true;

    for (const [key, value] of Object.entries(field.showIf)) {
      if (this.configValues[key] !== value) return false;
    }
    return true;
  }

  isStep2Valid(): boolean {
    if (!this.displayName?.trim()) return false;
    if (!this.selectedCredentialId) return false;  // Require credential selection
    if (!this.providerSchema?.fields) return false;

    for (const field of this.providerSchema.fields) {
      if (field.required && this.shouldShowField(field)) {
        const value = this.configValues[field.name];
        if (value === undefined || value === null || value === '') {
          return false;
        }
      }
    }
    return true;
  }

  async testConnection() {
    if (!this.selectedProvider) return;

    this.testing = true;
    this.connectionTestResult = null;

    try {
      const result = await this.api.testProviderConnection(
        this.selectedProvider.provider_type,
        this.configValues
      );
      this.connectionTestResult = result;
    } catch (e: any) {
      this.connectionTestResult = {
        success: false,
        message: e?.message || 'Connection test failed'
      };
    } finally {
      this.testing = false;
    }
  }


  getConfigSummary(): string {
    // Hide sensitive fields
    const summary: any = {};
    for (const [key, value] of Object.entries(this.configValues)) {
      const field = this.providerSchema?.fields?.find(f => f.name === key);
      if (field?.type === 'password') {
        summary[key] = '********';
      } else {
        summary[key] = value;
      }
    }
    return JSON.stringify(summary, null, 2);
  }

  getSelectedCredentialName(): string {
    const cred = this.availableCredentials.find(c => c.credential_id === this.selectedCredentialId);
    return cred ? `${cred.credential_name} (${cred.auth_type})` : 'None selected';
  }

  async createVectorStore() {
    if (!this.selectedProvider || !this.selectedCredentialId) return;

    this.creating = true;
    try {
      const result = await this.api.createVectorStoreWithoutEvent({
        display_name: this.displayName,
        provider_type: this.selectedProvider.provider_type,
        credential_id: this.selectedCredentialId,
        config: this.configValues
      });

      if (result.success) {
        await this.router.navigateByUrl('/administration/vector-stores');
      } else {
        alert(result.message || 'Failed to create vector store');
      }
    } catch (e: any) {
      console.error('Failed to create vector store', e);
      alert(e?.message || 'Failed to create vector store');
    } finally {
      this.creating = false;
    }
  }

  formatStatus(status: string): string {
    switch (status) {
      case 'available': return 'Available';
      case 'coming_soon': return 'Coming Soon';
      case 'beta': return 'Beta';
      default: return status;
    }
  }

  getProviderEmoji(icon: string): string {
    switch (icon) {
      case 'aws': return '☁️';
      case 'mongodb': return '🍃';
      case 'neo4j': return '🔷';
      case 'gcp': return '☁️';
      case 'azure': return '☁️';
      case 'postgresql': return '🐘';
      case 'redis': return '🔴';
      case 'elasticsearch': return '🔍';
      case 'pinecone': return '🌲';
      case 'milvus': return '🔵';
      case 'chroma': return '🎨';
      case 'qdrant': return '⚡';
      case 'weaviate': return '🔷';
      default: return '🗄️';
    }
  }
}
