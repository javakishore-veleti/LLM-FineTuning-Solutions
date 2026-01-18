import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule, NgForm } from '@angular/forms';
import { Router, RouterModule, ActivatedRoute } from '@angular/router';
import { AuthService } from '../../core/auth.service';
import { ToastService } from '../../core/toast.service';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterModule],
  styles: [`
    .login-container {
      min-height: 80vh;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
      padding: 2rem;
    }
    .login-wrapper {
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
    .stats-row {
      display: flex;
      gap: 2rem;
      margin-top: 2rem;
    }
    .stat-item {
      text-align: center;
    }
    .stat-number {
      font-size: 2rem;
      font-weight: 700;
      display: block;
    }
    .stat-label {
      font-size: 0.9rem;
      opacity: 0.85;
    }
    .auth-card {
      flex: 0 0 400px;
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
    .btn-login {
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
    .btn-login:hover:not(:disabled) {
      transform: translateY(-2px);
      box-shadow: 0 8px 25px rgba(102,126,234,0.4);
    }
    .btn-login:disabled {
      opacity: 0.6;
      cursor: not-allowed;
    }
    .btn-login .spinner {
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
    .signup-link {
      text-align: center;
      margin-top: 1.25rem;
      color: #666;
      font-size: 0.95rem;
    }
    .signup-link a {
      color: #667eea;
      font-weight: 600;
      text-decoration: none;
    }
    .signup-link a:hover {
      text-decoration: underline;
    }
    .divider {
      display: flex;
      align-items: center;
      margin: 1.5rem 0;
      color: #999;
      font-size: 0.85rem;
    }
    .divider::before, .divider::after {
      content: '';
      flex: 1;
      height: 1px;
      background: #e0e0e0;
    }
    .divider::before { margin-right: 1rem; }
    .divider::after { margin-left: 1rem; }
    .forgot-link {
      font-size: 0.85rem;
      color: #667eea;
      text-decoration: none;
    }
    .forgot-link:hover {
      text-decoration: underline;
    }
    @media (max-width: 900px) {
      .login-wrapper { flex-direction: column; gap: 2rem; }
      .hero-section { text-align: center; }
      .stats-row { justify-content: center; }
      .auth-card { flex: none; width: 100%; max-width: 400px; }
    }
  `],
  template: `
  <div class="login-container">
    <div class="login-wrapper">
<!-- Hero Section -->
      <div class="hero-section">
        <h1>Your AI-powered <span class="highlight">knowledge base</span> awaits 🧠</h1>
        <p>Sign in to continue scraping event content, indexing to your vector databases, and having intelligent conversations with your data.</p>

        <div class="stats-row">
          <div class="stat-item">
            <span class="stat-number">50+</span>
            <span class="stat-label">Event sources</span>
          </div>
          <div class="stat-item">
            <span class="stat-number">10+</span>
            <span class="stat-label">Vector DBs</span>
          </div>
          <div class="stat-item">
            <span class="stat-number">Any</span>
            <span class="stat-label">LLM provider</span>
          </div>
        </div>
      </div>

      <!-- Login Card -->
      <div class="auth-card">
        <h4>Sign in to your account</h4>
        <p class="subtitle">Continue building your knowledge base 💬</p>

        <form #loginForm="ngForm" (ngSubmit)="onSubmit(loginForm)">
          <div class="mb-3">
            <label class="form-label">Email</label>
            <input
              type="email"
              class="form-control"
              name="username"
              [(ngModel)]="username"
              #usernameRef="ngModel"
              required
              placeholder="you@example.com"
              aria-label="Email address"
            />
            <div class="text-danger small mt-1" *ngIf="usernameRef.invalid && (usernameRef.dirty || submitted)" aria-live="polite">
              Email is required
            </div>
          </div>

          <div class="mb-3">
            <div class="d-flex justify-content-between align-items-center">
              <label class="form-label mb-0">Password</label>
              <a href="#" class="forgot-link">Forgot password?</a>
            </div>
            <div class="password-wrapper mt-1">
              <input
                [type]="showPassword ? 'text' : 'password'"
                class="form-control"
                name="password"
                [(ngModel)]="password"
                #passwordRef="ngModel"
                required
                placeholder="Enter your password"
                aria-label="Password"
                style="padding-right: 60px"
              />
              <button type="button" class="show-pass-btn" (click)="showPassword = !showPassword">
                {{ showPassword ? 'Hide' : 'Show' }}
              </button>
            </div>
            <div class="text-danger small mt-1" *ngIf="passwordRef.invalid && (passwordRef.dirty || submitted)" aria-live="polite">
              Password is required
            </div>
          </div>

          <button type="submit" class="btn-login" [disabled]="loading || !loginForm.form.valid">
            <span class="spinner" *ngIf="loading"></span>
            <span *ngIf="loading">Signing in...</span>
            <span *ngIf="!loading">Access your workspace →</span>
          </button>
        </form>

        <div class="divider">or</div>

        <p class="signup-link">
          New to Events Grasp? <a routerLink="/signup">Create an account</a>
        </p>
      </div>
    </div>
  </div>
  `
})
export class LoginComponent {
  username = '';
  password = '';
  loading = false;
  submitted = false;
  showPassword = false;
  private redirect = '/dashboard';

  constructor(private auth: AuthService, private router: Router, private toast: ToastService, private route: ActivatedRoute) {
    this.route.queryParams.subscribe(q => {
      if (q['redirect']) this.redirect = q['redirect'];
    });
  }

  async onSubmit(form: NgForm) {
    this.submitted = true;
    if (!form.valid) {
      this.toast.error('Please enter your email and password');
      return;
    }

    this.loading = true;
    try {
      const ok = await this.auth.login(this.username, this.password);
      if (ok) {
        this.toast.success('🎉 Welcome back! Ready to chat with your data');
        await this.router.navigateByUrl(this.redirect || '/dashboard');
      } else {
        this.toast.error('Invalid email or password');
      }
    } catch (e: any) {
      this.toast.error('Login failed: ' + (e?.message || 'Please try again'));
    } finally {
      this.loading = false;
    }
  }
}
