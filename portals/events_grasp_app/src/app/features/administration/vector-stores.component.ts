import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ApiService, VectorStore } from '../../core/api.service';
import { AuthService } from '../../core/auth.service';

@Component({
  selector: 'app-admin-vector-stores',
  standalone: true,
  imports: [CommonModule, FormsModule],
  styles: [`
    .vector-stores-container {
      padding: 0;
    }
    .page-header {
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      padding: 2rem 2rem 4rem;
      color: white;
      margin: 0;
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
    .btn-add-store {
      background: white;
      color: #667eea;
      border: none;
      border-radius: 12px;
      padding: 0.75rem 1.5rem;
      font-size: 0.95rem;
      font-weight: 600;
      display: flex;
      align-items: center;
      gap: 0.5rem;
      cursor: pointer;
      transition: all 0.2s;
    }
    .btn-add-store:hover {
      transform: translateY(-2px);
      box-shadow: 0 5px 20px rgba(255,255,255,0.3);
    }
    .content-area {
      padding: 0 2rem 2rem;
      margin-top: -2.5rem;
    }
    .stats-row {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      gap: 1rem;
      margin-bottom: 1.5rem;
    }
    .stat-card {
      background: white;
      border-radius: 16px;
      padding: 1.25rem;
      box-shadow: 0 4px 20px rgba(0,0,0,0.1);
      display: flex;
      align-items: center;
      gap: 1rem;
    }
    .stat-icon {
      width: 48px;
      height: 48px;
      border-radius: 12px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 1.5rem;
    }
    .stat-icon.total { background: linear-gradient(135deg, rgba(102,126,234,0.15), rgba(118,75,162,0.15)); }
    .stat-icon.active { background: linear-gradient(135deg, rgba(17,153,142,0.15), rgba(56,239,125,0.15)); }
    .stat-icon.files { background: linear-gradient(135deg, rgba(255,153,102,0.15), rgba(255,94,98,0.15)); }
    .stat-icon.providers { background: linear-gradient(135deg, rgba(79,172,254,0.15), rgba(0,242,254,0.15)); }
    .stat-value {
      font-size: 1.5rem;
      font-weight: 700;
      color: #333;
    }
    .stat-label {
      font-size: 0.85rem;
      color: #888;
    }
    .stores-card {
      background: white;
      border-radius: 16px;
      box-shadow: 0 4px 20px rgba(0,0,0,0.1);
      overflow: hidden;
    }
    .stores-header {
      padding: 1.25rem 1.5rem;
      border-bottom: 1px solid #eee;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .stores-count {
      font-weight: 600;
      color: #333;
      font-size: 1rem;
    }
    .stores-count span {
      color: #667eea;
    }
    .loading-state, .error-state {
      padding: 3rem;
      text-align: center;
    }
    .loading-state { color: #888; }
    .error-state { color: #dc3545; }
    .empty-state {
      text-align: center;
      padding: 4rem 2rem;
      color: #888;
    }
    .empty-icon {
      font-size: 4rem;
      margin-bottom: 1rem;
      opacity: 0.5;
    }
    .empty-text {
      font-size: 1.2rem;
      margin-bottom: 0.5rem;
      color: #555;
    }
    .empty-hint {
      font-size: 0.95rem;
      color: #888;
      margin-bottom: 1.5rem;
    }
    .stores-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
      gap: 1rem;
      padding: 1.5rem;
    }
    .store-card {
      background: #fafafa;
      border-radius: 14px;
      padding: 1.25rem;
      border: 2px solid #e8e8e8;
      transition: all 0.2s;
    }
    .store-card:hover {
      border-color: #667eea;
      box-shadow: 0 4px 15px rgba(102, 126, 234, 0.15);
    }
    .store-header {
      display: flex;
      align-items: flex-start;
      gap: 1rem;
      margin-bottom: 1rem;
    }
    .store-icon {
      width: 48px;
      height: 48px;
      border-radius: 12px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 1.5rem;
      flex-shrink: 0;
    }
    .store-icon.openai { background: linear-gradient(135deg, #10a37f, #1a7f5a); }
    .store-icon.pinecone { background: linear-gradient(135deg, #000, #333); }
    .store-icon.weaviate { background: linear-gradient(135deg, #ff6b6b, #ee5a5a); }
    .store-icon.chroma { background: linear-gradient(135deg, #ffd43b, #fab005); }
    .store-icon.default { background: linear-gradient(135deg, #667eea, #764ba2); }
    .store-info {
      flex: 1;
      min-width: 0;
    }
    .store-name {
      font-weight: 600;
      color: #333;
      font-size: 1rem;
      margin-bottom: 0.25rem;
      word-break: break-word;
    }
    .store-provider {
      font-size: 0.85rem;
      color: #667eea;
      font-weight: 500;
    }
    .store-status {
      padding: 0.25rem 0.6rem;
      border-radius: 20px;
      font-size: 0.7rem;
      font-weight: 600;
      text-transform: uppercase;
    }
    .status-active { background: #d4edda; color: #155724; }
    .status-pending { background: #fff3cd; color: #856404; }
    .status-error { background: #f8d7da; color: #721c24; }
    .store-meta {
      display: flex;
      flex-wrap: wrap;
      gap: 1rem;
      margin-bottom: 1rem;
      padding-top: 1rem;
      border-top: 1px solid #eee;
    }
    .store-meta-item {
      display: flex;
      align-items: center;
      gap: 0.35rem;
      font-size: 0.85rem;
      color: #666;
    }
    .store-event {
      background: linear-gradient(135deg, rgba(102,126,234,0.1), rgba(118,75,162,0.1));
      border-radius: 8px;
      padding: 0.5rem 0.75rem;
      font-size: 0.85rem;
      color: #667eea;
      font-weight: 500;
      display: flex;
      align-items: center;
      gap: 0.35rem;
    }
    .store-actions {
      display: flex;
      gap: 0.5rem;
      margin-top: 1rem;
      padding-top: 1rem;
      border-top: 1px solid #eee;
    }
    .btn-action {
      flex: 1;
      padding: 0.5rem;
      border-radius: 8px;
      border: none;
      font-size: 0.85rem;
      font-weight: 500;
      cursor: pointer;
      transition: all 0.2s;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 0.35rem;
    }
    .btn-manage {
      background: linear-gradient(135deg, #667eea, #764ba2);
      color: white;
    }
    .btn-manage:hover {
      transform: translateY(-1px);
      box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    }
    .btn-delete {
      background: #f8f8f8;
      color: #dc3545;
      border: 1px solid #eee;
    }
    .btn-delete:hover {
      background: #f8d7da;
    }
  `],
  template: `
    <div class="vector-stores-container">
      <!-- Header -->
      <div class="page-header">
        <div class="header-content">
          <div>
            <div class="page-title">
              <span>🗄️</span>
              Vector Stores
            </div>
            <p class="page-subtitle">Manage your vector databases for semantic search and RAG</p>
          </div>
          <button class="btn-add-store" (click)="showAddModal = true">
            <span>➕</span>
            Add Vector Store
          </button>
        </div>
      </div>

      <div class="content-area">
        <!-- Stats Row -->
        <div class="stats-row" *ngIf="!loading && vectorStores.length > 0">
          <div class="stat-card">
            <div class="stat-icon total">🗄️</div>
            <div>
              <div class="stat-value">{{ vectorStores.length }}</div>
              <div class="stat-label">Total Stores</div>
            </div>
          </div>
          <div class="stat-card">
            <div class="stat-icon active">✅</div>
            <div>
              <div class="stat-value">{{ getActiveCount() }}</div>
              <div class="stat-label">Active</div>
            </div>
          </div>
          <div class="stat-card">
            <div class="stat-icon files">📁</div>
            <div>
              <div class="stat-value">{{ getTotalFiles() }}</div>
              <div class="stat-label">Total Files</div>
            </div>
          </div>
          <div class="stat-card">
            <div class="stat-icon providers">🔌</div>
            <div>
              <div class="stat-value">{{ getUniqueProviders().length }}</div>
              <div class="stat-label">Providers</div>
            </div>
          </div>
        </div>

        <!-- Stores Card -->
        <div class="stores-card">
          <!-- Header with count -->
          <div class="stores-header" *ngIf="!loading && vectorStores.length > 0">
            <div class="stores-count">
              Showing <span>{{ vectorStores.length }}</span> vector store{{ vectorStores.length !== 1 ? 's' : '' }}
            </div>
          </div>

          <!-- Loading State -->
          <div class="loading-state" *ngIf="loading">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">⏳</div>
            Loading vector stores...
          </div>

          <!-- Error State -->
          <div class="error-state" *ngIf="error">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">⚠️</div>
            {{ error }}
          </div>

          <!-- Empty State -->
          <div class="empty-state" *ngIf="!loading && !error && vectorStores.length === 0">
            <div class="empty-icon">🗄️</div>
            <div class="empty-text">No vector stores configured</div>
            <div class="empty-hint">Add a vector store to enable semantic search and RAG capabilities</div>
            <button class="btn-add-store" style="margin: 0 auto; background: linear-gradient(135deg, #667eea, #764ba2); color: white;" (click)="showAddModal = true">
              <span>🚀</span>
              Add Your First Vector Store
            </button>
          </div>

          <!-- Vector Stores Grid -->
          <div class="stores-grid" *ngIf="!loading && !error && vectorStores.length > 0">
            <div class="store-card" *ngFor="let store of vectorStores">
              <div class="store-header">
                <div class="store-icon" [ngClass]="getProviderClass(store.vector_store_provider)">
                  {{ getProviderIcon(store.vector_store_provider) }}
                </div>
                <div class="store-info">
                  <div class="store-name">{{ store.vector_store_db_name }}</div>
                  <div class="store-provider">{{ formatProvider(store.vector_store_provider) }}</div>
                </div>
                <span class="store-status" [ngClass]="'status-' + store.status">
                  {{ store.status }}
                </span>
              </div>

              <div class="store-meta">
                <div class="store-meta-item">
                  <span>📁</span>
                  <span>{{ store.files_count }} files</span>
                </div>
                <div class="store-meta-item" *ngIf="store.created_at">
                  <span>📅</span>
                  <span>{{ formatDate(store.created_at) }}</span>
                </div>
              </div>

              <div class="store-event" *ngIf="store.event_name">
                <span>📄</span>
                {{ store.event_name }}
              </div>

              <div class="store-actions">
                <button class="btn-action btn-manage">
                  <span>⚙️</span>
                  Manage
                </button>
                <button class="btn-action btn-delete" (click)="deleteStore(store.vector_store_id)">
                  <span>🗑️</span>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  `
})
export class AdminVectorStoresComponent implements OnInit {
  vectorStores: VectorStore[] = [];
  loading = false;
  error: string | null = null;
  showAddModal = false;
  private customerId: number | undefined;

