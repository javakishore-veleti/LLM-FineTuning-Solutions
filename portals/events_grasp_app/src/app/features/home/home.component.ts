import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ApiService } from '../../core/api.service';
import { RouterModule } from '@angular/router';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [CommonModule, RouterModule],
  styles: [`
    .hero-section {
      background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
      padding: 4rem 0;
      color: white;
    }
    .hero-section h1 {
      font-size: 2.75rem;
      font-weight: 700;
      line-height: 1.2;
    }
    .hero-section .highlight {
      background: linear-gradient(90deg, #ffecd2, #fcb69f);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
    }
    .hero-section .lead {
      font-size: 1.2rem;
      opacity: 0.95;
    }
    .hero-section ul {
      list-style: none;
      padding: 0;
    }
    .hero-section ul li {
      display: flex;
      align-items: center;
      gap: 10px;
      margin-bottom: 0.75rem;
      font-size: 1.05rem;
    }
    .hero-section ul li::before {
      content: '✓';
      background: rgba(255,255,255,0.2);
      border-radius: 50%;
      width: 24px;
      height: 24px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 0.8rem;
    }
    .btn-hero-primary {
      background: white;
      color: #667eea;
      font-weight: 600;
      padding: 0.75rem 1.75rem;
      border-radius: 8px;
      border: none;
      transition: transform 0.2s, box-shadow 0.2s;
    }
    .btn-hero-primary:hover {
      transform: translateY(-2px);
      box-shadow: 0 8px 25px rgba(0,0,0,0.2);
      color: #764ba2;
    }
    .btn-hero-secondary {
      background: transparent;
      color: white;
      font-weight: 600;
      padding: 0.75rem 1.75rem;
      border-radius: 8px;
      border: 2px solid rgba(255,255,255,0.5);
      transition: all 0.2s;
    }
    .btn-hero-secondary:hover {
      background: rgba(255,255,255,0.1);
      border-color: white;
      color: white;
    }
    .events-section {
      padding: 4rem 0;
      background: #f8f9fa;
    }
    .section-title {
      font-size: 2rem;
      font-weight: 700;
      color: #333;
      margin-bottom: 0.5rem;
    }
    .section-subtitle {
      color: #666;
      font-size: 1.1rem;
      margin-bottom: 2rem;
    }
    .event-card {
      background: white;
      border-radius: 16px;
      overflow: hidden;
      box-shadow: 0 4px 20px rgba(0,0,0,0.08);
      transition: transform 0.3s, box-shadow 0.3s;
      height: 100%;
      cursor: pointer;
    }
    .event-card:hover {
      transform: translateY(-8px);
      box-shadow: 0 12px 40px rgba(0,0,0,0.15);
    }
    .event-card-header {
      padding: 1.5rem;
      color: white;
      position: relative;
    }
    .event-card-header.aws { background: linear-gradient(135deg, #ff9900, #ff6600); }
    .event-card-header.microsoft { background: linear-gradient(135deg, #00bcf2, #0078d4); }
    .event-card-header.google { background: linear-gradient(135deg, #4285f4, #34a853); }
    .event-card-header.nvidia { background: linear-gradient(135deg, #76b900, #4a7c00); }
    .event-card-header.platform { background: linear-gradient(135deg, #6366f1, #8b5cf6); }
    .event-card-header.qcon { background: linear-gradient(135deg, #ef4444, #dc2626); }
    .event-badge {
      display: inline-block;
      background: rgba(255,255,255,0.2);
      padding: 4px 10px;
      border-radius: 20px;
      font-size: 0.75rem;
      font-weight: 600;
      margin-bottom: 0.75rem;
    }
    .event-card-header h5 {
      font-size: 1.25rem;
      font-weight: 700;
      margin-bottom: 0.25rem;
    }
    .event-card-header p {
      font-size: 0.9rem;
      opacity: 0.9;
      margin: 0;
    }
    .event-card-body {
      padding: 1.25rem 1.5rem;
    }
    .event-topics {
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
    }
    .event-topic {
      background: #f0f0f0;
      color: #555;
      padding: 4px 10px;
      border-radius: 20px;
      font-size: 0.75rem;
      font-weight: 500;
    }
    .how-it-works {
      padding: 4rem 0;
      background: #f8f9fa;
    }
    .step-card {
      text-align: center;
      padding: 2rem;
    }
    .step-icon {
      width: 80px;
      height: 80px;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 2rem;
      margin: 0 auto 1.25rem;
    }
    .step-card h5 {
      font-weight: 700;
      color: #333;
      margin-bottom: 0.5rem;
    }
    .step-card p {
      color: #666;
      font-size: 0.95rem;
    }
    .step-number {
      position: absolute;
      top: 10px;
      left: 10px;
      background: #667eea;
      color: white;
      width: 28px;
      height: 28px;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: 700;
      font-size: 0.85rem;
    }
  `],
  template: `
    <!-- Hero Section -->
    <div class="hero-section">
      <div class="container">
        <div class="row align-items-center">
          <div class="col-lg-7">
            <h1>Turn event announcements into <span class="highlight">instant, searchable knowledge</span></h1>
            <p class="lead mt-3">Scrape conference announcements, index them into vector stores, and power RAG-ready chat interfaces — all from a single control panel.</p>
            <div class="mt-4 d-flex gap-3">
              <a routerLink="/signup" class="btn btn-hero-primary">Get Started</a>
              <a routerLink="/login" class="btn btn-hero-secondary">Sign In</a>
            </div>
            <ul class="mt-4">
              <li>One-click scraping of event pages</li>
              <li>Index to multiple vector store providers</li>
              <li>Instant RAG chat interfaces for attendees and organizers</li>
            </ul>
          </div>
          <div class="col-lg-5 d-none d-lg-block">
            <div class="text-center" style="font-size: 8rem; opacity: 0.9;">
              🧠💬
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Popular Events Section -->
    <div class="events-section">
      <div class="container">
        <div class="text-center">
          <h2 class="section-title">Popular Tech Events to Scrape</h2>
          <p class="section-subtitle">Index content from the world's leading tech conferences and start chatting with the knowledge</p>
        </div>

        <div class="row g-4">
          <!-- AWS re:Invent -->
          <div class="col-md-6 col-lg-4">
            <div class="event-card">
              <div class="event-card-header aws">
                <span class="event-badge">🔥 Most Popular</span>
                <h5>AWS re:Invent</h5>
                <p>Amazon Web Services</p>
              </div>
              <div class="event-card-body">
                <div class="event-topics">
                  <span class="event-topic">Cloud</span>
                  <span class="event-topic">Serverless</span>
                  <span class="event-topic">AI/ML</span>
                  <span class="event-topic">DevOps</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Microsoft Ignite -->
          <div class="col-md-6 col-lg-4">
            <div class="event-card">
              <div class="event-card-header microsoft">
                <span class="event-badge">☁️ Enterprise</span>
                <h5>Microsoft Ignite</h5>
                <p>Microsoft Corporation</p>
              </div>
              <div class="event-card-body">
                <div class="event-topics">
                  <span class="event-topic">Azure</span>
                  <span class="event-topic">Copilot</span>
                  <span class="event-topic">M365</span>
                  <span class="event-topic">Security</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Google Cloud Next -->
          <div class="col-md-6 col-lg-4">
            <div class="event-card">
              <div class="event-card-header google">
                <span class="event-badge">🌐 Innovation</span>
                <h5>Google Cloud Next</h5>
                <p>Google Cloud</p>
              </div>
              <div class="event-card-body">
                <div class="event-topics">
                  <span class="event-topic">GCP</span>
                  <span class="event-topic">Gemini</span>
                  <span class="event-topic">Kubernetes</span>
                  <span class="event-topic">Data</span>
                </div>
              </div>
            </div>
          </div>

          <!-- NVIDIA GTC -->
          <div class="col-md-6 col-lg-4">
            <div class="event-card">
              <div class="event-card-header nvidia">
                <span class="event-badge">🤖 AI/ML</span>
                <h5>NVIDIA GTC AI Conference</h5>
                <p>NVIDIA Corporation</p>
              </div>
              <div class="event-card-body">
                <div class="event-topics">
                  <span class="event-topic">GPU</span>
                  <span class="event-topic">Deep Learning</span>
                  <span class="event-topic">CUDA</span>
                  <span class="event-topic">Robotics</span>
                </div>
              </div>
            </div>
          </div>

          <!-- PlatformCon -->
          <div class="col-md-6 col-lg-4">
            <div class="event-card">
              <div class="event-card-header platform">
                <span class="event-badge">🛠️ Platform Engineering</span>
                <h5>PlatformCon</h5>
                <p>Platform Engineering Community</p>
              </div>
              <div class="event-card-body">
                <div class="event-topics">
                  <span class="event-topic">IDP</span>
                  <span class="event-topic">DevEx</span>
                  <span class="event-topic">Backstage</span>
                  <span class="event-topic">GitOps</span>
                </div>
              </div>
            </div>
          </div>

          <!-- QCon -->
          <div class="col-md-6 col-lg-4">
            <div class="event-card">
              <div class="event-card-header qcon">
                <span class="event-badge">💡 Software Leaders</span>
                <h5>QCon</h5>
                <p>InfoQ / C4Media</p>
              </div>
              <div class="event-card-body">
                <div class="event-topics">
                  <span class="event-topic">Architecture</span>
                  <span class="event-topic">Leadership</span>
                  <span class="event-topic">AI Adoption</span>
                  <span class="event-topic">Scale</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- How It Works -->
    <div class="how-it-works">
      <div class="container">
        <div class="text-center mb-5">
          <h2 class="section-title">How It Works</h2>
          <p class="section-subtitle">From event link to AI conversation in three simple steps</p>
        </div>

        <div class="row">
          <div class="col-md-4">
            <div class="step-card position-relative">
              <div class="step-icon">🔗</div>
              <h5>1. Paste Event URL</h5>
              <p>Drop any conference or event announcement link — we handle the rest</p>
            </div>
          </div>
          <div class="col-md-4">
            <div class="step-card position-relative">
              <div class="step-icon">🗄️</div>
              <h5>2. Index to Vector DB</h5>
              <p>Content is scraped, chunked, and indexed to your configured vector store</p>
            </div>
          </div>
          <div class="col-md-4">
            <div class="step-card position-relative">
              <div class="step-icon">💬</div>
              <h5>3. Start Chatting</h5>
              <p>Ask questions, get insights — powered by your LLM provider of choice</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  `
})
export class HomeComponent {
  constructor(private api: ApiService) {}
}
