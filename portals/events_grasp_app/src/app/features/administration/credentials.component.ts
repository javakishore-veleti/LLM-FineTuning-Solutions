import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterModule } from '@angular/router';
import { ApiService, Credential, CredentialProvider } from '../../core/api.service';

@Component({
  selector: 'app-admin-credentials',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterModule],
  styles: [`
    .credentials-container { padding: 0; }
    .page-header { background: linear-gradient(135deg, #667eea, #764ba2); padding: 2rem 2rem 4rem; color: white; }
    .header-content { display: flex; justify-content: space-between; align-items: center; }
    .page-title { font-size: 1.75rem; font-weight: 700; margin-bottom: 0.25rem; display: flex; align-items: center; gap: 0.5rem; }
    .page-subtitle { opacity: 0.9; }
    .btn-add { background: white; color: #667eea; border: none; border-radius: 12px; padding: 0.75rem 1.5rem; font-weight: 600; display: flex; align-items: center; gap: 0.5rem; cursor: pointer; text-decoration: none; }
    .btn-add:hover { transform: translateY(-2px); box-shadow: 0 5px 20px rgba(0,0,0,0.2); }
    .content-area { padding: 0 2rem 2rem; margin-top: -2.5rem; }
    .stats-row { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 1rem; margin-bottom: 1.5rem; }
    .stat-card { background: white; border-radius: 12px; padding: 1rem; display: flex; align-items: center; gap: 0.75rem; box-shadow: 0 2px 8px rgba(0,0,0,0.08); }
    .stat-icon { width: 40px; height: 40px; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 1.25rem; }
    .stat-icon.total { background: rgba(102,126,234,0.15); }
    .stat-value { font-size: 1.5rem; font-weight: 700; color: #333; }
    .stat-label { font-size: 0.8rem; color: #888; }
    .main-card { background: white; border-radius: 16px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); overflow: hidden; }
    .card-header { padding: 1.25rem 1.5rem; border-bottom: 1px solid #eee; display: flex; justify-content: space-between; align-items: center; }
    .card-title { font-size: 1.1rem; font-weight: 600; color: #333; }
    .filter-select { padding: 0.5rem 1rem; border: 1.5px solid #e0e0e0; border-radius: 8px; background: white; }
    .filter-select:focus { outline: none; border-color: #667eea; }
    .credential-item { display: flex; align-items: center; padding: 1rem 1.5rem; border-bottom: 1px solid #f0f0f0; }
    .credential-item:hover { background: #fafafa; }
    .credential-item:last-child { border-bottom: none; }
    .provider-icon { width: 44px; height: 44px; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 1.5rem; margin-right: 1rem; color: white; }
    .provider-icon.aws { background: linear-gradient(135deg, #ff9900, #ff6600); }
    .provider-icon.azure { background: linear-gradient(135deg, #0078d4, #00bcf2); }
    .provider-icon.gcp { background: linear-gradient(135deg, #4285f4, #34a853); }
    .provider-icon.neo4j { background: linear-gradient(135deg, #018bff, #0056b3); }
    .provider-icon.mongodb { background: linear-gradient(135deg, #00684a, #13aa52); }
    .provider-icon.elasticsearch { background: linear-gradient(135deg, #fed10a, #00bfb3); color: #333; }
    .provider-icon.redis { background: linear-gradient(135deg, #dc382d, #a41e11); }
    .provider-icon.postgresql { background: linear-gradient(135deg, #336791, #0064a5); }
    .provider-icon.default { background: linear-gradient(135deg, #667eea, #764ba2); }
    .credential-info { flex: 1; }
    .credential-name { font-weight: 600; color: #333; margin-bottom: 0.25rem; }
    .credential-meta { font-size: 0.85rem; color: #888; display: flex; gap: 1rem; }
    .auth-badge { background: #f0f0f0; padding: 0.2rem 0.5rem; border-radius: 4px; font-size: 0.75rem; color: #666; }
    .credential-actions { display: flex; gap: 0.5rem; }
    .btn-action { padding: 0.5rem 1rem; border: none; border-radius: 8px; font-size: 0.85rem; cursor: pointer; }
    .btn-edit { background: #f0f0f0; color: #333; }
    .btn-edit:hover { background: #e0e0e0; }
    .btn-delete { background: #fff5f5; color: #dc3545; }
    .btn-delete:hover { background: #ffe0e0; }
    .empty-state { text-align: center; padding: 4rem 2rem; color: #888; }
    .empty-icon { font-size: 4rem; margin-bottom: 1rem; }
    .empty-text { font-size: 1.1rem; font-weight: 500; color: #666; margin-bottom: 0.5rem; }
    .empty-hint { font-size: 0.9rem; margin-bottom: 1.5rem; }
    .loading-state { text-align: center; padding: 3rem; color: #888; }
  `],
  template: `
    <div class="credentials-container">
      <!-- Header -->
      <div class="page-header">
        <div class="header-content">
          <div>
            <div class="page-title">
              <span>🔐</span>
              Credentials
            </div>
            <p class="page-subtitle">Manage your provider credentials for vector stores and integrations</p>
          </div>
          <a class="btn-add" routerLink="/administration/credentials/new">
            <span>➕</span>
            Add Credential
          </a>
        </div>
      </div>

      <div class="content-area">
        <!-- Stats -->
        <div class="stats-row" *ngIf="!loading && credentials.length > 0">
          <div class="stat-card">
            <div class="stat-icon total">🔐</div>
            <div>
              <div class="stat-value">{{ credentials.length }}</div>
              <div class="stat-label">Total</div>
            </div>
          </div>
          <div class="stat-card" *ngFor="let stat of providerStats">
            <div class="stat-icon" [ngClass]="stat.icon">{{ stat.emoji }}</div>
            <div>
              <div class="stat-value">{{ stat.count }}</div>
              <div class="stat-label">{{ stat.name }}</div>
            </div>
          </div>
        </div>

        <!-- Main Card -->
        <div class="main-card">
          <div class="card-header">
            <div class="card-title">All Credentials</div>
            <div class="filter-group">
              <select class="filter-select" [(ngModel)]="filterProvider" (change)="applyFilter()">
                <option value="">All Providers</option>
                <option *ngFor="let provider of providers" [value]="provider.provider_type">
                  {{ provider.name }}
                </option>
              </select>
            </div>
          </div>

          <!-- Loading -->
          <div class="loading-state" *ngIf="loading">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">⏳</div>
            Loading credentials...
          </div>

          <!-- Empty State -->
          <div class="empty-state" *ngIf="!loading && filteredCredentials.length === 0">
            <div class="empty-icon">🔐</div>
            <div class="empty-text">No credentials found</div>
            <div class="empty-hint">Add credentials to connect to your vector store providers</div>
            <a class="btn-add" style="display: inline-flex; background: linear-gradient(135deg, #667eea, #764ba2); color: white;"
               routerLink="/administration/credentials/new">
              <span>🚀</span>
              Add Your First Credential
            </a>
          </div>

          <!-- Credentials List -->
          <div class="credentials-list" *ngIf="!loading && filteredCredentials.length > 0">
            <div class="credential-item" *ngFor="let cred of filteredCredentials">
              <div class="provider-icon" [ngClass]="cred.provider_icon || 'default'">
                {{ getProviderEmoji(cred.provider_icon) }}
              </div>
              <div class="credential-info">
                <div class="credential-name">{{ cred.credential_name }}</div>
                <div class="credential-meta">
                  <span>{{ cred.provider_name }}</span>
                  <span class="auth-badge">{{ formatAuthType(cred.auth_type) }}</span>
                  <span *ngIf="cred.description">{{ cred.description }}</span>
                </div>
              </div>
              <div class="credential-actions">
                <button class="btn-action btn-edit" (click)="editCredential(cred)">
                  ✏️ Edit
                </button>
                <button class="btn-action btn-delete" (click)="deleteCredential(cred)">
                  🗑️ Delete
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  `
})
export class AdminCredentialsComponent implements OnInit {
  credentials: Credential[] = [];
  filteredCredentials: Credential[] = [];
  providers: CredentialProvider[] = [];
  loading = false;
  filterProvider = '';

