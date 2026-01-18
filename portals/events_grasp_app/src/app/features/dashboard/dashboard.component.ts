import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { AuthService } from '../../core/auth.service';
import { ApiService, DashboardDataResponse, RecentEvent, RecentConversation } from '../../core/api.service';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule, RouterModule],
  styles: [`
    .dashboard-container {
      min-height: calc(100vh - 60px);
      background: #f5f7fb;
    }
    .dashboard-header {
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      padding: 2.5rem 0;
      color: white;
    }
    .greeting {
      font-size: 2rem;
      font-weight: 700;
      margin-bottom: 0.5rem;
    }
    .greeting-sub {
      font-size: 1.1rem;
      opacity: 0.9;
    }
    .stats-row {
      margin-top: -3rem;
      position: relative;
      z-index: 10;
    }
    .stat-card {
      background: white;
      border-radius: 16px;
      padding: 1.5rem;
      box-shadow: 0 4px 20px rgba(0,0,0,0.08);
      height: 100%;
      transition: transform 0.2s, box-shadow 0.2s;
    }
    .stat-card:hover {
      transform: translateY(-4px);
      box-shadow: 0 8px 30px rgba(0,0,0,0.12);
    }
    .stat-icon {
      width: 56px;
      height: 56px;
      border-radius: 12px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 1.5rem;
      margin-bottom: 1rem;
    }
    .stat-icon.events { background: linear-gradient(135deg, #667eea, #764ba2); }
    .stat-icon.conversations { background: linear-gradient(135deg, #11998e, #38ef7d); }
    .stat-icon.vectors { background: linear-gradient(135deg, #ff9966, #ff5e62); }
    .stat-icon.providers { background: linear-gradient(135deg, #4facfe, #00f2fe); }
    .stat-value {
      font-size: 2rem;
      font-weight: 700;
      color: #333;
      line-height: 1;
    }
    .stat-label {
      font-size: 0.9rem;
      color: #666;
      margin-top: 0.25rem;
    }
    .section-title {
      font-size: 1.25rem;
      font-weight: 700;
      color: #333;
      margin-bottom: 1rem;
    }
    .quick-actions {
      padding: 2rem 0;
    }
    .quick-actions.mt-4 {
      margin-top: 1.5rem;
    }
    .getting-started-header {
      text-align: center;
      margin-bottom: 1.5rem;
      padding: 1.5rem;
      background: linear-gradient(135deg, rgba(102,126,234,0.1) 0%, rgba(118,75,162,0.1) 100%);
      border-radius: 16px;
      border: 2px dashed #667eea;
    }
    .getting-started-header .section-title {
      color: #667eea;
      font-size: 1.5rem;
    }
    .getting-started-sub {
      color: #444;
      font-size: 1.5rem;
      font-weight: 600;
      margin: 0;
      margin-top: 0.5rem;
    }
    .action-card {
      background: white;
      border-radius: 16px;
      padding: 1.5rem;
      box-shadow: 0 4px 20px rgba(0,0,0,0.08);
      cursor: pointer;
      transition: all 0.2s;
      text-decoration: none;
      color: inherit;
      display: block;
      height: 100%;
    }
    .action-card:hover {
      transform: translateY(-4px);
      box-shadow: 0 8px 30px rgba(0,0,0,0.12);
    }
    .action-icon {
      width: 48px;
      height: 48px;
      border-radius: 12px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 1.25rem;
      margin-bottom: 1rem;
      background: #f0f0f0;
    }
    .action-card h5 {
      font-size: 1rem;
      font-weight: 600;
      color: #333;
      margin-bottom: 0.25rem;
    }
    .action-card p {
      font-size: 0.85rem;
      color: #666;
      margin: 0;
    }
    .recent-section {
      padding: 0 0 2rem;
    }
    .recent-card {
      background: white;
      border-radius: 16px;
      box-shadow: 0 4px 20px rgba(0,0,0,0.08);
      overflow: hidden;
    }
    .recent-card-header {
      padding: 1rem 1.5rem;
      border-bottom: 1px solid #eee;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .recent-card-header h5 {
      font-size: 1rem;
      font-weight: 600;
      margin: 0;
    }
    .recent-card-body {
      padding: 0;
    }
    .recent-item {
      padding: 1rem 1.5rem;
      border-bottom: 1px solid #f0f0f0;
      display: flex;
      align-items: center;
      gap: 1rem;
      transition: background 0.2s;
    }
    .recent-item:last-child {
      border-bottom: none;
    }
    .recent-item:hover {
      background: #f9f9f9;
    }
    .recent-item-icon {
      width: 40px;
      height: 40px;
      border-radius: 10px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 1rem;
      flex-shrink: 0;
    }
    .recent-item-icon.event { background: #e8f4fd; }
    .recent-item-icon.chat { background: #e8fdf4; }
    .recent-item-content {
      flex: 1;
      min-width: 0;
    }
    .recent-item-title {
      font-weight: 600;
      color: #333;
      font-size: 0.95rem;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }
    .recent-item-meta {
      font-size: 0.8rem;
      color: #888;
    }
    .recent-item-badge {
      padding: 4px 10px;
      border-radius: 20px;
      font-size: 0.75rem;
      font-weight: 500;
    }
    .badge-indexed { background: #d4edda; color: #155724; }
    .badge-pending { background: #fff3cd; color: #856404; }
    .empty-state {
      padding: 3rem;
      text-align: center;
      color: #888;
    }
    .empty-state-icon {
      font-size: 3rem;
      margin-bottom: 1rem;
      opacity: 0.5;
    }
    .view-all-link {
      color: #667eea;
      font-size: 0.85rem;
      font-weight: 500;
      text-decoration: none;
    }
    .view-all-link:hover {
      text-decoration: underline;
    }
    .tips-card {
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      border-radius: 16px;
      padding: 1.5rem;
      color: white;
    }
    .tips-card h5 {
      font-size: 1rem;
      font-weight: 600;
      margin-bottom: 1rem;
    }
    .tip-item {
      display: flex;
      align-items: flex-start;
      gap: 10px;
      margin-bottom: 0.75rem;
      font-size: 0.9rem;
      opacity: 0.95;
    }
    .tip-item:last-child {
      margin-bottom: 0;
    }
  `],
  template: `
    <div class="dashboard-container">
      <!-- Header -->
      <div class="dashboard-header">
        <div class="container">
          <div class="greeting">Welcome back, {{ userName }}! 👋</div>
          <p class="greeting-sub">Here's what's happening with your knowledge base</p>
        </div>
      </div>

      <!-- Stats Row - Only show when user has events -->
      <div class="container stats-row" *ngIf="stats.events > 0">
        <div class="row g-4">
          <div class="col-6 col-lg-3">
            <div class="stat-card">
              <div class="stat-icon events">📄</div>
              <div class="stat-value">{{ stats.events }}</div>
              <div class="stat-label">Events Scraped</div>
            </div>
          </div>
          <div class="col-6 col-lg-3">
            <div class="stat-card">
              <div class="stat-icon conversations">💬</div>
              <div class="stat-value">{{ stats.conversations }}</div>
              <div class="stat-label">Conversations</div>
            </div>
          </div>
          <div class="col-6 col-lg-3">
            <div class="stat-card">
              <div class="stat-icon vectors">🗄️</div>
              <div class="stat-value">{{ stats.vectorStores }}</div>
              <div class="stat-label">Vector Stores</div>
            </div>
          </div>
          <div class="col-6 col-lg-3">
            <div class="stat-card">
              <div class="stat-icon providers">🔌</div>
              <div class="stat-value">{{ stats.providers }}</div>
              <div class="stat-label">LLM Providers</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Quick Actions -->
      <div class="container quick-actions" [class.mt-4]="stats.events === 0">
        <h4 class="section-title" *ngIf="stats.events > 0">Quick Actions</h4>
        <div *ngIf="stats.events === 0" class="getting-started-header">
          <h4 class="section-title mb-1">🚀 Quick Actions — Start Here!</h4>
          <p class="getting-started-sub">Set up your first event and start having AI-powered conversations with it!</p>
        </div>
        <div class="row g-4">
          <div class="col-6 col-md-3">
            <a routerLink="/administration/events/new" class="action-card">
              <div class="action-icon">🔗</div>
              <h5>Scrape New Event</h5>
              <p>Add a new event URL to scrape</p>
            </a>
          </div>
          <div class="col-6 col-md-3">
            <a routerLink="/conversations" class="action-card">
              <div class="action-icon">💬</div>
              <h5>Start Conversation</h5>
              <p>Chat with your indexed content</p>
            </a>
          </div>
          <div class="col-6 col-md-3">
            <a routerLink="/settings" class="action-card">
              <div class="action-icon">🗄️</div>
              <h5>Configure Vector DB</h5>
              <p>Set up your vector store providers</p>
            </a>
          </div>
          <div class="col-6 col-md-3">
            <a routerLink="/settings" class="action-card">
              <div class="action-icon">🤖</div>
              <h5>Add LLM Provider</h5>
              <p>Connect OpenAI, Anthropic, etc.</p>
            </a>
          </div>
        </div>
      </div>

      <!-- Recent Activity - Only show when user has events -->
      <div class="container recent-section" *ngIf="stats.events > 0">
        <div class="row g-4">
          <!-- Recent Events -->
          <div class="col-lg-6">
            <div class="recent-card">
              <div class="recent-card-header">
                <h5>📄 Recent Events</h5>
                <a routerLink="/administration/events" class="view-all-link">View all →</a>
              </div>
              <div class="recent-card-body">
                <div *ngIf="recentEvents.length === 0" class="empty-state">
                  <div class="empty-state-icon">📄</div>
                  <p>No events scraped yet</p>
                  <a routerLink="/administration/events/new" class="btn btn-sm btn-primary mt-2">Scrape your first event</a>
                </div>
                <div *ngFor="let event of recentEvents" class="recent-item">
                  <div class="recent-item-icon event">📄</div>
                  <div class="recent-item-content">
                    <div class="recent-item-title">{{ event.name }}</div>
                    <div class="recent-item-meta">{{ event.source }}</div>
                  </div>
                  <span class="recent-item-badge" [ngClass]="event.indexed ? 'badge-indexed' : 'badge-pending'">
                    {{ event.indexed ? 'Indexed' : 'Pending' }}
                  </span>
                </div>
              </div>
            </div>
          </div>

          <!-- Recent Conversations -->
          <div class="col-lg-6">
            <div class="recent-card">
              <div class="recent-card-header">
                <h5>💬 Recent Conversations</h5>
                <a routerLink="/conversations" class="view-all-link">View all →</a>
              </div>
              <div class="recent-card-body">
                <div *ngIf="recentConversations.length === 0" class="empty-state">
                  <div class="empty-state-icon">💬</div>
                  <p>No conversations yet</p>
                  <a routerLink="/conversations" class="btn btn-sm btn-primary mt-2">Start a conversation</a>
                </div>
                <div *ngFor="let conv of recentConversations" class="recent-item">
                  <div class="recent-item-icon chat">💬</div>
                  <div class="recent-item-content">
                    <div class="recent-item-title">{{ conv.title }}</div>
                    <div class="recent-item-meta">{{ conv.messages }} messages · {{ conv.timeAgo }}</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Tips Section -->
      <div class="container pb-4">
        <div class="row">
          <div class="col-12">
            <div class="tips-card">
              <h5>💡 Getting Started Tips</h5>
              <div class="tip-item">
                <span>1️⃣</span>
                <span>Configure your LLM provider (OpenAI, Anthropic, etc.) in Settings</span>
              </div>
              <div class="tip-item">
                <span>2️⃣</span>
                <span>Set up a vector database (Pinecone, Weaviate, ChromaDB) for indexing</span>
              </div>
              <div class="tip-item">
                <span>3️⃣</span>
                <span>Scrape your first event by pasting a conference URL</span>
              </div>
              <div class="tip-item">
                <span>4️⃣</span>
                <span>Start chatting with your indexed content using RAG-powered conversations</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  `
})
export class DashboardComponent implements OnInit {
  userName = 'User';
  isLoading = true;