  constructor(private api: ApiService, private auth: AuthService) {}

  async ngOnInit() {
    // Get logged in user's customer ID
    try {
      const user = await this.auth.me();
      if (user) {
        this.customerId = user.customer_id;
      }
    } catch (e) {
      console.error('Failed to get user info', e);
    }
    this.loadVectorStores();
  }

  async loadVectorStores() {
    this.loading = true;
    this.error = null;
    try {
      // Pass undefined for eventId and customerId for customer filtering
      const response = await this.api.getVectorStores(undefined, this.customerId);
      if (response.success && response.vector_stores) {
        this.vectorStores = response.vector_stores;
      } else {
        this.error = response.message || 'Failed to load vector stores';
      }
    } catch (err: any) {
      console.error(err);
      this.error = err?.message || 'Failed to load vector stores';
    } finally {
      this.loading = false;
    }
  }

  getActiveCount(): number {
    return this.vectorStores.filter(s => s.status === 'active').length;
  }

  getTotalFiles(): number {
    return this.vectorStores.reduce((sum, s) => sum + (s.files_count || 0), 0);
  }

  getUniqueProviders(): string[] {
    return [...new Set(this.vectorStores.map(s => s.vector_store_provider))];
  }

  getProviderIcon(provider: string): string {
    switch (provider?.toLowerCase()) {
      case 'openai': return '🤖';
      case 'pinecone': return '🌲';
      case 'weaviate': return '🔷';
      case 'chroma': return '🎨';
      case 'qdrant': return '🔶';
      case 'milvus': return '🐬';
      default: return '🗄️';
    }
  }

