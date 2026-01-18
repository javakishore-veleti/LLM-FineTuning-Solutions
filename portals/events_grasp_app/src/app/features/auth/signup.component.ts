import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule, NgForm } from '@angular/forms';
import { Router, RouterModule } from '@angular/router';
import { AuthService } from '../../core/auth.service';
import { ToastService } from '../../core/toast.service';

@Component({
  selector: 'app-signup',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterModule],
  styles: [`
    .signup-container {
      min-height: 80vh;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
      padding: 2rem;
    }
    .signup-wrapper {
      display: flex;
      justify-content: center;
      align-items: center;
      gap: 4rem;
      max-width: 1100px;
      margin: 0 auto;
      flex-wrap: wrap;
    }
    .hero-section {
      flex: 1;
      min-width: 320px;
      max-width: 480px;
      color: white;
      animation: slideInLeft 0.6s ease-out;
    }
    @keyframes slideInLeft {
      from { opacity: 0; transform: translateX(-30px); }
      to { opacity: 1; transform: translateX(0); }
    }
    .hero-section h1 {
      font-size: 2.5rem;
      font-weight: 700;
      margin-bottom: 1rem;
      line-height: 1.2;
    }
    .hero-section .highlight {
      background: linear-gradient(90deg, #ffecd2, #fcb69f);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
    }
    .hero-section p {
      font-size: 1.15rem;
      opacity: 0.95;
      margin-bottom: 1.5rem;
      line-height: 1.6;
    }
    .feature-list {
      list-style: none;
      padding: 0;
      margin: 0;
    }
    .feature-list li {
      display: flex;
      align-items: center;
      gap: 12px;
      margin-bottom: 1rem;
      font-size: 1rem;
      opacity: 0.95;
    }
    .feature-icon {
      width: 36px;
      height: 36px;
      background: rgba(255,255,255,0.2);
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 1.1rem;
    }
    .auth-card {
      flex: 0 0 420px;
      background: white;
      border-radius: 16px;
      box-shadow: 0 20px 60px rgba(0,0,0,0.15);
      padding: 2.5rem;
      animation: slideInRight 0.6s ease-out;
    }
    @keyframes slideInRight {
      from { opacity: 0; transform: translateX(30px); }
      to { opacity: 1; transform: translateX(0); }
    }
    .auth-card h4 {
      font-size: 1.5rem;
      font-weight: 600;
      color: #333;
      margin-bottom: 0.5rem;
    }
    .auth-card .subtitle {
      color: #666;
      font-size: 0.95rem;
      margin-bottom: 1.5rem;
    }
    .form-label {
      font-weight: 500;
      color: #444;
    }
    .form-control {
      border-radius: 8px;
      padding: 0.75rem 1rem;
      border: 1.5px solid #e0e0e0;
      transition: border-color 0.2s, box-shadow 0.2s;
    }
    .form-control:focus {
      border-color: #667eea;
      box-shadow: 0 0 0 3px rgba(102,126,234,0.15);
    }
    .password-wrapper {
      position: relative;
    }
    .show-pass-btn {
      position: absolute;
      right: 12px;
      top: 50%;
      transform: translateY(-50%);
      border: none;
      background: transparent;
      color: #667eea;
      font-size: 0.85rem;
      cursor: pointer;
      font-weight: 500;
    }
    .password-hint {
      margin-top: 8px;
      font-size: 0.85rem;
    }
    .password-hint .weak { color: #e53935; }
    .password-hint .medium { color: #fb8c00; }
    .password-hint .strong { color: #43a047; }
    .strength-bar {
      height: 4px;
      border-radius: 2px;
      background: #e0e0e0;
      margin-top: 8px;
      overflow: hidden;
    }
    .strength-bar-fill {
      height: 100%;
      border-radius: 2px;
      transition: width 0.3s, background 0.3s;
    }
    .strength-bar-fill.weak { width: 33%; background: #e53935; }
    .strength-bar-fill.medium { width: 66%; background: #fb8c00; }
    .strength-bar-fill.strong { width: 100%; background: #43a047; }
    .strength-bar-fill.empty { width: 0%; }
    .btn-signup {
      width: 100%;
      padding: 0.85rem;
      font-size: 1rem;
      font-weight: 600;
      border-radius: 8px;
      border: none;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      color: white;
      cursor: pointer;
      transition: transform 0.2s, box-shadow 0.2s;
    }
    .btn-signup:hover:not(:disabled) {
      transform: translateY(-2px);
      box-shadow: 0 8px 25px rgba(102,126,234,0.4);
    }
    .btn-signup:disabled {
      opacity: 0.6;
      cursor: not-allowed;
    }
    .btn-signup .spinner {
      display: inline-block;
      width: 18px;
      height: 18px;
      border: 2px solid rgba(255,255,255,0.3);
      border-top-color: white;
      border-radius: 50%;
      animation: spin 0.8s linear infinite;
      margin-right: 8px;
      vertical-align: middle;
    }
    @keyframes spin {
      to { transform: rotate(360deg); }
    }
    .login-link {
      text-align: center;
      margin-top: 1.25rem;
      color: #666;
      font-size: 0.95rem;
    }
    .login-link a {
      color: #667eea;
      font-weight: 600;
      text-decoration: none;
    }
    .login-link a:hover {
      text-decoration: underline;
    }
    .trust-badges {
      display: flex;
      justify-content: center;
      gap: 1.5rem;
      margin-top: 1.5rem;
      padding-top: 1.25rem;
      border-top: 1px solid #eee;
    }
    .trust-badge {
      display: flex;
      align-items: center;
      gap: 6px;
      font-size: 0.8rem;
      color: #888;
    }
    @media (max-width: 900px) {
      .signup-wrapper { flex-direction: column; gap: 2rem; }
      .hero-section { text-align: center; }
      .auth-card { flex: none; width: 100%; max-width: 420px; }
    }
  `],
  template: `
  <div class="signup-container">
    <div class="signup-wrapper">
<!-- Hero Section -->
      <div class="hero-section">
        <h1>Turn event content into <span class="highlight">intelligent conversations</span> 🧠</h1>
        <p>Paste any event link — we scrape, index, and let you chat with the content using AI. Your knowledge base, your vector DB, your LLM.</p>

        <ul class="feature-list">
          <li>
            <span class="feature-icon">🔗</span>
            <span><strong>Smart Scraping</strong> — Drop a link, we extract everything</span>
          </li>
          <li>
            <span class="feature-icon">🗄️</span>
            <span><strong>Vector Indexing</strong> — Connect your Pinecone, Weaviate, or more</span>
          </li>
          <li>
            <span class="feature-icon">💬</span>
            <span><strong>AI Conversations</strong> — Chat with your content using any LLM</span>
          </li>
          <li>
            <span class="feature-icon">🔐</span>
            <span><strong>Your Credentials</strong> — Bring your own API keys, fully secure</span>
          </li>
        </ul>
      </div>

      <!-- Signup Card -->
      <div class="auth-card">
        <h4>Create your account</h4>
        <p class="subtitle">Start building your AI knowledge base in minutes 🚀</p>

        <form #signupForm="ngForm" (ngSubmit)="onSubmit(signupForm)">
          <div class="row">
            <div class="col-6 mb-3">
              <label class="form-label">First name</label>
              <input
                class="form-control"
                name="firstName"
                [(ngModel)]="firstName"
                #firstNameRef="ngModel"
                required
                placeholder="Jane"
                aria-label="First name"
              />
              <div class="text-danger small mt-1" *ngIf="firstNameRef.invalid && (firstNameRef.dirty || submitted)" aria-live="polite">
                Required
              </div>
            </div>

            <div class="col-6 mb-3">
              <label class="form-label">Last name</label>
              <input
                class="form-control"
                name="lastName"
                [(ngModel)]="lastName"
                #lastNameRef="ngModel"
                required
                placeholder="Doe"
                aria-label="Last name"
              />
              <div class="text-danger small mt-1" *ngIf="lastNameRef.invalid && (lastNameRef.dirty || submitted)" aria-live="polite">
                Required
              </div>
            </div>
          </div>

          <div class="mb-3">
            <label class="form-label">Email</label>
            <input
              type="email"
              class="form-control"
              name="email"
              [(ngModel)]="email"
              #emailRef="ngModel"
              required
              placeholder="jane@example.com"
              aria-label="Email address"
            />
            <div class="text-danger small mt-1" *ngIf="emailRef.invalid && (emailRef.dirty || submitted)" aria-live="polite">
              <span *ngIf="emailRef.errors?.['required']">Email is required</span>
              <span *ngIf="emailRef.errors?.['email']">Enter a valid email</span>
            </div>
          </div>

          <div class="mb-3">
            <label class="form-label">Password</label>
            <div class="password-wrapper">
              <input
                [type]="showPassword ? 'text' : 'password'"
                class="form-control"
                name="password"
                [(ngModel)]="password"
                #passwordRef="ngModel"
                required
                minlength="8"
                placeholder="Min 8 characters"
                aria-label="Password"
                style="padding-right: 60px"
              />
              <button type="button" class="show-pass-btn" (click)="showPassword = !showPassword">
                {{ showPassword ? 'Hide' : 'Show' }}
              </button>
            </div>

            <div class="strength-bar">
              <div class="strength-bar-fill" [ngClass]="passwordStrengthClass(password)"></div>
            </div>

            <div class="password-hint" [ngClass]="passwordStrengthClass(password)">
              {{ passwordStrengthLabel(password) }}
            </div>

            <div class="text-danger small mt-1" *ngIf="passwordRef.invalid && (passwordRef.dirty || submitted)" aria-live="polite">
              <span *ngIf="passwordRef.errors?.['required']">Password is required</span>
              <span *ngIf="passwordRef.errors?.['minlength']">At least 8 characters needed</span>
            </div>
          </div>

          <button type="submit" class="btn-signup" [disabled]="loading || !signupForm.form.valid">
            <span class="spinner" *ngIf="loading"></span>
            <span *ngIf="loading">Creating your account...</span>
            <span *ngIf="!loading">Start scraping smarter →</span>
          </button>
        </form>

        <p class="login-link">
          Already have an account? <a routerLink="/login">Sign in</a>
        </p>

        <div class="trust-badges">
          <span class="trust-badge">🔒 Your keys stay yours</span>
          <span class="trust-badge">⚡ Unlimited scraping</span>
          <span class="trust-badge">🧠 Any LLM provider</span>
        </div>
      </div>
    </div>
  </div>
  `
})
export class SignupComponent {
  firstName = '';
  lastName = '';
  email = '';
  password = '';

