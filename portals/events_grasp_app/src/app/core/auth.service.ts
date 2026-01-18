import { Injectable } from '@angular/core';

@Injectable({ providedIn: 'root' })
export class AuthService {
  private readonly TOKEN_KEY = 'eg_auth_token';

  constructor() {}

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

  // placeholder login - in future call backend auth endpoint
  async login(username: string, password: string): Promise<boolean> {
    // Example: call backend for real auth; for now accept any non-empty
    if (!username || !password) return false;
    const fakeToken = 'local-dev-token';
    this.setToken(fakeToken);
    return true;
  }

  logout() {
    this.clearToken();
  }
}