  getProviderClass(provider: string): string {
    switch (provider?.toLowerCase()) {
      case 'openai': return 'openai';
      case 'pinecone': return 'pinecone';
      case 'weaviate': return 'weaviate';
      case 'chroma': return 'chroma';
      default: return 'default';
    }
  }

  formatProvider(provider: string): string {
    switch (provider?.toLowerCase()) {
      case 'openai': return 'OpenAI';
      case 'pinecone': return 'Pinecone';
      case 'weaviate': return 'Weaviate';
      case 'chroma': return 'ChromaDB';
      case 'qdrant': return 'Qdrant';
      case 'milvus': return 'Milvus';
      default: return provider;
    }
  }

  formatDate(dateStr: string): string {
    if (!dateStr) return '';
    try {
      const date = new Date(dateStr);
      return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
    } catch {
      return dateStr;
    }
  }

  async deleteStore(vectorStoreId: number) {
    if (!confirm('Are you sure you want to delete this vector store?')) return;

    try {
      const response = await this.api.deleteVectorStore(vectorStoreId);
      if (response.success) {
        this.vectorStores = this.vectorStores.filter(s => s.vector_store_id !== vectorStoreId);
      } else {
        alert(response.message || 'Failed to delete vector store');
      }
    } catch (err: any) {
      console.error(err);
      alert(err?.message || 'Failed to delete vector store');
    }
  }
}