  providerStats: { name: string; icon: string; emoji: string; count: number }[] = [];

  constructor(private api: ApiService) {}

  async ngOnInit() {
    await this.loadData();
  }

  async loadData() {
    this.loading = true;
    try {
      // Load providers
      const providersResp = await this.api.getCredentialProviders();
      if (providersResp.success) {
        this.providers = providersResp.providers;
      }

      // Load credentials
      const credsResp = await this.api.getCredentials();
      if (credsResp.success) {
        this.credentials = credsResp.credentials;
        this.filteredCredentials = [...this.credentials];
        this.calculateStats();
      }
    } catch (e) {
      console.error('Failed to load data', e);
    } finally {
      this.loading = false;
    }
  }

  calculateStats() {
    const counts: { [key: string]: number } = {};
    for (const cred of this.credentials) {
      counts[cred.provider_type] = (counts[cred.provider_type] || 0) + 1;
    }

    this.providerStats = Object.entries(counts)
      .map(([type, count]) => {
        const provider = this.providers.find(p => p.provider_type === type);
        return {
          name: provider?.name || type,
          icon: provider?.icon || 'default',
          emoji: this.getProviderEmoji(provider?.icon || 'default'),
          count
        };
      })
      .slice(0, 4); // Show top 4
  }

  applyFilter() {
    if (!this.filterProvider) {
      this.filteredCredentials = [...this.credentials];
    } else {
      this.filteredCredentials = this.credentials.filter(c => c.provider_type === this.filterProvider);
    }
  }

  async deleteCredential(cred: Credential) {
    if (!confirm(`Are you sure you want to delete "${cred.credential_name}"?`)) {
      return;
    }

    try {
      const result = await this.api.deleteCredential(cred.credential_id);
      if (result.success) {
        await this.loadData();
      } else {
        alert(result.message || 'Failed to delete credential');
      }
    } catch (e: any) {
      alert(e?.message || 'Failed to delete credential');
    }
  }

  editCredential(cred: Credential) {
    // TODO: Navigate to edit page or open modal
    alert('Edit functionality coming soon');
  }

  formatAuthType(authType: string): string {
    const mapping: { [key: string]: string } = {
      'basic': 'Access Key',
      'iam_role': 'IAM Role',
      'profile': 'AWS Profile',
      'service_principal': 'Service Principal',
      'managed_identity': 'Managed Identity',
      'connection_string': 'Connection String',
      'service_account': 'Service Account',
      'application_default': 'Default Credentials',
      'api_key': 'API Key',
      'password': 'Password Auth',
      'acl': 'ACL User'
    };
    return mapping[authType] || authType;
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
      'default': '🔐'
    };
    return mapping[icon] || '🔐';
  }
}