  loading = false;
  submitted = false;
  showPassword = false;

  constructor(private auth: AuthService, private router: Router, private toast: ToastService) {}

  passwordStrengthLabel(pw: string): string {
    if (!pw) return '';
    const score = this.simplePasswordScore(pw);
    if (score >= 4) return '💪 Strong password';
    if (score >= 2) return '👍 Getting better';
    return '🔑 Keep going...';
  }

  passwordStrengthClass(pw: string): string {
    if (!pw) return 'empty';
    const score = this.simplePasswordScore(pw);
    if (score >= 4) return 'strong';
    if (score >= 2) return 'medium';
    return 'weak';
  }

  private simplePasswordScore(pw: string): number {
    let score = 0;
    if (pw.length >= 8) score++;
    if (pw.length >= 12) score++;
    if (/[0-9]/.test(pw)) score++;
    if (/[a-z]/.test(pw) && /[A-Z]/.test(pw)) score++;
    if (/[^A-Za-z0-9]/.test(pw)) score++;
    return score;
  }

  async onSubmit(form: NgForm) {
    this.submitted = true;
    if (!form.valid) {
      this.toast.error('Please complete all fields');
      return;
    }

    this.loading = true;
    try {
      await this.auth.signup({ first_name: this.firstName, last_name: this.lastName, email: this.email, password: this.password });
      this.toast.success('🎉 Welcome! Please sign in to start scraping');
      await this.router.navigateByUrl('/login');
    } catch (e: any) {
      // Show user-friendly error messages based on error type
      const status = e?.status;
      const detail = e?.error?.detail || '';

      if (status === 400 && detail.toLowerCase().includes('email already')) {
        this.toast.error('This email is already registered. Please sign in or use a different email.');
      } else if (status === 400) {
        this.toast.error('Invalid information provided. Please check your details and try again.');
      } else if (status === 0 || status === 503 || status === 504) {
        this.toast.error('Unable to connect to server. Please check your internet connection.');
      } else {
        this.toast.error('Something went wrong. Please try again later.');
      }
    } finally {
      this.loading = false;
    }
  }
}