  stats = {
    events: 0,
    conversations: 0,
    vectorStores: 0,
    providers: 0
  };

  recentEvents: Array<{ name: string; source: string; indexed: boolean }> = [];
  recentConversations: Array<{ title: string; messages: number; timeAgo: string }> = [];

  constructor(private auth: AuthService, private api: ApiService) {}

  async ngOnInit() {
    // Load user info
    try {
      const user = await this.auth.me();
      if (user) {
        this.userName = user.first_name || 'User';
      }
    } catch (e) {
      console.error('Failed to load user info', e);
    }

    // Load dashboard data from API
    await this.loadDashboardData();
  }

  private async loadDashboardData(): Promise<void> {
    try {
      this.isLoading = true;
      const response: DashboardDataResponse = await this.api.getDashboardData(1, 5);

      if (response.success) {
        // Map stats
        if (response.stats) {
          this.stats = {
            events: response.stats.events || 0,
            conversations: response.stats.conversations || 0,
            vectorStores: response.stats.vector_stores || 0,
            providers: response.stats.providers || 0
          };
        }

        // Map recent events
        if (response.recent_events) {
          this.recentEvents = response.recent_events.map((event: RecentEvent) => ({
            name: event.name,
            source: event.source,
            indexed: event.indexed
          }));
        }

        // Map recent conversations
        if (response.recent_conversations) {
          this.recentConversations = response.recent_conversations.map((conv: RecentConversation) => ({
            title: conv.title,
            messages: conv.messages,
            timeAgo: conv.time_ago
          }));
        }
      } else {
        console.error('Failed to load dashboard data:', response.message);
      }
    } catch (e) {
      console.error('Error loading dashboard data', e);
      // Keep defaults on error
    } finally {
      this.isLoading = false;
    }
  }
}
