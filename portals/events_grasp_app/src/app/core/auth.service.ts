import { Injectable } from '@angular/core';
import { ApiService } from './api.service';

@Injectable({ providedIn: 'root' })
export class AuthService {
  private readonly TOKEN_KEY = 'eg_auth_token';

  constructor(private api: ApiService) {}

  getToken(): string | null {
    return localStorage.getItem(this.TOKEN_KEY);
  }

  setToken(token: string) {
    localStorage.setItem(this.TOKEN_KEY, token);
  }

  clearToken() {
    localStorage.removeItem(this.TOKEN_KEY);
  }

  isAuthenticated(): boolean {
    return !!this.getToken();
  }

  async signup(payload: { first_name: string; last_name: string; email: string; password: string }) {
    return await this.api.request('/api/auth/signup', { method: 'POST', body: payload });
  }

  async login(email: string, password: string): Promise<boolean> {
    const resp = await this.api.request('/api/auth/login', { method: 'POST', body: { email, password } });
    if (resp && resp.token) {
      this.setToken(resp.token);
      return true;
    }
    return false;
  }

  async logout() {
    const token = this.getToken();
    if (token) {
      try {
        await this.api.request('/api/auth/logout', { method: 'POST', body: { token } });
      } catch (e) {
        // ignore
      }
    }
    this.clearToken();
  }

  async me() {
    const token = this.getToken();
    if (!token) return null;
    return await this.api.request('/api/auth/me?token=' + encodeURIComponent(token));
  }
}
